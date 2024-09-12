from fastapi import UploadFile
from faster_whisper import WhisperModel
import ffmpeg
from youtube_manager import schemas
from typing import Any, List
from googleapiclient.discovery import build
import youtube_manager.service as service
from dateutil import parser
import re

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
        cutoff = parser.isoparse(cutoff_date)
        video_ids = []
        next_page_token = None

        while True:
            request = self.youtube.search().list(
                part="snippet",
                channelId=channel_id,
                maxResults=50,
                order="date",
                type="video",
                pageToken=next_page_token
            )
            response = request.execute()
            videos = response.get('items', [])
            if cutoff:
                videos = [video for video in videos if parser.isoparse(video['snippet']['publishedAt']) > cutoff]
            
            video_ids.extend(schemas.VideoBase(id=item['id']['videoId']) for item in videos)

            # Verifica se há mais páginas
            next_page_token = response.get('nextPageToken')
            if not next_page_token or len(videos) == 0:
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
                video_data = schemas.VideoBase(
                    id=item['id'],
                    title=re.sub(r'[^\w\s]', '', item['snippet']['title']).strip(),
                    description=item['snippet'].get('description'),
                    publishedAt=item['snippet']['publishedAt'],
                    thumbnail=item['snippet']['thumbnails']['default']['url'],
                    duration=item['contentDetails']['duration'],
                    viewCount=item['statistics'].get('viewCount'),
                    likeCount=item['statistics'].get('likeCount'),
                    commentCount=item['statistics'].get('commentCount'),
                    url=f"https://www.youtube.com/watch?v={item['id']}"
                )
                videos.append(video_data)  # Converte para dict se precisar em outro formato
        return videos

youtube = build('youtube', 'v3', developerKey=service.settings.YOUTUBE_API_KEY)

youtube_manager = BusinessYoutubeManager(youtube)
