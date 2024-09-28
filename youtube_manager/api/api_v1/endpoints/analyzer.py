from fastapi import APIRouter
from youtube_manager import schemas, business
from typing import Any, List

router = APIRouter()

 
@router.post("/channels/search", response_model=schemas.Channel)
def search_channel(names: List[str]):
    """
    Searches a channel by name and returns a channel_id.
    """
    return business.youtube_manager.search(names)


@router.get("/channels/{channel_id}/videos", response_model=List[schemas.Video])
def channel_videos(channel_id: str, start_date: str, end_date: str = None):
    """
    Returns a video list from a channel within a specified date range.
    """
    return business.youtube_manager.get_channel_videos(channel_id, start_date, end_date)


@router.post("/videos", response_model=List[schemas.VideoBase])
def video_details(video_ids: List[schemas.Video]):
    """
    Returns a list of details from each video.
    """
    return business.youtube_manager.get_video_details(video_ids)

