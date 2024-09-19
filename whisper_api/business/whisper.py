from fastapi import UploadFile
from faster_whisper import WhisperModel
import ffmpeg
import os
from whisper_api import schemas
from typing import Any
from pathlib import Path
from optimum.intel.openvino import OVModelForSpeechSeq2Seq
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
from whisper_api.service.config import settings

class BusinessWhisper():
    def __init__(self, model_id):
        self.model_id = model_id
        self.model_path = Path(model_id.replace("/", "_"))
        self.ov_config = {"CACHE_DIR": ""}
        self.processor = AutoProcessor.from_pretrained(model_id.value)
        self.pt_model = AutoModelForSpeechSeq2Seq.from_pretrained(model_id.value)
        self.ov_model = None
        self.pt_model.eval();

        if not self.model_path.exists():
            self.ov_model = OVModelForSpeechSeq2Seq.from_pretrained(
                self.model_id,
                ov_config=self.ov_config,
                export=True,
                compile=False,
                load_in_8bit=False,
            )
            self.ov_model.half()
            self.ov_model.save_pretrained(self.model_path)
        else:
            self.ov_model = OVModelForSpeechSeq2Seq.from_pretrained(self.model_path, ov_config=self.ov_config, compile=False)

    async def transcribe(self, obj_in: UploadFile) -> schemas.Audio:
        """
        Returns all objects.
        """
        contents = await obj_in.read()
        with open(obj_in.filename, 'wb') as f:
            f.write(contents)
        audio_file = open(obj_in.filename, "rb")

        segments, _ = self.whisper_model.transcribe(audio_file,
                                                                    word_timestamps=True, 
                                                                    language="pt")
        
        transcription_with_timestamps = []
        full_transcription = "" 

        time_interval = 10
        current_start_time = None
        current_end_time = None
        current_text = []

        for segment in segments:
            for word in segment.words:
                if current_start_time is None:
                    current_start_time = word.start
                    current_end_time = current_start_time + time_interval  

                if word.start <= current_end_time:
                    current_text.append(word.word)
                else:
                    text_segment = " ".join(current_text)
                    transcription_with_timestamps.append({
                        "start": current_start_time,
                        "end": current_end_time,
                        "text": text_segment
                    })
                    
                    full_transcription += text_segment + " "

                    current_start_time = word.start
                    current_end_time = current_start_time + time_interval
                    current_text = [word.word]

        if current_text:
            text_segment = " ".join(current_text)
            transcription_with_timestamps.append({
                "start": current_start_time,
                "end": current_end_time,
                "text": text_segment
            })
            full_transcription += text_segment + " "

        full_transcription = full_transcription.strip()
        if os.path.exists(obj_in.filename):
            os.remove(obj_in.filename)
        return schemas.Audio(
                transcription_with_timestamps=transcription_with_timestamps,
                full_transcription=full_transcription
            )


    async def transcribe_faster(self, obj_in: UploadFile) -> Any:
        """
        Returns all objects.
        """
        contents = await obj_in.read()
        with open(obj_in.filename, 'wb') as f:
            f.write(contents)
        audio_file = open(obj_in.filename, "rb")

        # segments, _ = self.whisper_model.transcribe(audio_file,
        #                                                             word_timestamps=True, 
        #                                                             language="pt")
        
        # transcription_with_timestamps = []
        # full_transcription = "" 

        # time_interval = 10
        # current_start_time = None
        # current_end_time = None
        # current_text = []

        # for segment in segments:
        #     for word in segment.words:
        #         if current_start_time is None:
        #             current_start_time = word.start
        #             current_end_time = current_start_time + time_interval  

        #         if word.start <= current_end_time:
        #             current_text.append(word.word)
        #         else:
        #             text_segment = " ".join(current_text)
        #             transcription_with_timestamps.append({
        #                 "start": current_start_time,
        #                 "end": current_end_time,
        #                 "text": text_segment
        #             })
                    
        #             full_transcription += text_segment + " "

        #             current_start_time = word.start
        #             current_end_time = current_start_time + time_interval
        #             current_text = [word.word]

        # if current_text:
        #     text_segment = " ".join(current_text)
        #     transcription_with_timestamps.append({
        #         "start": current_start_time,
        #         "end": current_end_time,
        #         "text": text_segment
        #     })
        #     full_transcription += text_segment + " "

        # full_transcription = full_transcription.strip()

        # return schemas.Audio(
        #         transcription_with_timestamps=transcription_with_timestamps,
        #         full_transcription=full_transcription
        #     )
    
audio = BusinessWhisper(settings.DISTIL_WHISPER_SMALL)
