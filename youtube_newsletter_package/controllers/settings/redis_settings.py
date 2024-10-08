from pydantic import RedisDsn
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    REDIS_SERVER: str = ""
    REDIS_PORT: str = ""
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_DB: str = "0"

    @property
    def REDIS_DATABASE_URI(self) -> str:
        return f"redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_SERVER}:{self.REDIS_PORT}/{self.REDIS_DB}"

    SHARD_SIZE: int = 314572800  # 300 MB

    class Config:
        case_sensitive = True
        extra = "allow"
