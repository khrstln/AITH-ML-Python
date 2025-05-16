import json
from pathlib import Path
from typing import Dict

from src.web_service.core.message_brokers.i_message_broker import \
    IMessageBroker
from src.web_service.core.repositories import IUserRepository
from src.web_service.core.repositories.dto import UpdateUserBalanceDTO
from src.web_service.core.services.interfaces import IModelService


class ModelService(IModelService):
    MODELS_CONFIG_PATH = Path(__file__).parents[4] / "configs/models.json"

    def __init__(
        self,
        message_broker: IMessageBroker,
        user_repository: IUserRepository,
    ):
        self._user_repository = user_repository
        self._message_broker = message_broker

        with open(self.MODELS_CONFIG_PATH, encoding="utf-8") as f:
            self._models_registry: Dict[str, float] = json.load(f)

    async def generate_text(
        self,
        model_name: str,
        prompt: str,
        max_length: int,
        temperature: float,
        top_k: int,
        top_p: float,
        username: str,
    ) -> Dict[str, str]:
        if self._models_registry.get(model_name) is None:
            raise ValueError(f"Model {model_name} not found.")

        model_token_cost: float = self._models_registry[model_name]
        user = await self._user_repository.get_user_by_username(username)
        if user is None:
            raise ValueError("User not found")

        if user.balance < model_token_cost * max_length:
            raise ValueError("Insufficient balance")

        await self._user_repository.update_user_balance(
            username,
            UpdateUserBalanceDTO(username=username, amount=-model_token_cost * max_length),
        )

        response = await self._message_broker.generate_text(
            model_name,
            prompt,
            max_length,
            temperature,
            top_k,
            top_p,
            username,
        )

        if response is None:
            raise ValueError("Error while generate")

        response["new_balance"] = user.balance - response["token_count"] * model_token_cost

        return response
