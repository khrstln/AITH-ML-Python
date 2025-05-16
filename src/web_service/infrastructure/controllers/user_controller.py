import os
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response

from src.web_service.core.repositories.dto import UpdateUserBalanceDTO
from src.web_service.core.services import UserService
from src.web_service.infrastructure.controllers.dependencies import get_current_user, user_service

TOKEN_COOKIE_NAME = os.environ.get("TOKEN_COOKIE_NAME", "")
SECRET_KEY = os.environ.get("SECRET_KEY", "")
ALGORITHM = os.environ.get("ALGORITHM", "")


router = APIRouter(prefix="/user", tags=["User"])


@router.get("/balance")
async def get_balance(
    user_service: Annotated[UserService, Depends(user_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    try:
        user = await user_service.get_user_by_username(current_user)
        return {"username": user.username, "balance": user.balance}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/update_balance")
async def update_balance(
    user: UpdateUserBalanceDTO,
    user_service: Annotated[UserService, Depends(user_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    try:
        updated_user = await user_service.update_user_balance(current_user, user)
        return {"username": current_user, "balance": updated_user.balance}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key=TOKEN_COOKIE_NAME)
    return {"message": "Logged out successfully"}
