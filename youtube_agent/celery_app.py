from celery import Celery, chain, group, chord
from youtube_agent.services.config import settings
from youtube_agent.services.clients import get_redis
from youtube_agent import schemas
from youtube_agent.business import youtube_manager
from youtube_agent.business import transcriptor
from youtube_agent.business import summarizer
from typing import List
import asyncio

app = Celery("youtube_newsletter", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

def run_async_in_sync(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()

@app.task(name="extract_video_metadata")
def extract_video_metadata(item: dict):
    """
    Extract a metadata dict from a video id.
    """
    print("extracting metadata from video...")
    metadata = run_async_in_sync(youtube_manager.get_video_details([schemas.Video(id=item["id"])]))
    print("\n\n\n\n\n\n\nMETADATA: ", metadata, "\n\n\n\n\n\n\n")
    item["metadata"] = metadata[0]
    return item

@app.task(name="get_audio")
def get_audio(item: dict):
    """
    """
    print("downloading audio from link...")
    audio = youtube_manager.download_audio([schemas.VideoBase(**item["metadata"])])
    redis = get_redis()
    key = redis.set_data(audio[0])
    print("\n\n\nkey: ", key, "\n\n\n")
    item["audio"] = key
    return item

@app.task(name="transcribe_audio")
def transcribe_audio(item: dict):
    """
    """
    print("transcribing audio...")
    redis = get_redis()
    audio_data = redis.get_data(item["audio"])
    # loop = asyncio.get_event_loop()
    # transcription = loop.run_until_complete(transcriptor.transcribe(schemas.AudioBytes(bytes=audio_data["bytes"])))
    # loop.close()
    transcription = run_async_in_sync(transcriptor.transcribe(schemas.AudioBytes(bytes=audio_data["bytes"])))
    redis.delete_data(item["audio"])
    item["transcription"] = transcription
    return item



@app.task(name="generate_summary")
def generate_summary(item: dict):
    """
    """
    print("generating summary...")
    summary = run_async_in_sync(summarizer.summarize_video(schemas.VideoBase(**item["metadata"]), item["transcription"]))
    print("\n\n\n", summary, "\n\n\n")
    item["summary"] = summary
    return item

@app.task(name="join_summaries")
def join_summaries(results: List[dict]):
    """
    Join all the summaries from the processed videos
    """
    print("joining summaries...")
    combined_summary = "\n\n".join([item["summary"] for item in results if item.get("summary")])
    return {"combined_summary": combined_summary}

@app.task(name="join_channels_summaries")
def join_channels_summaries(results: List[dict]):
    """
    Join all the summaries from all channels
    """
    print("joining channels summaries...")
    channels_summaries = []
    for channel in results:
        channels_summaries.append(channel)
    return channels_summaries


def video_chain_builder(item: dict):
    workflow_video_chain = chain(
        extract_video_metadata.s(item),
        get_audio.s(),
        transcribe_audio.s(),
        generate_summary.s()
    )
    return workflow_video_chain

def workflow_channel(channel: schemas.ChannelBase):
    """Create a workflow for processing all videos in a channel."""
    group_videos = []
    for video in channel.videos:
        item = {
            "id": video.id,
            "link": video.link,
            "metadata": None,
            "audio": None,
            "transcription": None,
            "summary": None
        }
        video_chain = video_chain_builder(item)
        group_videos.append(video_chain)

    return chord(group(*group_videos), join_summaries.s())

def workflow_all_channels(channels: List[schemas.ChannelBase]):
    group_channels = []

    for channel in channels:
        group_channels.append(workflow_channel(channel))

    return chord(group(*group_channels), join_channels_summaries.s())
    # return "teste"