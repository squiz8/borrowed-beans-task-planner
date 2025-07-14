from fastapi import APIRouter, Query, HTTPException
from sqlmodel import select
from app.core.db import get_session
from app.models.db_models import Task
from app.utils.knapsack import knapsack
from typing import List
from app.models.schemas import TaskRead
from app.utils.logger import logger

router = APIRouter()

@router.get("/", response_model=List[TaskRead])
def allocate_tasks(effort: int = Query(..., gt=0)):
    """
    Allocates tasks optimally based on available effort points using a 0/1 Knapsack approach.

    - `effort`: The total number of effort points available for the week. Must be greater than 0.
    - Returns a list of allocated tasks sorted by priority and updated timestamp.
    """
    
    # Get DB session and fetch all available tasks
    session = get_session()
    tasks = session.exec(select(Task)).all()

    if not tasks:
        logger.warning("Allocation requested, but no tasks available")
        raise HTTPException(status_code=404, detail="No tasks available")

    logger.info(f"Allocating with max effort = {effort} across {len(tasks)} tasks")

    # Apply the Knapsack algorithm to select best-fit tasks
    selected = knapsack(tasks, effort)

    logger.info(f"{len(selected)} tasks allocated: {[t.name for t in selected]}")
    
    return selected
