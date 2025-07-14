import pytest
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.validators.task_validators import ensure_no_future_dates, ensure_no_duplicates_in_file
from app.models.schemas import TaskCreate

# Helper: Create a valid TaskCreate object
def make_task(name="Task", team="Grinders", updated_at=None):
    return TaskCreate(
        name=name,
        team=team,
        description="desc",
        effort=3,
        priority="medium",
        updated_timestamp=updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )


def test_no_future_dates_valid():
    """Should pass when all tasks have valid timestamps."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks = [make_task(name="ValidTask", updated_at=now)]
    ensure_no_future_dates(tasks)


def test_no_future_dates_raises():
    """Should raise HTTPException when a task has a future timestamp."""
    future = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
    tasks = [make_task(name="FutureTask", updated_at=future)]

    with pytest.raises(HTTPException) as exc:
        ensure_no_future_dates(tasks)
    assert exc.value.status_code == 400
    assert "future timestamp" in exc.value.detail


def test_no_duplicates_in_file_valid():
    """Should pass when all tasks in file are unique."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks = [
        make_task(name="A", updated_at=now),
        make_task(name="B", updated_at=now),
    ]
    ensure_no_duplicates_in_file(tasks)


def test_duplicates_in_file_raises():
    """Should raise HTTPException when duplicate tasks exist in file."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task1 = make_task(name="A", updated_at=now)
    task2 = make_task(name="A", updated_at=now)
    tasks = [task1, task2]

    with pytest.raises(HTTPException) as exc:
        ensure_no_duplicates_in_file(tasks)
    assert exc.value.status_code == 400
    assert "duplicate task" in exc.value.detail.lower()
