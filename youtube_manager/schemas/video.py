from typing import List, Optional
from pydantic import BaseModel, HttpUrl


# Shared properties
class VideoBase(BaseModel):
    id: str
    title: str
    description: Optional[str]
    publishedAt: str
    thumbnail: str
    channelTitle: str
    duration: str
    viewCount: Optional[int]
    likeCount: Optional[int]
    commentCount: Optional[int]
    url: str
    audio_bytes: Optional[str] = None


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
