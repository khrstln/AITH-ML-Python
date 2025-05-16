from abc import ABC, abstractmethod
from typing import List, Optional

from src.web_service.core.entities.user import User
from src.web_service.core.repositories.dto import CreateUserDTO, UpdateUserBalanceDTO


class IUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user_dto: CreateUserDTO) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        raise NotImplementedError()

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        raise NotImplementedError()

    @abstractmethod
    async def update_user_balance(self, username: str, top_up_user_balance: UpdateUserBalanceDTO) -> Optional[User]:
        raise NotImplementedError()
