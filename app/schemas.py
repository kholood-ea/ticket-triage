from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Channel(str, Enum):
    app = "app"
    web = "web"
    email = "email"
    call_center = "call_center"
    chat = "chat"


class Category(str, Enum):
    billing_charges = "billing_charges"
    payment_failure = "payment_failure"
    account_access = "account_access"
    service_outage = "service_outage"
    technical_issue = "technical_issue"
    security_fraud = "security_fraud"
    request_information = "request_information"
    other_unclear = "other_unclear"


class Priority(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


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
    category: Category | str | None = None  # filled by the classifier on Day 4
    priority: Priority | str | None = None
    created_at: str


class CategoryCount(BaseModel):
    category: str
    n: int
