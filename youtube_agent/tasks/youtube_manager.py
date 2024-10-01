from celery import shared_task, chord
from ...youtube_manager import schemas
from business import youtube_manager
from typing import List
from pydantic import ValidationError


@shared_task
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

@shared_task
def handle_channel(channel_name: str):
    """
    Processes a channel name by searching for the channel and downloading audio.
    """
    channel = youtube_manager.search([channel_name])
    videos = youtube_manager.get_channel_videos(channel['channel_id'], '2023-01-01')
    video_details = youtube_manager.get_video_details([video['id'] for video in videos])
    return youtube_manager.download_audio(video_details)

@shared_task
def handle_video_link(video_link: str):
    """
    Processes a video link by directly downloading the audio.
    """
    video_id = youtube_manager.extract_youtube_id(video_link)
    video_details = youtube_manager.get_video_details([video_id])
    return youtube_manager.download_audio(video_details)

@shared_task
def finalize(results):
    """
    Final task that runs when all tasks are complete.
    """
    return "All tasks completed successfully!"

@shared_task
def extract_video_id_from_link(link: str) -> str:
    """
    Extracts video ID from a YouTube link.
    """
    # Extrai o ID do vídeo de um link YouTube
    return link.split('v=')[1] if 'v=' in link else link.split('/')[-1]

def workflow(items: List[str]):
    """
    Orchestrates the entire workflow using a chord.
    """
    task_group = [process_item.s(item) for item in items]
    workflow = chord(task_group)(finalize.s())
    return workflow
