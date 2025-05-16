from pydantic import BaseModel, ConfigDict, Field


class GenerateTextDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(...)
    max_length: int = Field(100, gt=0)
    temperature: float = Field(0.5, gt=0)
    top_k: int = Field(10, gt=0)
    top_p: float = Field(0.95, gt=0, le=1)
