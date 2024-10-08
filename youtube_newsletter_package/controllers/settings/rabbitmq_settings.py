from typing import Optional, Dict, Any
from pydantic import AmqpDsn, field_validator
from pydantic_settings import BaseSettings


class RabbitMQSettings(BaseSettings):
    RABBITMQ_SERVER: str = ""
    RABBITMQ_PORT: str = ""
    RABBITMQ_USER: str = ""
    RABBITMQ_PASSWORD: str = ""
    RABBITMQ_VHOST: str = ""

    @property
    def RABBITMQ_URI(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_SERVER}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"

    class Config:
        case_sensitive = True
        extra = "allow"
