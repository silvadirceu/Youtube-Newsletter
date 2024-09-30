from fastapi import APIRouter, UploadFile
from youtube_manager import schemas, business
from typing import Any, List

router = APIRouter()

 
@router.post("/audios", response_model=str)
async def download_audios(videos: List[schemas.VideoBase]):
    """
    Downloads the audios from a video list.
    """
    return await business.youtube_manager.download_audio(videos)


@router.post("/videos", response_model=str)
async def download_videos(videos: List[schemas.VideoBase]):
    """
    Downloads the videos from a video list.
    """
    return await business.youtube_manager.download_video(videos)