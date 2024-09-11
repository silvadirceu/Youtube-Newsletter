from fastapi import UploadFile
from faster_whisper import WhisperModel
import ffmpeg
from youtube_manager import schemas
from typing import Any
from googleapiclient.discovery import build
import youtube_manager.service as service

class BusinessYoutubeManager():
    def __init__(self, youtube) -> None:
        self.youtube = youtube

    def search(self, name: str) -> Any:
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
        print("response: ", response)
        if response.get('items'):
            print("\n\n\n", response['items'][0]['snippet']['channelId'], "\n\n\n")
            return response['items'][0]['snippet']['channelId']
        return None


youtube = build('youtube', 'v3', developerKey=service.settings.YOUTUBE_API_KEY)

youtube_manager = BusinessYoutubeManager(youtube)
