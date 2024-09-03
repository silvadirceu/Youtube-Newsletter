from fastapi import UploadFile, File
from typing import Dict, List
from pydantic import BaseModel


# Shared properties
class AudioBase(BaseModel):
    file: UploadFile = File(...)


# Properties to receive via API on creation
class AudioCreate(AudioBase):
    pass


# Properties to receive via Bussiness on creation
class AudioBussinessCreate(AudioBase):
    pass

# Properties to receive via API on update
class AudioUpdate(AudioBase):
    pass

class AudioInDBBase(AudioBase):
    pass
    class Config:
        pass

class TranscriptionSegment(BaseModel):
    start: float
    end: float
    text: str

# Schema principal que inclui a transcrição completa e os segmentos com timestamps
class Audio(BaseModel):
    transcription_with_timestamps: List[TranscriptionSegment]
    full_transcription: str



class AudioInfo(Audio):
    pass
