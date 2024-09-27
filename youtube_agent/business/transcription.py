from fastapi import UploadFile
from faster_whisper import WhisperModel
import ffmpeg
import os
from whisper_api import schemas
from typing import Any
from ...whisper_api import schemas
from ...whisper_api.business import whisper

class BusinessTranscription():
    async def transcribe(self, obj_in: UploadFile) -> schemas.Audio:
        """
        Transcribe an audio file to a dict.
        """
        return whisper.transcribe(obj_in)
    


transcriptor = BusinessTranscription()