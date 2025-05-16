from typing import Dict, Optional
from transformers.modeling_utils import PreTrainedModel
from transformers.models.gpt2 import GPT2LMHeadModel, GPT2Tokenizer
from transformers.pipelines import pipeline
from transformers.pipelines.base import Pipeline
from transformers.tokenization_utils import PreTrainedTokenizer
from pathlib import Path

from src.model_service.core.models import IModelHandler


class ModelHandler(IModelHandler):
    def __init__(self, model_path: Path):
        self._model_path = model_path
        self._model: Optional[PreTrainedModel] = None
        self._tokenizer: Optional[PreTrainedTokenizer] = None
        self._generator: Optional[Pipeline] = None

    def load_model(self) -> None:
        self._tokenizer = GPT2Tokenizer.from_pretrained(self._model_path)
        self._model = GPT2LMHeadModel.from_pretrained(self._model_path)
        self._generator = pipeline("text-generation", model=self._model, tokenizer=self._tokenizer, truncation=True)

    def generate_text(
        self,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
        do_sample: bool,
    ) -> Dict[str, str]:

        if self._model is None:
            raise ValueError("The model is not loaded.")

        if self._tokenizer is None:
            raise ValueError("The tokenizer is not loaded.")

        if self._generator is None:
            raise ValueError("The generator is not loaded.")

        prompt_length_in_tokens = self.count_tokens(prompt)

        full_text = self._generator(
            prompt,
            max_length=max_length + prompt_length_in_tokens,
            temperature=temperature,
            do_sample=do_sample,
            top_k=top_k,
            top_p=top_p,
        )

        full_text = full_text[0]["generated_text"]

        prompt_length_in_chars = self._count_chars(prompt)
        trimmed_text = full_text[prompt_length_in_chars:]

        return {"full_text": full_text, "generated_text": trimmed_text}

    def count_tokens(self, input: str) -> int:
        if self._tokenizer is None:
            raise ValueError("The tokenizer is not loaded.")

        return len(self._tokenizer.encode(input, return_tensors="pt")[0])

    def _count_chars(self, input: str) -> int:
        return len(input)
