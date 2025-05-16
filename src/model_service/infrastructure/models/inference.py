from pathlib import Path
from typing import Dict

from src.model_service.core.models import IInference
from src.model_service.infrastructure.models.model_handler import ModelHandler


class Inference(IInference):
    _MODEL_PATHS = {
        "rugpt3small_based_on_gpt2": Path(__file__).parents[4].resolve() / "models_sources/rugpt3small_based_on_gpt2"
    }

    def __init__(self):
        self._models_nadlers = {name: ModelHandler(path) for name, path in self._MODEL_PATHS.items()}

        for model_handler in self._models_nadlers.values():
            model_handler.load_model()

    def generate_text(
        self,
        model_name: str,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
    ) -> Dict[str, str | int]:
        do_sample = True
        model_output = self._models_nadlers[model_name].generate_text(
            prompt,
            max_length,
            temperature,
            top_k,
            top_p,
            do_sample,
        )

        full_text: str = model_output["full_text"]
        generated_text: str = model_output["generated_text"]

        token_count = self._models_nadlers[model_name].count_tokens(generated_text)
        return {"text": full_text, "token_count": token_count}
