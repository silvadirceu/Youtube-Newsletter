from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from whisper_api import schemas, business

router = APIRouter()


@router.post("/", response_model=schemas.Audio)
async def transcribe(
    obj_in: UploadFile,
) -> schemas.Audio:
    """
    Transcribe an audio file to a dict. 
    
    """
    return await business.audio.transcribe(obj_in)