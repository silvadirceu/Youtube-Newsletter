from fastapi import APIRouter

from whisper_api.api.api_v1.endpoints import transcribe

api_router = APIRouter()
api_router.include_router(transcribe.router, prefix="/transcribe", tags=["Transcribe"])

