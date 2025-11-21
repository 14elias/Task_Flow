from fastapi import HTTPException
from app.schemas import team
from app.models.team import Team, TeamMember

def creat_team(db, team: team.TeamCreat):
    team = db.query(Team).filter(Team.name == team.get('name')).first()

    if team:
        raise HTTPException(status_code=400, detail="Team already registered")
    team = Team(**team)

    db.add(team)
    db.commit()
    db.refresh(team)

    return team

def get_all_team(db):
    return db.query(Team).all()

def get_a_team(db, id):
    team = db.query(Team).filter(Team.id == id).first()

    return team

def delete_team(db, id):
    team = db.query(Team).filter(Team.id == id).first()

    db.delete(team)
    db.commit()

    return team


def update_team(db, id: int, data: dict):
    team = db.query(Team).filter(Team.id == id).first()
    if not team:
        return None
    
    team = db.query(Team).filter(Team.id == id).first()
    if data.get('name'):
        team.name = data.get('name')
    if data.get('description'):
        team.description = data.get('description')

    db.commit()
    db.refresh(team)

    return team


def add_member(db, team_member_data: dict):
    existing_member = (
        db.query(TeamMember)
        .filter(
            TeamMember.team_id == team_member_data.get('team_id'),
            TeamMember.user_id == team_member_data.get('user_id')
        )
        .first()
    )

    if existing_member:
        raise HTTPException(status_code=400, detail="user already added")
    
    new_member = TeamMember(**team_member_data)

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


def remove_member(db, id: int):
    existing_member = db.query(TeamMember).filter(TeamMember.id == id).first()
    
    if not existing_member:
        raise HTTPException(status_code=404, detail="User not found in the team")
    
    db.delete(existing_member)
    db.commit()

    return existing_member

def get_team_members(db, id):
    team_members = db.query(Team).filter(Team.id == id).first()

    users = [member.user for member in team_members.members]
    return users


