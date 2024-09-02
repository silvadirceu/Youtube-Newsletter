from typing import Any, Dict, List, Optional

from pydantic import EmailStr, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        env_file=('.env', '.env.prod'),
        extra='ignore'
    )

    # Project and API version
    PROJECT_NAME: str = "Whisper API"
    PROJECT_DESCRIPTION: str = "API to transcribe audio to text using Whisper Model"
    API_PROXY_STR: str = ""
    ROOT_PATH: str = ""
    
    # CHATGPT API
    CHATGPT_API_KEY: str = ""
    CHATGPT_MODEL: str = "gpt-3.5-turbo-1106"
    CHATGPT_TEMPERATURE: float = .2


settings = Settings()
