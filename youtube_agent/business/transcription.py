from youtube_agent import schemas
from youtube_agent.services.config import settings
from fastapi import UploadFile
from io import BytesIO
import base64
import aiohttp
from aiohttp import FormData

WHISPER_HOST = settings.WHISPER_HOST
WHISPER_PORT = settings.WHISPER_PORT

class BusinessTranscription():
    async def transcribe(self, audio_data: schemas.AudioBytes) -> schemas.Audio:
        """
        Transcribe an audio file to a dict.
        """  

        audio_bytes = base64.b64decode(audio_data.bytes)
        
        form_data = FormData()
        form_data.add_field(
            'obj_in', 
            BytesIO(audio_bytes),  # Audio como BytesIO
            filename='audio.wav',
            content_type='audio/wav'
        )
            
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{WHISPER_HOST}:{WHISPER_PORT}/whisper/transcribe", data=form_data) as response:
                result = await response.json()
                return result     
    

transcriptor = BusinessTranscription()