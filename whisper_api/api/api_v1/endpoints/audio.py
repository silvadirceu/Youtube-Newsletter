from fastapi import APIRouter, UploadFile
from whisper_api import schemas, business
from typing import Any

router = APIRouter()


@router.post("/", response_model=schemas.Audio)
async def transcribe(
    obj_in: UploadFile,
) -> schemas.Audio:
    """
    Transcribe an audio file to a dict. 
    
    """
    return await business.whisper.transcribe(obj_in)
