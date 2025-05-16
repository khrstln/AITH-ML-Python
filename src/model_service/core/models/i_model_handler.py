from abc import ABC, abstractmethod
from typing import Dict


class IModelHandler(ABC):
    @abstractmethod
    def load_model(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
        do_sample: bool,
    ) -> Dict[str, str]:
        """
        Text generation based on the provided initial text (prompt) and parameters.

        Parameters:
            - prompt (str): User-provided text.
            - max_length (int): Maximum length of the generated text.
            - temperature (float): Controls the diversity of the output.
            - top_k (int): If greater than 0, limits the word selection to the k most probable words.
            - top_p (float): If less than 1.0, applies nucleus sampling.
            - do_sample (bool): If True, enables random sampling to increase diversity.

        Returns:
            dict: A dictionary containing the generated text and related metadata (e.g., token count).
        """
        raise NotImplementedError()

    @abstractmethod
    def count_tokens(self, input: str) -> int:
        raise NotImplementedError()

    @abstractmethod
    def _count_chars(self, input: str) -> int:
        raise NotImplementedError()
