from sqlmodel import Session
from fastapi import HTTPException
from typing import List
from app.models.schemas import TaskCreate
from app.models.db_models import Task
from app.utils.logger import logger

def check_duplicate_in_db(session: Session, task: TaskCreate):
    """
    Check if a task with the same name, team, and timestamp already exists in the database.

    Args:
        session (Session): SQLModel database session.
        task (TaskCreate): Task input object to check for duplication.

    Raises:
        HTTPException (409): If a duplicate task is found in the database.
    """
    existing = session.query(Task).filter_by(
        name=task.name,
        team=task.team,
        updated_at=task.updated_at
    ).first()

    if existing:
        logger.warning(f"Duplicate found in DB: {task.name} (team: {task.team})")
        raise HTTPException(
            status_code=409,
            detail=f"Duplicate task in DB: {task.name} (team={task.team})"
        )

def insert_task(session: Session, task: TaskCreate) -> Task:
    """
    Insert a new task into the database after validation.

    Args:
        session (Session): SQLModel database session.
        task (TaskCreate): Validated task input data.

    Returns:
        Task: The task object after insertion (with generated ID).
    """
    task_db = Task(**task.model_dump())
    session.add(task_db)
    session.commit()
    session.refresh(task_db)
    logger.info(f"Inserted task into DB: {task_db.name} (id: {task_db.id})")
    return task_db
