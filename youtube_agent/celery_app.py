from celery import Celery, chain, group, chord
from services.config import settings
import schemas
from business import youtube_manager
from typing import List
from pydantic import ValidationError


app = Celery("youtube_newsletter", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@app.task(name="extract_metadata_link")
def extract_metadata_link(item: dict):
    """
    """
    print("extracting metadata from video link...")
    item["metadata"] = "metadata"
    return item

@app.task(name="get_audio")
def get_audio(item: dict):
    """
    """
    print("downloading audio from link...")
    item["audio"] = "audio"
    return item

@app.task(name="transcribe_audio")
def transcribe_audio(item: dict):
    """
    """
    print("transcribing audio...")
    item["transcription"] = "transcription"
    return item

@app.task(name="generate_summary")
def generate_summary(item: dict):
    """
    """
    print("generating summary...")
    item["summary"] = "summary"
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


@app.task(name="workflow_all_channels_result")
def workflow_channels_result(results: dict):
    """
    """
    print("passing workflow all channels result...")
    return results


def link_chain_builder(item: dict):
    workflow_link_chain = chain(
        extract_metadata_link.s(item),
        get_audio.s(),
        transcribe_audio.s(),
        generate_summary.s()
    )
    return workflow_link_chain

def workflow_channel(channel: dict):
    group_links = []
    for link in channel["links"]:
        item = {
            "link": link,
            "metadata": None,
            "audio": None,
            "transcription": None,
            "summary": None
        }
        link_chain = link_chain_builder(item)
        group_links.append(link_chain)

    return chord(group(*group_links), join_summaries.s())

def workflow_all_channels(channels: List[dict]):
    group_channels = []

    for channel in channels:
        group_channels.append(workflow_channel(channel))

    return chord(group(*group_channels), join_channels_summaries.s())




# workflow_link = Chain(extract_metadata(), download_audio(), transcript(), summary())

# workflow_channel = chord(Group([workflow_link for link in channel]), join_summaries())
