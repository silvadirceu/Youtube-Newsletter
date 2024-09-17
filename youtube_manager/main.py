from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from youtube_manager.api.api_v1.api import api_router
from youtube_manager.service.config import settings

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="0.0.1",
    openapi_url=f"{settings.API_PROXY_STR}/openapi.json",
    root_path=settings.ROOT_PATH,
    middleware=middleware,
)

app.include_router(api_router)
