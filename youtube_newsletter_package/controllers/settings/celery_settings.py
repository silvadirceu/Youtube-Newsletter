from typing import List
from pydantic_settings import BaseSettings


class CelerySettings(BaseSettings):
    WORKER_TAG: str = "1.0b"
    WORKER_VERSION: str = WORKER_TAG
    CELERY_NAMESPACE: str = "CELERY"
    CELERY_WORKER_NAME: str = ""
    CELERY_BROKER: str = ""
    CELERY_BACKEND: str = ""
    CELERY_ENABLE_UTC: bool = False
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: List = ["json", "msgpack"]
    CELERY_RESULT_EXTENDED: bool = True

    class Config:
        case_sensitive = True
        extra = "allow"
