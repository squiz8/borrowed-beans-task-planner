from pydantic import BaseModel, field_validator, Field
from typing import Literal
from datetime import datetime
from app.utils.fibonacci import generate_fibonacci_up_to
from app.core.config import MAX_EFFORT


class TaskCreate(BaseModel):
    """
    Schema for creating a task via API input.

    - Accepts form or JSON data.
    - Validates effort against the Fibonacci sequence.
    - Validates accepted teams and priority values.
    - Uses `updated_timestamp` as alias for `updated_at`.
    """
    name: str
    team: Literal["Grinders", "Bean Selectors", "Taste Testers", "Finance"]
    description: str
    effort: int
    priority: Literal["low", "medium", "high"]
    updated_at: datetime = Field(alias="updated_timestamp", example="2025-07-13 23:33:58")

    @field_validator("effort")
    @classmethod
    def validate_effort(cls, v):
        allowed_efforts = generate_fibonacci_up_to(MAX_EFFORT)
        if v not in allowed_efforts:
            raise ValueError(f"Effort must be a Fibonacci number up to 100: {allowed_efforts}")
        return v


class TaskRead(BaseModel):
    """
    Schema for task output responses (returned by API).

    Includes all task fields, including auto-generated ID.
    """
    id: int
    name: str
    team: str
    description: str
    effort: int
    priority: str
    updated_at: datetime