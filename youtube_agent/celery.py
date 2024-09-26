from celery import Celery
import youtube_agent.service.config as config

app = Celery("tasks", broker=config.REDIS_URL, backend=config.REDIS_URL)