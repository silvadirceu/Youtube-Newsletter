from fastapi import APIRouter, UploadFile
from youtube_manager import schemas, business
from typing import Any, List

router = APIRouter()

 
@router.post("/audios", response_model=str)
def download_audios(videos: List[schemas.VideoBase]):
    """
    Downloads the audios from a video list.
    """
    return business.youtube_manager.download_audio(videos)