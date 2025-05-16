from abc import ABC, abstractmethod
from typing import List

from src.web_service.core.entities import User
from src.web_service.core.repositories.dto import (RegisterUserDTO,
                                                   UpdateUserBalanceDTO)


class IUserService(ABC):
    @abstractmethod
    async def register_user(self, user_dto: RegisterUserDTO) -> User:
        """
        Registers a new user in the system
        :param user_dto: information about the user to be created
        :return: created user
        """

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> User:
        """
        Returns a user by its id
        :param user_id: id of the user to be returned, positive integer
        :return: found user
        """

    @abstractmethod
    async def get_user_by_username(self, username: str) -> User:
        """
        Returns a user by its username
        :param username: username of the user to be returned
        :return: found user
        """

    @abstractmethod
    async def get_all_users(self) -> List[User]:
        """
        Returns a list of all users
        :return: list of users with filtering and pagination
        """

    @abstractmethod
    async def update_user_balance(self, username: str, update_balance_dto: UpdateUserBalanceDTO) -> User:
        """
        Updates an existing item in the system partially
        :param username: username of the user to be updated, positive integer
        :param update_balance_dto: information about the user to be updated
        :return: updated user
        """
