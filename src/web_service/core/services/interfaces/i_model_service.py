from abc import ABC, abstractmethod
from typing import Dict


class IModelService(ABC):
    @abstractmethod
    async def generate_text(
        self,
        model_name: str,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
        do_sample: bool,
        username: str,
    ) -> Dict[str, str]:
        """
        Text generation based on the provided initial text (prompt) and parameters.

        :param model_name (str): name of the model
        :param prompt (str): User-provided text.
        :param max_length (int): Maximum length of the generated text.
        :param temperature (float): Controls the diversity of the output.
        :param top_k (int): If greater than 0, limits the word selection to the k most probable words.
        :param top_p (float): If less than 1.0, applies nucleus sampling.
        :param do_sample (bool): If True, enables random sampling to increase diversity.
        :param username: username in db who called the method
        :return: A dictionary containing the generated text and related metadata (e.g., token count).
        """
