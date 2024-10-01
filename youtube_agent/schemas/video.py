from typing import List, Optional
from pydantic import BaseModel, HttpUrl, FieldValidationInfo, ValidationError, field_validator


# Shared properties
class VideoBase(BaseModel):
    id: str
    title: str
    description: Optional[str]
    publishedAt: str
    thumbnail: HttpUrl
    channelTitle: str
    duration: str
    viewCount: Optional[int]
    likeCount: Optional[int]
    commentCount: Optional[int]
    url: HttpUrl


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

class YouTubeLink(BaseModel):
    url: HttpUrl

    @field_validator('url')
    def validate_youtube_link(cls, v: str, info: FieldValidationInfo):
        if "youtube.com" not in v and "youtu.be" not in v:
            raise ValueError('Not a valid YouTube link')
        return v
    