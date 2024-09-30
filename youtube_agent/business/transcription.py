from whisper_api import schemas
from ...whisper_api import schemas
from youtube_agent.services.config import settings
import requests

WHISPER_HOST = settings.WHISPER_HOST
WHISPER_PORT = settings.WHISPER_PORT

class BusinessTranscription():
    async def transcribe(self, path: str) -> schemas.Audio:
        """
        Transcribe an audio file to a dict.
        """
        file = {"obj_in": open(path, 'rb')}
        response = requests.post(f"{WHISPER_HOST}:{WHISPER_PORT}/whisper/transcribe", files=file)
        return response.json()
    


transcriptor = BusinessTranscription()