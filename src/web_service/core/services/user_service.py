import os
from typing import List
from src.web_service.core.entities import User
from src.web_service.core.repositories.dto import RegisterUserDTO, CreateUserDTO, UpdateUserBalanceDTO
from src.web_service.core.repositories.i_user_repository import IUserRepository
from src.web_service.core.services.interfaces import IUserService
from passlib.hash import bcrypt
from jose import jwt
from datetime import datetime, timedelta

ACCESS_TOKEN_EXPIRE_DAYS = float(os.environ.get("ACCESS_TOKEN_EXPIRE_DAYS", ""))
SECRET_KEY = os.environ.get("SECRET_KEY", "")
ALGORITHM = os.environ.get("ALGORITHM", "")


class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository):
        self._user_repository = user_repository

    async def register_user(self, user_dto: RegisterUserDTO) -> User:
        hashed_password = bcrypt.hash(user_dto.password)

        create_user_dto = CreateUserDTO(username=user_dto.username, hashed_password=hashed_password)

        new_user: User | None = await self._user_repository.create_user(create_user_dto)
        if new_user is None:
            raise ValueError(f"User with username {user_dto.username} already exists.")

        return new_user

    async def get_user_by_id(self, user_id: int) -> User:
        user: User | None = await self._user_repository.get_user_by_id(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found.")

        return user

    async def get_user_by_username(self, username: str) -> User:
        user: User | None = await self._user_repository.get_user_by_username(username)
        if user is None:
            raise ValueError(f"User with username {username} not found.")

        return user

    async def get_all_users(self) -> List[User]:
        users: List[User] = await self._user_repository.get_all_users()
        return users

    async def update_user_balance(self, username: str, update_balance_dto: UpdateUserBalanceDTO) -> User:
        user: User | None = await self._user_repository.update_user_balance(username, update_balance_dto)
        if user is None:
            raise ValueError(f"User with username {username} not found.")

        return user

    async def authenticate_user(self, username: str, password: str) -> str:
        user: User | None = await self._user_repository.get_user_by_username(username)
        if user is None:
            raise ValueError(f"User with username {username} not found.")

        if not bcrypt.verify(password, user.hashed_password):
            raise ValueError("Invalid password.")

        token_data = {"sub": user.username, "exp": datetime.now() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)}
        token: str = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
        return token
