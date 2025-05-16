from sqlalchemy import Column, Float, Integer, String

from src.web_service.utils import Base


class UserEntity(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    balance = Column(Float, nullable=False, default=0.0)
    hashed_password = Column(String, nullable=False)
