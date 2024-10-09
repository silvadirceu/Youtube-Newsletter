from pydantic import RedisDsn
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class RedisSettings(BaseSettings):
    REDIS_SERVER: str = os.getenv('REDIS_SERVER')
    REDIS_PORT: str = os.getenv('REDIS_PORT')
    REDIS_USER: str = os.getenv('REDIS_USER')
    REDIS_PASSWORD: str = os.getenv('REDIS_PASSWORD')
    REDIS_DB: str = os.getenv('REDIS_DB')

    @property
    def REDIS_DATABASE_URI(self) -> str:
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_SERVER}:{self.REDIS_PORT}/{self.REDIS_DB}"

    SHARD_SIZE: int = 314572800  # 300 MB

    class Config:
        case_sensitive = True
        extra = "allow"
