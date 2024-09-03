from fastapi import APIRouter

from whisper_api.api.api_v1.endpoints import audio

api_router = APIRouter()
api_router.include_router(audio.router, prefix="/audio", tags=["Audio"])

