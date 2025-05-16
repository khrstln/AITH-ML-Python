from pydantic import BaseModel, ConfigDict, Field


class RegisterUserDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(..., max_length=100)
    password: str = Field(..., min_length=1, max_length=30)
