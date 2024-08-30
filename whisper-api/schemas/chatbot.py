from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# Shared properties
class ChatbotBase(BaseModel):
    name: Optional[str] = None
    character: str = None
    instructions: str = None
    prompt: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Properties to receive via API on creation
class ChatbotCreate(ChatbotBase):
    pass


# Properties to receive via Bussiness on creation
class ChatbotBussinessCreate(ChatbotBase):
    owner_id: int


# Properties to receive via API on update
class ChatbotUpdate(ChatbotBase):
    prompt: Optional[str] = None


class ChatbotInDBBase(ChatbotBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Chatbot(ChatbotInDBBase):
    pass


class ChatbotInfo(Chatbot):
    pass
