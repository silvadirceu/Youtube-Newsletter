from fastapi import UploadFile, File
from typing import List, Optional
from pydantic import BaseModel


# Shared properties
class VideoBase(BaseModel):
    id: Optional[str] = None


# Properties to receive via API on creation
class VideoCreate(VideoBase):
    pass


# Properties to receive via Bussiness on creation
class VideoBussinessCreate(VideoBase):
    pass

# Properties to receive via API on update
class VideoUpdate(VideoBase):
    pass

class VideoInDBBase(VideoBase):
    pass
    class Config:
        pass


class Video(BaseModel):
    id: Optional[str] = None



class VideoInfo(Video):
    pass
