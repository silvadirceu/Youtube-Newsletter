from fastapi import APIRouter, UploadFile
from youtube_manager import schemas, business
from typing import Any, List

router = APIRouter()

 
@router.get("/channels/search", response_model=schemas.Channel)
def search_channel(name: str):
    """
    Searches a channel by name and returns a channel_id.
    """
    return business.youtube_manager.search(name)


@router.get("/channels/{channel_id}/videos", response_model=List[schemas.Video])
def channel_videos(channel_id: str, cutoff_date: str):
    """
    Returns a video_id list from a channel.
    """
    return business.youtube_manager.get_channel_videos(channel_id, cutoff_date)


@router.post("/videos", response_model=List[schemas.VideoBase])
def video_details(video_ids: List[schemas.Video]):
    """
    Returns a list of details from each video.
    """
    return business.youtube_manager.get_video_details(video_ids)

# @router.post("/faster")
# async def transcribe_faster(
#     obj_in: UploadFile,
# ) -> Any:
#     """
#     Transcribe an audio file to a dict. 
    
#     """
#     return await business.audio.transcribe_faster(obj_in)