from core.entities import User
from infrastructure.db.entities import UserEntity
from infrastructure.db.mappers.interfaces import IMapper


class UserMapper(IMapper[User, UserEntity]):
    @staticmethod
    def to_domain(entity: UserEntity) -> User:
        id = int(entity.id)
        username = entity.username
        balance = entity.balance
        hashed_password = entity.hashed_password

        return User(id=id, username=username, balance=balance, hashed_password=hashed_password)

    @staticmethod
    def to_entity(domain: User) -> UserEntity:
        id = int(domain.id)
        username = domain.username
        balance = domain.balance
        hashed_password = domain.hashed_password

        return UserEntity(id=id, username=username, balance=balance, hashed_password=hashed_password)
