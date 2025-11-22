from fastapi import HTTPException
from app.schemas import project
from app.models.project import Project, ProjectTeam

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
        raise HTTPException(status_code=400, detail="project not exist ")

    db.delete(existing_project)
    db.commit()

    return existing_project


def get_a_project(db, id: int):
    existing_project = db.query(Project).filter(Project.id == id).first()

    if not existing_project:
        raise HTTPException(status_code=400, detail="project not exist ")
    
    return existing_project


def get_all_project(db):
    existing_project = db.query(Project).all()
    if not existing_project:
        raise HTTPException(status_code=400, detail="project not exist ")
    
    return existing_project


def update_project(db, id: int, data:dict):
    existing_project = db.query(Project).filter(Project.id == id).first()

    if not existing_project:
        raise HTTPException(status_code=400, detail="project not exist ")

    if data.get('description'):
        existing_project.description = data.get('description')
    if data.get('title'):
        existing_project.title = data.get('title')

    db.commit()
    db.refresh(existing_project)

    return existing_project
