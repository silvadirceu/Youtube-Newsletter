from abc import ABC, abstractmethod
from numpy import ndarray


class InferenceClient(ABC):
    @abstractmethod
    async def predict(input_data: list[ndarray], model_version=0) -> list[ndarray]: ...