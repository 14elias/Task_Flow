from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.models.user import User
from app.schemas.team import ResponseTeam, TeamCreat, CreateTeamMember, ResponseTeamMember
from app.schemas.user import User
from app.api import deps
from app.crud import crud_team
from app.db.session import get_db

router = APIRouter()
 
@router.post("/creat/team", response_model = ResponseTeam, status_code = 201)
def creat_team(
    team: TeamCreat,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    team = team.model_dump()
    team['created_by'] = current_user.id
    team = crud_team.creat_team(db, team)

    return team


@router.get('/get_all_team', response_model = list[ResponseTeam])
def get_team(
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    teams =crud_team.get_all_team(db)

    return teams


@router.get('/get_a_team', response_model = ResponseTeam)
def get_team(
    id:int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    teams =crud_team.get_a_team(db,id)

    return teams

@router.get('/delete_a_team', response_model = ResponseTeam)
def get_team(
    id:int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    teams =crud_team.delete_team(db,id)

    return teams


@router.patch('/update_a_team', response_model = ResponseTeam)
def get_team(
    id:int,
    data: TeamCreat,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    
    data = data.model_dump()
    teams =crud_team.update_team(db, id, data)

    return teams


@router.post("/team/add_member", status_code = 201, response_model = ResponseTeamMember)
def creat_team(
    team_member_data: CreateTeamMember,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    team_member_data = team_member_data.model_dump()
    new_member = crud_team.add_member(db, team_member_data)

    return new_member


@router.post("/team/remove_member", response_model = ResponseTeamMember)
def creat_team(
    id: int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    new_member = crud_team.remove_member(db, id)

    return new_member

@router.get('/get_team_members', response_model = list[User])
def get_team(
    id:int,
    current_user: Annotated[User, Security(deps.get_current_active_user, scopes=["admin"])],
    db: Session = Depends(get_db)
):
    team_members =crud_team.get_team_members(db, id)

    return team_members