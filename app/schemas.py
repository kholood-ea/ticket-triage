from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Channel(str, Enum):
    app = "app"
    web = "web"
    email = "email"
    call_center = "call_center"
    chat = "chat"


class TicketIn(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    channel: Channel
    metadata: dict[str, Any] | None = None

    @field_validator("text")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("text must not be blank")
        return v


class TicketOut(BaseModel):
    id: int
    text: str
    channel: Channel
    metadata: dict[str, Any] | None = None
    category: str | None = None  # filled by the classifier on Day 4
    priority: str | None = None
    created_at: str


class CategoryCount(BaseModel):
    category: str
    n: int
