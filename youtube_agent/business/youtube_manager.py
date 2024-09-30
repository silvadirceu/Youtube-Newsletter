from typing import List
from ...youtube_manager import schemas
from ...youtube_manager.business import youtube_manager
from youtube_agent.services.config import settings
import requests

YOUTUBE_MANAGER_HOST = settings.YOUTUBE_MANAGER_HOST
YOUTUBE_MANAGER_PORT = settings.YOUTUBE_MANAGER_PORT

class BusinessYoutubeManager():

    def search(self, name: str) -> schemas.Channel:
        """
        Searches a channel by name and returns a channel_id.
        """
        json_data = {"name": name}
        response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/analyzer/channels/search", json=json_data)
        return response.json()


    def get_channel_videos(self, channel_id: str, start_date: str, end_date: str = None) -> List[schemas.Video]:
        """
        Returns a video list from a channel within a specified date range.
        """
        # json_data = {"name": name}
        # response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/analyzer/channels/search", json=json_data)
        # return response.json()


    
    def get_video_details(self, video_ids: List[schemas.Video]) -> List[schemas.VideoBase]:
        """
        Returns a list of details from each video.
        """
        json_data = {"video_ids": video_ids}
        response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/analyzer/videos", json=json_data)
        return response.json()

    
    async def download_audio(self, videos: List[schemas.VideoBase]) -> str:
        """
        Downloads the audios from a video list.
        """
        json_data = {"videos": videos}
        response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/downloader/audios", json=json_data)
        return response.json()



    async def download_video(self, videos: List[schemas.VideoBase]) -> str:
        """
        Downloads the videos from a video list.
        """
        json_data = {"videos": videos}
        response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/downloader/videos", json=json_data)
        return response.json()


youtube_manager = BusinessYoutubeManager()
