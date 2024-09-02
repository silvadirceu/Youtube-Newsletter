from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from whisper_api import schemas, business

router = APIRouter()


@router.post("/", response_model=schemas.Chatbot)
def transcribe(
    obj_in: schemas.AudioBase,
) -> schemas.Audio:
    """
    Transcribe an audio file to a dict. 
    The dict contains the following structure:
    
    """
    return business.audio.transcribe(obj_in)