from pydantic import BaseModel, ConfigDict, Field


class CreateUserDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(..., max_length=100)
    hashed_password: str = Field(...)
