import os
from typing import Annotated, Optional

from fastapi import Cookie, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from src.web_service.core.services import UserService
from src.web_service.core.services.model_service import ModelService
from src.web_service.infrastructure.db.repositories import UserRepository
from src.web_service.infrastructure.message_brokers import RabbitmqBroker

TOKEN_COOKIE_NAME = os.environ.get("TOKEN_COOKIE_NAME", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")
ALGORITHM = os.environ.get("ALGORITHM", "")

security = HTTPBearer()


async def get_current_user(
    token: Annotated[Optional[HTTPAuthorizationCredentials], Depends(security)] = None,
    cookie_token: Optional[str] = Cookie(default=None, alias=TOKEN_COOKIE_NAME),
) -> str:
    credentials = token.credentials if token else cookie_token
    if not credentials:
        raise HTTPException(status_code=401, detail="Token not provided")

    try:
        payload = jwt.decode(credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token: username not found")
        return username
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token decode error: {e}")


def user_service():
    return UserService(UserRepository)  # type: ignore


def model_service():
    return ModelService(RabbitmqBroker, UserRepository)  # type: ignore
