from fastapi import UploadFile
from faster_whisper import WhisperModel
import ffmpeg
import os
from whisper_api import schemas
from typing import Any
from pathlib import Path
from optimum.intel.openvino import OVModelForSpeechSeq2Seq
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, pipeline
from whisper_api.service.config import settings
import librosa
import numpy as np

class BusinessWhisper():
    def __init__(self, model_id):
        self.model_id = model_id
        whisper_api_dir = Path(__file__).resolve().parent.parent
        models_dir = whisper_api_dir / "models"
        models_dir.mkdir(parents=True, exist_ok=True)
        self.model_path = models_dir / self.model_id.replace("/", "_")
        self.ov_config = {"CACHE_DIR": ""}
        self.processor = AutoProcessor.from_pretrained(self.model_id)
        self.pt_model = AutoModelForSpeechSeq2Seq.from_pretrained(self.model_id)
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
        
        self.ov_model.to(settings.DEVICE)
        self.ov_model.compile()
        self.ov_model.generation_config = self.pt_model.generation_config

    def extract_input_features(self, sample: dict):
        input_features = self.processor(
            sample["audio"]["array"],
            sampling_rate=sample["audio"]["sampling_rate"],
            return_tensors="pt",
        ).input_features
        return input_features

    def predict(self, sample):
        pipe = pipeline(
            "automatic-speech-recognition",
            model=self.ov_model,
            tokenizer=self.processor.tokenizer,
            feature_extractor=self.processor.feature_extractor,
            max_new_tokens=128,
            chunk_length_s=15,
            batch_size=16,
        )

        return pipe(sample["audio"].copy(), return_timestamps=True)

    async def transcribe(self, obj_in: UploadFile) -> Any:
        """
        Returns all objects.
        """
        contents = await obj_in.read()
        with open(obj_in.filename, 'wb') as f:
            f.write(contents)
        audio_array, sampling_rate = librosa.load(obj_in.filename, sr=settings.SAMPLING_RATING)
        sample = {
            "audio": {
                "sampling_rate": sampling_rate,
                "array": np.array(audio_array)
            }
        }
        result = self.predict(sample)
        if os.path.exists(obj_in.filename):
            os.remove(obj_in.filename)
        print("\n\n\n", result, "\n\n\n")
        # contents = await obj_in.read()
        # with open(obj_in.filename, 'wb') as f:
        #     f.write(contents)
        # audio_file = open(obj_in.filename, "rb")

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
        # if os.path.exists(obj_in.filename):
        #     os.remove(obj_in.filename)
        # return schemas.Audio(
        #         transcription_with_timestamps=transcription_with_timestamps,
        #         full_transcription=full_transcription
        #     )

    
whisper = BusinessWhisper(settings.DISTIL_WHISPER_SMALL)
