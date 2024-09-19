from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv()


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
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    CHATGPT_MODEL: str = "gpt-3.5-turbo-1106"
    CHATGPT_TEMPERATURE: float = .2

    # DISTIL WHISPER MODEL
    DISTIL_WHISPER_SMALL: str = "distil-whisper/distil-small.en"
    DISTIL_WHISPER_MEDIUM: str = "distil-whisper/distil-medium.en"
    DISTIL_WHISPER_LARGE: str = "distil-whisper/distil-large-v2"
    DEVICE: str = "AUTO"

settings = Settings()
