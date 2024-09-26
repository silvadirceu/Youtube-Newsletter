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
    PROJECT_NAME: str = "Youtube Agent API"
    PROJECT_DESCRIPTION: str = "This project manages the creation of newsletters from YouTube videos, acting as an AI agent that perceives the environment, processes data, and takes action to send periodic summaries to users, optimizing the information flow."
    API_PROXY_STR: str = ""
    ROOT_PATH: str = ""
    
    # CHATGPT API
    # OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY')
    CHATGPT_MODEL: str = "gpt-3.5-turbo-1106"
    CHATGPT_TEMPERATURE: float = .2


settings = Settings()
