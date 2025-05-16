from typing import List, Optional

from src.web_service.utils import async_session_maker
from src.web_service.core.repositories.dto import CreateUserDTO, UpdateUserBalanceDTO
from src.web_service.core.repositories.i_user_repository import IUserRepository
from src.web_service.core.entities.user import User
from src.web_service.infrastructure.db.entities import UserEntity
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound


class UserRepository(IUserRepository):
    @staticmethod
    async def create_user(user_dto: CreateUserDTO) -> Optional[User]:
        username = user_dto.username
        if await UserRepository._is_username_taken(username):
            return None

        new_user = UserEntity(username=username, hashed_password=user_dto.hashed_password, balance=0.0)

        async with async_session_maker() as session:
            session.add(new_user)

            await session.commit()
            await session.refresh(new_user)

        return User.model_validate(new_user)

    @staticmethod
    async def get_user_by_id(user_id: int) -> Optional[User]:
        query = select(UserEntity).where(UserEntity.id == user_id)
        async with async_session_maker() as session:
            result = await session.execute(query)

        try:
            user = result.scalar_one()
            return User.model_validate(user)
        except NoResultFound:
            return None

    @staticmethod
    async def get_user_by_username(username: str) -> Optional[User]:
        query = select(UserEntity).where(UserEntity.username == username)
        async with async_session_maker() as session:
            result = await session.execute(query)

        try:
            user = result.scalar_one()
            return User.model_validate(user)
        except NoResultFound:
            return None

    @staticmethod
    async def get_all_users() -> List[User]:
        query = select(UserEntity)
        async with async_session_maker() as session:
            result = await session.execute(query)

        users = result.scalars().all()

        return [User.model_validate(item) for item in users]

    @staticmethod
    async def update_user_balance(username: str, updated_user_balance: UpdateUserBalanceDTO) -> Optional[User]:
        query = select(UserEntity).where(UserEntity.username == username)
        async with async_session_maker() as session:
            result = await session.execute(query)

            try:
                user = result.scalar_one_or_none()
                if not user:
                    return None

                user.balance = user.balance + updated_user_balance.amount  # type: ignore

                await session.commit()
                await session.refresh(user)

                return User.model_validate(user)
            except NoResultFound:
                return None

    @staticmethod
    async def _is_username_taken(username: str) -> bool:
        query = select(UserEntity).where(UserEntity.username == username)
        async with async_session_maker() as session:
            result = await session.execute(query)

        return result.scalar_one_or_none() is not None
