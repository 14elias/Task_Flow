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


@router.post('/project/create')
async def create_project(
    data: project.ProjectCreate,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    data = data.model_dump()
    data['created_by'] = current_user.id
    data['deadline']  = datetime.now(timezone.utc) +  timedelta(days=10)
    project = await crud_project.create_project(db, data)

    return project


@router.delete('/project/delete')
async def delete_project(
    id:int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    project = await crud_project.delete_project(db, id)

    return project


@router.get('/project/get')
async def get_a_project(
    id:int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    project = await crud_project.get_a_project(db, id)

    return project


@router.get('/project/get_all')
async def get_all_project(
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    project = await crud_project.get_all_project(db)

    return project


@router.patch('/project/update')
async def update_project(
    id:int,
    data:project.ProjectUpdate ,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    data = data.model_dump()
    
    project = await crud_project.update_project(db, id, data)

    return project


@router.post('/project/assign_to_team')
async def project_add_team(
    data:project.ProjectTeam,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    data = data.model_dump()
    project_team = await crud_project.give_project_to_a_team(db, data)

    return project_team


@router.post('/project/remove_from_team')
async def project_remove_team(
    id:int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    project_team = await crud_project.remove_project_from_a_team(db, id)

    return project_team

@router.get('/project/get_teams')
async def get_team_attached_with_project(
    id: int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    project = await crud_project.project_team(db, id)

    return project


@router.get('/project/get_tasks')
async def get_project_tasks(
    id: int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    tasks = await crud_project.get_project_tasks(db, id)

    return tasks