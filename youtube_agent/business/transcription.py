from whisper_api import schemas
from ...whisper_api import schemas
from youtube_agent.services.config import settings
import requests
from fastapi import UploadFile
from io import BytesIO
import base64
import httpx

WHISPER_HOST = settings.WHISPER_HOST
WHISPER_PORT = settings.WHISPER_PORT

class BusinessTranscription():
    async def transcribe(self, audio_data: dict) -> schemas.Audio:
        """
        Transcribe an audio file to a dict.
        """  

        audio_bytes = base64.b64decode(audio_data.audio_bytes)
        
        # Criar um UploadFile com o áudio decodificado
        audio_file = UploadFile(
            filename=f"audio.wav",
            file=BytesIO(audio_bytes),
            content_type="audio/wav"
        )
            
        async with httpx.AsyncClient() as client:
            # Abrir o arquivo como se fosse enviado por um formulário multipart
            files = {'obj_in': (audio_file.filename, audio_file.file, audio_file.content_type)}
            
            # Fazer a requisição POST para o endpoint de transcrição
            response = await client.post(f"{WHISPER_HOST}:{WHISPER_PORT}/whisper/transcribe", files=files)
                
        return response.json()
    


transcriptor = BusinessTranscription()