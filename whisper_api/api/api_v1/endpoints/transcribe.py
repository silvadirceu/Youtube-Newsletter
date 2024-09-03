from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session

from whisper_api import schemas, business

router = APIRouter()


@router.post("/")
async def transcribe(
    obj_in: UploadFile,
) -> Any:
    """
    Transcribe an audio file to a dict. 
    The dict contains the following structure:
    
    """
    return await business.audio.transcribe(obj_in)