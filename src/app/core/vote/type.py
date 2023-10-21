from pydantic import BaseModel, Field


class OldVoteOption(BaseModel):
    label: str
    emoji: str
    current: int = Field(default=0, ge=0)
