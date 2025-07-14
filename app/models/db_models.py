from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    """
    Represents a task in the database.

    Attributes:
        id: Auto-incremented primary key.
        name: Name of the task owner or requestor.
        team: The team responsible for the task.
        description: A brief explanation of the task.
        effort: Estimated effort in Fibonacci units.
        priority: Task priority (low, medium, high).
        updated_at: Timestamp of last update.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    team: str = Field(max_length=50)
    description: str = Field(max_length=500)
    effort: int
    priority: str = Field(max_length=10)
    updated_at: datetime
