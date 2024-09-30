from celery import Celery
from youtube_agent.services.config import settings

app = Celery("tasks", broker=settings.REDIS_URL, backend=settings.REDIS_URL)