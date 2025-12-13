from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.models.user import User
from app.schemas import user, project, team
from app.api import deps
from app.crud import crud_team
from app.db.session import get_db

router = APIRouter()
 
@router.post("/team/create", response_model = team.ResponseTeam, status_code = 201)
async def creat_team(
    team: team.TeamCreat,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    team = team.model_dump()
    team['created_by'] = current_user.id
    team = await crud_team.creat_team(db, team)

    return team


@router.get('/team/get/all', response_model = list[team.ResponseTeam])
async def get_team(
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    teams = await crud_team.get_all_team(db)

    return teams


@router.get('/team/get', response_model = team.ResponseTeam)
async def get_team(
    id:int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    teams = await crud_team.get_a_team(db,id)

    return teams

@router.get('/team/delete', response_model = team.ResponseTeam)
async def get_team(
    id:int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    teams = await crud_team.delete_team(db,id)

    return teams


@router.patch('/team/update', response_model = team.ResponseTeam)
async def get_team(
    id:int,
    data: team.TeamCreat,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    data = data.model_dump()
    teams = await crud_team.update_team(db, id, data)

    return teams


@router.post("/team/add/member", status_code = 201, response_model = team.ResponseTeamMember)
async def creat_team(
    team_member_data: team.CreateTeamMember,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    team_member_data = team_member_data.model_dump()
    new_member = await crud_team.add_member(db, team_member_data)

    return new_member


@router.post("/team/remove/member", response_model = team.ResponseTeamMember)
async def creat_team(
    id: int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    new_member = await crud_team.remove_member(db, id)

    return new_member

@router.get('/team/get/members', response_model = list[user.User])
async def get_team(
    id:int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    team_members = await crud_team.get_team_members(db, id)

    return team_members


@router.get('/team/get/projects', response_model=list[project.ProjectResponse])
async def get_projects(
    id: int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    team_projects = await crud_team.get_team_projects(db, id)

    return team_projects