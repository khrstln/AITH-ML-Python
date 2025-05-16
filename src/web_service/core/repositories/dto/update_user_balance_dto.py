from pydantic import BaseModel, ConfigDict, Field


class UpdateUserBalanceDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(...)
    amount: float = Field(...)
