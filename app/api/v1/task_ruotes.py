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


@router.patch('/task/assign', response_model=task.ResponseTask)
def assign_task(
    data: task.AssignTask,
    crrent_user: Annotated[user.User,Security(deps.get_current_active_user, scopes=['admin'])],
    db: Session = Depends(get_db)
):
    data = data.model_dump()
    assign_task = crud_task.assign_task(db,data)

    return assign_task



@router.patch('/task/unassign', response_model=task.ResponseTask)
def unassign_task(
    data: task.UnAssignTask,
    crrent_user: Annotated[user.User,Security(deps.get_current_active_user, scopes=['admin'])],
    db: Session = Depends(get_db)
):
    data = data.model_dump()
    assign_task = crud_task.assign_task(db,data)

    return assign_task


@router.patch('/task/update', response_model=task.ResponseTask)
def update_task(
    id: int,
    data: task.UpdateTask,
    crrent_user: Annotated[user.User,Security(deps.get_current_active_user, scopes=['admin'])],
    db: Session = Depends(get_db)
):
    data = data.model_dump(exclude_unset=True)
    assign_task = crud_task.update_task(db, data, id)

    return assign_task


@router.get('/task/get_by_status', response_model = list[task.ResponseTask])
def get_tasks_based_status(
     crrent_user: Annotated[user.User,Security(deps.get_current_active_user, scopes=['admin'])],
    status,
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_db)
):
    tasks = crud_task.get_tasks_based_status(db, status, skip, limit)

    return tasks


@router.delete('/task/delete', response_model = task.ResponseTask)
def delete_task(
    id: int,
    crrent_user: Annotated[user.User,Security(deps.get_current_active_user, scopes=['admin'])],
    db: Session = Depends(get_db)
):
    task = crud_task.delete_task(db, id)

    return task