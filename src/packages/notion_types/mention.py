from typing import Literal

from pydantic import UUID4, BaseModel


class DatabaseMentionDatabase(BaseModel):
    id: UUID4

    model_config = {"frozen": True}


class DatabaseMention(BaseModel):
    type: Literal["database"]
    database: DatabaseMentionDatabase

    model_config = {"frozen": True}


class DateMentionDate(BaseModel):
    pass


class DateMention(BaseModel):
    type: Literal["date"]
