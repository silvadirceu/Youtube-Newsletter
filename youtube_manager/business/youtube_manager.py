import ffmpeg
from youtube_manager import schemas
from typing import List
from googleapiclient.discovery import build
import youtube_manager.service as service
import re
import pandas as pd
import os
from pytubefix import YouTube
from fastapi import HTTPException, status
import base64
import httpx
import asyncio

class BusinessYoutubeManager():
    def __init__(self, youtube, api_key):
        self.youtube = youtube
        self.api_key = api_key

    def search(self, channels: schemas.Channels) -> schemas.Channel:
        """
        Searches a channel by name and returns a channel_id.
        """
        channels_ids = []
        try:
            for name in channels.names:
                request = self.youtube.search().list(
                    part="snippet",
                    q=name,
                    type="channel",
                    maxResults=1
                )
                response = request.execute()
                channels_ids.append(response['items'][0]['snippet']['channelId'])

                if not response.get('items'):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found.")
            
            return schemas.Channel(ids=channels_ids)
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    def get_channel_videos(self, channel_id: str, start_date: str, end_date: str = None) -> List[schemas.Video]:
        """
        Returns a video list from a channel within a specified date range.
        """
        try:
            start_date = pd.to_datetime(start_date).tz_localize(None)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid start date format.")
        
        if end_date:
            try:
                end_date = pd.to_datetime(end_date).tz_localize(None)
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid end date format.")
        else:
            end_date = pd.Timestamp.now().tz_localize(None)

        if start_date > end_date:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date must be before end date.")

        video_ids = []
        next_page_token = None

        try:
            while True:
                request = self.youtube.channels().list(
                    part="contentDetails",
                    id=channel_id,
                    maxResults=50,
                    pageToken=next_page_token
                )
                response = request.execute()

                if not response.get('items'):
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found.")

                uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

                videos_request = self.youtube.playlistItems().list(
                    part="snippet",
                    playlistId=uploads_id,
                    maxResults=5,
                    pageToken=next_page_token
                )
                videos = videos_request.execute()
                
                items = videos.get('items', [])
                
                items = [
                    video for video in items 
                    if start_date <= pd.to_datetime(video['snippet']['publishedAt']).tz_localize(None) <= end_date
                ]
                
                video_ids.extend(schemas.Video(id=item['snippet']['resourceId']['videoId']) for item in items)

                next_page_token = videos.get('nextPageToken')
                if not next_page_token or len(items) == 0:
                    break

            if not video_ids:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No videos found in the specified date range.")
            
            return video_ids
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    
    async def get_video_details(self, video_ids: List[schemas.Video]) -> List[schemas.VideoBase]:
        """
        Returns a list of details from each video, fetched asynchronously.
        """
        if not video_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No video IDs provided.")

        try:
            videos = []
            async with httpx.AsyncClient() as client:
                for i in range(0, len(video_ids), 50): 
                    video_id_slice = [video.id for video in video_ids[i:i+50] if video.id]
                    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={','.join(video_id_slice)}&key={self.api_key}"
                    
                    response = await client.get(url)
                    response.raise_for_status()
                    data = response.json()

                    for item in data.get('items', []):
                        video_data = schemas.VideoBase(
                            id=item['id'],
                            title=re.sub(r'[^\w\s]', '', item['snippet']['title']).strip(),
                            description=item['snippet'].get('description'),
                            publishedAt=item['snippet']['publishedAt'],
                            thumbnail=item['snippet']['thumbnails']['default']['url'],
                            channelTitle=item['snippet']['channelTitle'],
                            duration=item['contentDetails']['duration'],
                            viewCount=item['statistics'].get('viewCount'),
                            likeCount=item['statistics'].get('likeCount'),
                            commentCount=item['statistics'].get('commentCount'),
                            url=f"https://www.youtube.com/watch?v={item['id']}"
                        )
                        videos.append(video_data)
                    
            if not videos:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No video details found.")
            
            return videos

        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error fetching video details: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    async def download_audio(self, videos: List[schemas.VideoBase]) -> List[schemas.AudioBytes]:
        if not videos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No video list provided.")
        
        audio_data = []

        try:
            for video in videos:
                yt = YouTube(str(video.url))
                stream_url = yt.streams[0].url

                # Executa o ffmpeg de forma assíncrona usando subprocess
                process = await asyncio.create_subprocess_exec(
                    'ffmpeg',
                    '-i', stream_url,
                    '-f', 'wav',
                    '-acodec', 'pcm_s16le',
                    'pipe:1',  # saída padrão (stdout)
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                audio, err = await process.communicate()

                # Verifica se houve erro na execução do ffmpeg
                if process.returncode != 0:
                    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"FFmpeg error: {err.decode()}")

                # Encode audio bytes to base64 string
                audio_base64 = base64.b64encode(audio).decode('utf-8')
                audio_data.append(schemas.AudioBytes(bytes=audio_base64))

            return audio_data

        except FileNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    # def download_audio(self, videos: List[schemas.VideoBase]) -> List[schemas.AudioBytes]:
    #     if not videos:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No video list provided.")
        
    #     audio_data = []

    #     try:
    #         for video in videos:
    #             yt = YouTube(str(video.url))
    #             stream_url = yt.streams[0].url

    #             audio, err = (
    #                 ffmpeg
    #                 .input(stream_url)
    #                 .output("pipe:", format='wav', 
    #                         acodec='pcm_s16le', 
    #                         loglevel="error")  
    #                 .run(capture_stdout=True)
    #             )

    #             # Encode audio bytes to base64 string
    #             audio_base64 = base64.b64encode(audio).decode('utf-8')
    #             audio_data.append(schemas.AudioBytes(bytes=audio_base64))
                
    #         return audio_data

    #     except FileNotFoundError as e:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found: {str(e)}")
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




    # def download_video(self, videos: List[schemas.VideoBase]) -> str:
    #     if not videos:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No video list provided.")
        
    #     try:
    #         for video in videos:
    #             base_dir = f"videos/{video.channelTitle}"
    #             os.makedirs(base_dir, exist_ok=True)

    #             # Verificar se o vídeo já foi baixado
    #             actual_videos = [i.split(".mp4")[0] for i in os.listdir(base_dir)]
    #             if video.title not in actual_videos:     
    #                 yt = YouTube(str(video.url))

    #                 # Buscar a melhor stream de vídeo (pode incluir áudio junto)
    #                 stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
                    
    #                 if not stream:
    #                     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No suitable video stream found.")

    #                 # Download do vídeo diretamente no diretório
    #                 stream.download(output_path=base_dir, filename=f"{video.title}.mp4")

    #         return "Videos downloaded!"

    #     except FileNotFoundError as e:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found: {str(e)}")
    #     except Exception as e:
    #         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



youtube = build('youtube', 'v3', developerKey=service.settings.YOUTUBE_API_KEY)

youtube_manager = BusinessYoutubeManager(youtube, service.settings.YOUTUBE_API_KEY)
