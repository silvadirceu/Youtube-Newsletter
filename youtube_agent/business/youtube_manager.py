from typing import List
from ...youtube_manager import schemas
from ...youtube_manager.business import youtube_manager

class BusinessYoutubeManager():

    def search(self, name: str) -> schemas.Channel:
        """
        Searches a channel by name and returns a channel_id.
        """
        return youtube_manager.search(name)


    def get_channel_videos(self, channel_id: str, start_date: str, end_date: str = None) -> List[schemas.Video]:
        """
        Returns a video list from a channel within a specified date range.
        """
        return youtube_manager.get_channel_videos(channel_id, start_date, end_date)


    
    def get_video_details(self, video_ids: List[schemas.Video]) -> List[schemas.VideoBase]:
        """
        Returns a list of details from each video.
        """
        return youtube_manager.get_video_details(video_ids)

    
    async def download_audio(self, videos: List[schemas.VideoBase]) -> str:
        """
        Downloads the audios from a video list.
        """
        return youtube_manager.download_audio(videos)



    async def download_video(self, videos: List[schemas.VideoBase]) -> str:
        """
        Downloads the videos from a video list.
        """
        return youtube_manager.download_video(videos)


youtube_manager = BusinessYoutubeManager()
