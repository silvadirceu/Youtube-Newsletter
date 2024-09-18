from fastapi import UploadFile
from faster_whisper import WhisperModel
import ffmpeg
import os
from whisper_api import schemas
from typing import Any


class BusinessAudio():
    def __init__(self, model):
        self.whisper_model = model

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
    

model = WhisperModel("small", 
                    compute_type="int8", 
                    cpu_threads=os.cpu_count(), 
                    num_workers=os.cpu_count())

audio = BusinessAudio(model)