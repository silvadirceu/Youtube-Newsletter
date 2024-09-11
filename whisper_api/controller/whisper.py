# adapted from https://stackoverflow.com/a/22171182

import numpy as np
from sklearn.preprocessing import normalize
from inference_client.client import InferenceClient


class WhisperController:
    def __init__(self, inference_server: InferenceClient, params=None):
        self.params = params
        self.whisper_client = inference_server
        self.batchsize = params["batchsize"]

    async def inference_request(self, data, model_version=0):
        response = await self.cqtnet_client.predict([data], model_version)
        return response[0]

    async def predict(self, data, model_version=0):
        n = data.shape[0]
        features = []

        if self.batchsize == -1:
            vectors = await self.inference_request(data, model_version)
            features.extend(vectors)

        else:
            batch, rem = divmod(n, self.batchsize)
            # print("Running {:d} Batches ".format(batch))

            for i in range(batch):
                # print("Running Batch {:d}".format(i))
                start = i * self.batchsize
                end = start + self.batchsize
                input_data = data[start:end, ...]

                vectors = await self.inference_request(input_data, model_version)
                features.extend(vectors)

            if rem > 0:
                input_data = data[batch * self.batchsize :, ...]
                vectors = await self.inference_request(input_data, model_version)

                features.extend(vectors)

        return features

    async def process(
        self, cqt: np.ndarray, is_query: bool, is_segmenter: bool, model_version=0
    ):
        if is_query:
            transform_frame = cqt_models_set_transform_frames_isquery
            transform_all_data = cqt_models_set_transform_all_audio_isquery
        else:
            transform_frame = cqt_models_set_transform_frames
            transform_all_data = cqt_models_set_transform_all_audio

        if not is_segmenter:
            new_data = transform_frame.transform(cqt)
            # tensorflow --> batch, height, width, channels - transpose(1, 2, 3, 0)
            # pytorch -->  batch, channels, height, width - transpose(1, 0, 2, 3)
            new_data = new_data[None, :].transpose(1, 0, 2, 3)
            features = await self.predict(new_data, model_version)

        if not is_query or is_segmenter:
            new_data = transform_all_data.transform(cqt)
            new_data = new_data[None, :].transpose(1, 0, 2, 3)
            features2 = await self.predict(new_data, model_version)

            features.extend(features2)
        return normalize(features, norm="l2")