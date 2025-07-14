from datetime import datetime
from fastapi import HTTPException
from typing import List
from app.models.schemas import TaskCreate
from app.utils.logger import logger

def ensure_no_future_dates(tasks: List[TaskCreate]):
    """
    Validates that no task has a future-dated 'updated_at' timestamp.

    Args:
        tasks (List[TaskCreate]): List of task objects to validate.

    Raises:
        HTTPException (400): If any task has a timestamp set in the future.
    """
    for task in tasks:
        if task.updated_at > datetime.now():
            logger.warning(f"Rejected future timestamp: {task.name} -> {task.updated_at}")
            raise HTTPException(
                status_code=400,
                detail=f"Task '{task.name}' has a future timestamp: {task.updated_at}"
            )

def ensure_no_duplicates_in_file(tasks: List[TaskCreate]):
    """
    Validates that no duplicate tasks exist within the uploaded JSON file.

    A duplicate is defined as a task with the same name, team, and timestamp.

    Args:
        tasks (List[TaskCreate]): List of task objects parsed from JSON.

    Raises:
        HTTPException (400): If a duplicate task is found in the file.
    """
    seen = set()
    for task in tasks:
        key = (task.name, task.team, task.updated_at)
        if key in seen:
            logger.warning(f"In-file duplicate task: {task.name} (team: {task.team}, time: {task.updated_at})")
            raise HTTPException(
                status_code=400,
                detail=f"Duplicate task found in file: {task.name} (team={task.team})"
            )
        seen.add(key)
