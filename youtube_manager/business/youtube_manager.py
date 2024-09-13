import ffmpeg
from youtube_manager import schemas
from typing import Any, List
from googleapiclient.discovery import build
import youtube_manager.service as service
import re
import pandas as pd
import os
from pytubefix import YouTube

class BusinessYoutubeManager():
    def __init__(self, youtube):
        self.youtube = youtube

    def search(self, name: str) -> schemas.Channel:
        """
        Searches a channel by name and returns a channel_id.
        """
        request = self.youtube.search().list(
            part="snippet",
            q=name,
            type="channel",
            maxResults=1
        )
        response = request.execute()
        if response.get('items'):
            return schemas.Channel(id=response['items'][0]['snippet']['channelId'])
        return None

    def get_channel_videos(self, channel_id: str, cutoff_date: str) -> List[schemas.Video]:
        """
        Returns a video_id list from a channel.
        """
        cutoff = pd.to_datetime(cutoff_date)
        video_ids = []
        next_page_token = None

        while True:
            request = self.youtube.channels().list(
                part="contentDetails",
                id=channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
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

            # Verifica se há mais páginas
            next_page_token = videos.get('nextPageToken')
            if not next_page_token or len(items) == 0:
                break

        return video_ids

    
    def get_video_details(self, video_ids: List[schemas.Video]) -> List[schemas.VideoBase]:
        videos = []
        for i in range(0, len(video_ids), 50): 
            video_id_slice = [video.id for video in video_ids[i:i+50] if video.id]
            request = youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=",".join(video_id_slice) 
            )
            response = request.execute()

            for item in response.get('items', []):
                print("\n\n\n", item, "\n\n\n")
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
                videos.append(video_data)  # Converte para dict se precisar em outro formato
        return videos
    
    def download_audio(self, videos: List[schemas.VideoBase]) -> str:
        for video in videos:
            base_dir = f"audios/{video.channelTitle}"
            os.makedirs(base_dir, exist_ok=True)

            # Verifica se o áudio já foi baixado
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

                # Salva o áudio em formato .wav
                with open(f'{base_dir}/{video.title}.wav', 'wb') as f:
                    f.write(audio)

        return "Audios downloaded!"



youtube = build('youtube', 'v3', developerKey=service.settings.YOUTUBE_API_KEY)

youtube_manager = BusinessYoutubeManager(youtube)
