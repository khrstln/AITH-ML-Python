from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import JSONResponse

from src.web_service.core.repositories.dto import GenerateTextDTO
from src.web_service.core.services.model_service import ModelService
from src.web_service.infrastructure.controllers.dependencies import (
    get_current_user, model_service)

router = APIRouter(
    prefix="/model",
    tags=["Model"],
)


@router.post("/generate_text")
async def generate_text(
    generate_text_dto: GenerateTextDTO,
    model_name: str,
    model_service: Annotated[ModelService, Depends(model_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    try:
        prompt: str = generate_text_dto.prompt
        max_length: int = generate_text_dto.max_length
        temperature: float = generate_text_dto.temperature
        top_k: int = generate_text_dto.top_k
        top_p: float = generate_text_dto.top_p

        generation_result = await model_service.generate_text(
            model_name,
            prompt,
            max_length,
            temperature,
            top_k,
            top_p,
            current_user,
        )
        generated_text = generation_result["text"]
        token_count = generation_result["token_count"]
        new_balance = generation_result["new_balance"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while generation: {e}.")

    return JSONResponse(content={"text": generated_text, "token_count": token_count, "new_balance": new_balance})
