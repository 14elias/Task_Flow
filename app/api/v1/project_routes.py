from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, timedelta, timezone

from app.schemas import project
from app.models import user
from app.api import deps
from app.db.session import get_db
from app.crud import crud_project


router = APIRouter()


@router.post('/create/project')
def create_project(
    data: project.ProjectCreate,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    data = data.model_dump()
    data['created_by'] = current_user.id
    data['deadline']  = datetime.now(timezone.utc) +  timedelta(days=10)
    project = crud_project.create_project(db, project = data)

    return project


@router.delete('/delete/project')
def delete_project(
    id:int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    project = crud_project.delete_project(db, id)

    return project


@router.get('/get/project')
def get_a_project(
    id:int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    project = crud_project.get_a_project(db, id)

    return project


@router.get('/get/all_project')
def get_all_project(
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    project = crud_project.get_all_project(db)

    return project


@router.patch('/update/project')
def get_all_project(
    id:int,
    data:project.ProjectUpdate ,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    data = data.model_dump()
    
    project = crud_project.update_project(db, id, data)

    return project