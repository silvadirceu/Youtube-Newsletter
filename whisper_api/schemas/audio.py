from fastapi import UploadFile
from typing import Dict
from pydantic import BaseModel


# Shared properties
class AudioBase(BaseModel):
    file: UploadFile


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

# Additional properties to return via API
class Audio(AudioInDBBase):
    transcription: Dict[str, str]


class AudioInfo(Audio):
    pass
