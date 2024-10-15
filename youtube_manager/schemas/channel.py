from fastapi import UploadFile, File
from typing import List, Optional
from pydantic import BaseModel


# Shared properties
class ChannelBase(BaseModel):
    id: Optional[str] = None


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
    ids: Optional[List[str]] = []

class Channels(BaseModel):
    names: List[str]


class ChannelInfo(Channel):
    pass
