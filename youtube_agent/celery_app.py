from celery import Celery
from youtube_agent.services.config import settings

app = Celery("youtube_newsletter", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

# Importa as tasks após a definição do app para evitar problemas de importação circular
import youtube_agent.tasks
