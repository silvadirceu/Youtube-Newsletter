import asyncio
import logging
from numpy import ndarray
from inference_client.openvino.params import ModelName
from inference_client.client import InferenceClient
from ovmsclient import make_grpc_client, ModelServerError

logger = logging.getLogger(__name__)


class OpenVinoClient(InferenceClient):
    def __init__(self, url: str, model_name: ModelName):
        logger.info(
            f"Connecting to OpenVino server {url}"
        )
        self.client = make_grpc_client(url)
        self.model_name = model_name
        try:
            self.metadata = self.client.get_model_metadata(model_name)
        except:
            logger.error(f"The OpenVino Server for {model_name} is not running.")
            raise

    async def predict(self, input_data: list[ndarray], model_version=0):
        inputs_meta = self.metadata["inputs"]
        inputs = {}

        for i, (k, _) in enumerate(inputs_meta.items()):
            inputs[k] = input_data[i]

        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, self.client.predict, inputs, self.model_name, model_version, 60)
        # response = self.client.predict(inputs=inputs, model_name=self.model_name, model_version=model_version)

        if isinstance(response, ndarray):
            return [response]

        formated_response = [value for _, value in response.items()]
        formated_response.reverse()

        return formated_response