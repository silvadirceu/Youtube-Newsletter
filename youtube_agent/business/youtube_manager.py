from typing import List
from youtube_agent import schemas
from youtube_agent.services.config import settings
import requests
import re
from pydantic import AnyUrl

YOUTUBE_MANAGER_HOST = settings.YOUTUBE_MANAGER_HOST
YOUTUBE_MANAGER_PORT = settings.YOUTUBE_MANAGER_PORT

class BusinessYoutubeManager():

    def search(self, name: List[str]) -> schemas.Channel:
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
        json_data = {"channel_id": channel_id, "start_date": start_date, "end_date": end_date}
        response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/analyzer/channels/search", json=json_data)
        return response.json()


    
    def get_video_details(self, video_ids: List[schemas.Video]) -> List[schemas.VideoBase]:
        """
        Returns a list of details from each video.
        """
        json_data = [video.model_dump() for video in video_ids]
        response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/analyzer/videos", json=json_data)
        return response.json()

    
    def download_audio(self, videos: List[schemas.VideoBase]) -> List[schemas.AudioBytes]:
        """
        Downloads the audios from a video list.
        """
        # Converta os campos do tipo Url para strings
        json_data = []
        for video in videos:
            video_data = video.model_dump()
            # Se o campo de URL existir e for um objeto Url, converte para string
            video_data['url'] = str(video_data['url'])
            video_data['thumbnail'] = str(video_data['thumbnail'])
            json_data.append(video_data)
        
        response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/downloader/audios", json=json_data)
        # response = [{"teste": "teste"}]
        return response.json()

    # def download_video(self, videos: List[schemas.VideoBase]) -> str:
    #     """
    #     Downloads the videos from a video list.
    #     """
    #     json_data = {"videos": videos}
    #     response = requests.post(f"{YOUTUBE_MANAGER_HOST}:{YOUTUBE_MANAGER_PORT}/downloader/videos", json=json_data)
    #     return response.json()

    
    def extract_youtube_id(self, url: str) -> str:
        pattern = r'(?:v=|\/(shorts|watch)\/|\/)([0-9A-Za-z_-]{11})'
        match = re.search(pattern, url)
        return match.group(1) if match else None


youtube_manager = BusinessYoutubeManager()
