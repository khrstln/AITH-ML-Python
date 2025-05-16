from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class IMessageBroker(ABC):
    @staticmethod
    @abstractmethod
    async def generate_text(
        model_name: str,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
        username: str,
    ) -> Optional[Dict[str, Any]]:
        """Generates text using the provided prompt."""
