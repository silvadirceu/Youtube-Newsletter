from celery import Celery
from services.config import settings

app = Celery("youtube_newsletter", broker=settings.REDIS_URL, backend=settings.REDIS_URL)


# from youtube_agent.celery_app import app
from celery import chord
import schemas
from business import youtube_manager
from typing import List
from pydantic import ValidationError


@app.task(name="process_item")
def process_item(item: str):
    """
    Identifies if the item is a channel name or a video link, and processes accordingly.
    """
    try:
        # Valida se o item é um link de YouTube
        schemas.YouTubeLink(url=item)
        # Se for um link de vídeo
        return handle_video_link(item)
    except ValidationError:
        # Caso contrário, assume ser um nome de canal
        return handle_channel(item)

@app.task(name="handle_channel")
def handle_channel(channel_name: str):
    """
    Processes a channel name by searching for the channel and downloading audio.
    """
    channel = youtube_manager.search([channel_name])
    videos = youtube_manager.get_channel_videos(channel['channel_id'], '2023-01-01')
    video_details = youtube_manager.get_video_details([video['id'] for video in videos])
    return youtube_manager.download_audio(video_details)

@app.task(name="handle_video_link")
def extract_metadata(video_link: str):
    """
    Processes a video link by directly downloading the audio.
    """
    video_id = youtube_manager.extract_youtube_id(video_link)
    video_details = youtube_manager.get_video_details([video_id])
    return video_details


@app.task(name="handle_video_link")
def download_audio(video_details: List[schemas.VideoBase]):
    """
    Processes a video link by directly downloading the audio.
    """
    return youtube_manager.download_audio(video_details)


workflow_link = Chain(extract_metadata(), download_audio(), transcript(), summary())

workflow_channel = chord(Group([workflow_link for link in channel]), join_summaries())






































@app.task(name="finalize")
def finalize(results):
    """
    Final task that runs when all tasks are complete.
    """
    return "All tasks completed successfully!"


@app.task(name="workflow")
def workflow(items: List[str]):
    """
    Orchestrates the entire workflow using a chord.
    """
    task_group = [process_item.s(item) for item in items]
    workflow = chord(task_group)(finalize.s())
    return workflow



link -> extracao de dados -> transcrição 