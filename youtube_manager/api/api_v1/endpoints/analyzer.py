from fastapi import APIRouter, UploadFile
from youtube_manager import schemas, business
from typing import Any

router = APIRouter()

 
@router.get("/channels/search", response_model=schemas.Audio)
def search_channel(name: str):
    """
    Searches a channel by name and returns a channel_id.
    """
    return business.audio.transcribe(obj_in)


# @router.post("/faster")
# async def transcribe_faster(
#     obj_in: UploadFile,
# ) -> Any:
#     """
#     Transcribe an audio file to a dict. 
    
#     """
#     return await business.audio.transcribe_faster(obj_in)