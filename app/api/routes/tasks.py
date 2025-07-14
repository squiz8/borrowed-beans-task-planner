from fastapi import APIRouter, UploadFile, File, Body, HTTPException, Query
from typing import List, Optional
from app.models.schemas import TaskCreate, TaskRead
from app.core.db import get_session
from app.models.db_models import Task
from app.validators.task_validators import ensure_no_future_dates, ensure_no_duplicates_in_file
from app.services.task_service import check_duplicate_in_db, insert_task
from app.utils.logger import logger
import json


router = APIRouter()

@router.post("/")
def create_single_task(task: TaskCreate = Body(...)):
    """
    Accepts a single task from the request body (form or JSON).

    - Validates timestamp is not in the future.
    - Ensures no duplicate task exists in the DB.
    - Logs creation process.
    """
    logger.info(f"Single task submitted: {task.name} (team: {task.team})")

    # Timestamp must not be in the future
    ensure_no_future_dates([task])

    # Ensure the task does not already exist in the DB
    session = get_session()
    check_duplicate_in_db(session, task)

    # Insert the task and confirm insertion
    created = insert_task(session, task)
    logger.info(f"Task inserted: {created.name} (id: {created.id})")

    return created
    
    


@router.post("/file", response_model=List[TaskRead])
def create_tasks_from_file(file: UploadFile = File(...)):
    """
    Accepts a JSON file containing a list of tasks.

    - Parses and validates the uploaded JSON
    - Checks for:
      - JSON format errors
      - Internal duplicates within the file
      - Future timestamps
      - Duplicates against existing DB records
    - Saves valid tasks to the database

    Returns:
        List of successfully created tasks
    """
    try:
        content = file.file.read()
        parsed = json.loads(content)

        if not isinstance(parsed, list):
            raise ValueError("Uploaded file must contain a list of tasks")
        
        # Validate structure with Pydantic
        validated = [TaskCreate(**item) for item in parsed]
        logger.info(f"JSON file upload received with {len(validated)} tasks")

    except json.JSONDecodeError:
        logger.warning("Failed to parse uploaded JSON file")
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        logger.warning(f"Task upload failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


    # App-level validations
    ensure_no_duplicates_in_file(validated)
    ensure_no_future_dates(validated)

    # Save each task, checking DB for duplicates
    session = get_session()
    created = []

    for task in validated:
        check_duplicate_in_db(session, task)
        created.append(insert_task(session, task))

    logger.info(f"{len(created)} tasks successfully stored from file")
    return created


@router.get("/filtered")
def get_tasks_by_team(team: Optional[str] = Query(None)):
    """
    Retrieves all tasks, with optional filtering by team.

    - If a team is specified via query string (`?team=Grinders`), only tasks for that team are returned
    - Otherwise, returns all tasks

    Returns:
        List of matching tasks
    """
    session = get_session()

    if team:
        logger.info(f"Filtering tasks by team: {team}")
        tasks = session.query(Task).filter(Task.team == team).all()
    else:
        tasks = session.query(Task).all()
        logger.info(f"Fetching all tasks ({len(tasks)} found)")
    return tasks

