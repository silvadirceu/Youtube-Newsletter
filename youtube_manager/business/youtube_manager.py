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

class BusinessYoutubeManager():
    def __init__(self, youtube):
        self.youtube = youtube

    def search(self, name: str) -> schemas.Channel:
        """
        Searches a channel by name and returns a channel_id.
        """
        try:
            request = self.youtube.search().list(
                part="snippet",
                q=name,
                type="channel",
                maxResults=1
            )
            response = request.execute()

            if not response.get('items'):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Channel not found.")
            
            return schemas.Channel(id=response['items'][0]['snippet']['channelId'])
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


    def get_channel_videos(self, channel_id: str, cutoff_date: str) -> List[schemas.Video]:
        """
        Returns a video_id list from a channel.
        """
        try:
            cutoff = pd.to_datetime(cutoff_date)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid cutoff date format.")

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
                if cutoff:
                    items = [video for video in items if pd.to_datetime(video['snippet']['publishedAt']) > cutoff]
                
                video_ids.extend(schemas.Video(id=item['snippet']['resourceId']['videoId']) for item in items)

                next_page_token = videos.get('nextPageToken')
                if not next_page_token or len(items) == 0:
                    break

            if not video_ids:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No videos found.")
            
            return video_ids
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
    def get_video_details(self, video_ids: List[schemas.Video]) -> List[schemas.VideoBase]:
        if not video_ids:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No video IDs provided.")

        try:
            videos = []
            for i in range(0, len(video_ids), 50): 
                video_id_slice = [video.id for video in video_ids[i:i+50] if video.id]
                request = self.youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=",".join(video_id_slice) 
                )
                response = request.execute()

                for item in response.get('items', []):
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

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    
    def download_audio(self, videos: List[schemas.VideoBase]) -> str:
        if not videos:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No video list provided.")
        
        try:
            for video in videos:
                base_dir = f"audios/{video.channelTitle}"
                os.makedirs(base_dir, exist_ok=True)

                actual_audios = [i.split(".wa")[0] for i in os.listdir(base_dir)]
                if video.title not in actual_audios:
                    print(f"Downloading {video.title} from {video.url}.")
                    yt = YouTube(str(video.url))

                    stream_url = yt.streams[0].url
                    audio, err = (
                        ffmpeg
                        .input(stream_url)
                        .output("pipe:", format='wav', 
                                acodec='pcm_s16le', 
                                loglevel="error")  
                        .run(capture_stdout=True)
                    )

                    with open(f'{base_dir}/{video.title}.wav', 'wb') as f:
                        f.write(audio)

            return "Audios downloaded!"

        except FileNotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File not found: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))




youtube = build('youtube', 'v3', developerKey=service.settings.YOUTUBE_API_KEY)

youtube_manager = BusinessYoutubeManager(youtube)
