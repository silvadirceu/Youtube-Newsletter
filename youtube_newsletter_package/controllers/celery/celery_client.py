from celery import Celery
from ..settings import Settings


class CeleryClient:
    """
    Initializes the Celery application with the loaded settings.
    """

    def __init__(self, name: str) -> Celery:
        settings = Settings()
        self.app = Celery(
            name,
            broker=settings.RABBITMQ_URI,
            backend=settings.REDIS_DATABASE_URI,
        )
        celery_conf = {
            "broker_url": str(settings.RABBITMQ_URI),
            "result_backend": f"{str(settings.REDIS_DATABASE_URI)}",
            "enable_utc": settings.CELERY_ENABLE_UTC,
            "task_serializer": settings.CELERY_TASK_SERIALIZER,
            "result_serializer": settings.CELERY_RESULT_SERIALIZER,
            "accept_content": settings.CELERY_ACCEPT_CONTENT,
            "result_extended": settings.CELERY_RESULT_EXTENDED,
            "namespace": settings.CELERY_NAMESPACE,
            "broker_connection_retry_on_startup": True,
        }
        self.app.conf.update(celery_conf)
