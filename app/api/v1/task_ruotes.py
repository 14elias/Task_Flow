from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.session import get_db
from app.models import user, task
from app.schemas import task
from app.api import deps
from app.crud import crud_task


router = APIRouter()

@router.post('/task/create', response_model = task.ResponseTask)
def create_task(
    task: task.CreateTask,
    crrent_user: Annotated[user.User,Security(deps.get_current_active_user, scopes=['admin'])],
    db: Session = Depends(get_db)
):
    data = task.model_dump()
    task = crud_task.create_task(db, data)

    return task

@router.get('/task/get_all', response_model = list[task.ResponseTask])
def get_tasks(
    crrent_user: Annotated[user.User,Security(deps.get_current_active_user, scopes=['admin'])],
    db: Session = Depends(get_db)
):
    tasks = crud_task.get_tasks(db)

    return tasks