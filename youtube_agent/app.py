from celery import Celery
from services.config import settings

app = Celery("youtube_newsletter", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

app.autodiscover_tasks()
