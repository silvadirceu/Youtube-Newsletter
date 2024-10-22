from typing import List, Optional
from pydantic import BaseModel
from youtube_agent.schemas import Video

# Shared properties
class ChannelBase(BaseModel):
    id: str = ""
    title: str = ""
    videos: List[Video]

# Properties to receive via API on creation
class ChannelCreate(ChannelBase):
    pass


# Properties to receive via Bussiness on creation
class ChannelBussinessCreate(ChannelBase):
    pass

# Properties to receive via API on update
class ChannelUpdate(ChannelBase):
    pass

class ChannelInDBBase(ChannelBase):
    pass
    class Config:
        pass


class Channel(BaseModel):
    id: Optional[str] = None

class Channels(BaseModel):
    names: List[str]


class ChannelInfo(Channel):
    pass