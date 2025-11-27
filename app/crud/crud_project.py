from fastapi import HTTPException
from app.schemas import project
from app.models.project import Project, ProjectTeam
from app.models.team import Team

def create_project(db, project: dict):
    existing_project = db.query(Project).filter(Project.title == project.get('title')).first()

    if existing_project:
        raise HTTPException(status_code=400, detail="project already created ")
    new_project = Project(**project)

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


def delete_project(db, id: int):
    existing_project = db.query(Project).filter(Project.id == id).first()

    if not existing_project:
        raise HTTPException(status_code=404, detail="project not exist ")

    db.delete(existing_project)
    db.commit()

    return existing_project


def get_a_project(db, id: int):
    existing_project = db.query(Project).filter(Project.id == id).first()

    if not existing_project:
        raise HTTPException(status_code=404, detail="project not exist ")
    
    return existing_project


def get_all_project(db):
    existing_project = db.query(Project).all()
    if not existing_project:
        raise HTTPException(status_code=404, detail="project not exist ")
    
    return existing_project


def update_project(db, id: int, data:dict):
    existing_project = db.query(Project).filter(Project.id == id).first()

    if not existing_project:
        raise HTTPException(status_code=404, detail="project not exist ")

    if data.get('description'):
        existing_project.description = data.get('description')
    if data.get('title'):
        existing_project.title = data.get('title')

    db.commit()
    db.refresh(existing_project)

    return existing_project

def give_project_to_a_team(db, data: dict):
    existing_project_team = (
        db.query(ProjectTeam)
        .filter(
            ProjectTeam.project_id == data.get('project_id'), 
            ProjectTeam.team_id == data.get('team_id')
        )
    ).first()

    if existing_project_team:
        raise HTTPException(status_code=400, detail="project already given to the team ")
    
    if not db.query(Project).filter(Project.id == data.get('project_id')):
        raise HTTPException(status_code=404, detail="project not found")
    
    if not db.query(Team).filter(Team.id == data.get('team_id')):
        raise HTTPException(status_code=404, detail="team not found")

    new_project_team = ProjectTeam(**data)

    db.add(new_project_team)
    db.commit()
    db.refresh(new_project_team)

    return new_project_team



def remove_project_from_a_team(db, id: int):
    existing_project_team = (
        db.query(ProjectTeam)
        .filter(
            ProjectTeam.id == id 
        )
    ).first()

    if not existing_project_team:
        raise HTTPException(status_code=404, detail="project_team not found")

    db.delete(existing_project_team)
    db.commit()

    return existing_project_team


def project_team(db, id):
    existing_project = db.query(Project).filter(Project.id == id).first()

    if not existing_project:
        raise HTTPException(status_code=404, detail="project not exist ")
    
    teams = existing_project.teams

    return teams


def get_project_tasks(db,id):
     existing_project = db.query(Project).filter(Project.id == id).first()

     if not existing_project:
        raise HTTPException(status_code=404, detail="project not exist ")
     
     tasks = existing_project.tasks

     return tasks