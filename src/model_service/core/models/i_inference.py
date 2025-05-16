from abc import ABC, abstractmethod
from typing import Dict


class IInference(ABC):
    @abstractmethod
    def generate_text(
        self,
        model_name: str,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
    ) -> Dict[str, str | int]:
        raise NotImplementedError()
