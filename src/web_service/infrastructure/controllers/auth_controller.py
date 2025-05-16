import os
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from src.web_service.core.repositories.dto import LoginUserDTO, RegisterUserDTO
from src.web_service.core.services import UserService
from src.web_service.infrastructure.controllers.dependencies import \
    user_service

TOKEN_COOKIE_NAME = os.environ.get("TOKEN_COOKIE_NAME", "")

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
async def register_user(user: RegisterUserDTO, user_service: Annotated[UserService, Depends(user_service)]):
    try:
        await user_service.get_user_by_username(user.username)
    except Exception:
        registered_user = await user_service.register_user(user)
        user_info = {"username": registered_user.username, "balance": registered_user.balance}
        return JSONResponse(content=user_info, status_code=201)

    raise HTTPException(status_code=400, detail="User already exists")


@router.post("/login")
async def login_user(
    user: LoginUserDTO,
    user_service: Annotated[UserService, Depends(user_service)],
):
    try:
        token = await user_service.authenticate_user(user.username, user.password)
        return {"access_token": token, "username": user.username, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
