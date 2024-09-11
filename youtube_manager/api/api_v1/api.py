from fastapi import APIRouter

from youtube_manager.api.api_v1.endpoints import analyzer

api_router = APIRouter()
api_router.include_router(analyzer.router, prefix="/analyzer", tags=["Analyzer"])

