from fastapi import HTTPException
from app.schemas.task import CreateTask
from app.models  import project, user, task



def create_task(db, data: dict):
    # existing_task = (
    #     db.query(task.Task)
    #     .filter(
    #         task.Task.assigned_to == data.get('assigned_to'),
    #         task.Task.project_id == data.get('project_id')
    #     ).first()
    # )

    # if existing_task:
    #     raise HTTPException(status_code=400, detail='the task allready assigned to the user')
    

    if not db.query(project.Project).filter(project.Project.id == data.get('project_id')).first():
        raise HTTPException(status_code=404, detail='project not found ')

    # if not db.query(user.User).filter(user.User.id == data.get('assigned_to')).first():
    #     raise HTTPException(status_code=404, detail='user not found ')

    

    new_task = task.Task(**data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_tasks(db):
    tasks = db.query(task.Task).all()

    if not tasks :
        raise HTTPException(status_code=404, detail= "tasks not found")

    return tasks


def assign_task(db, data):
    existing_task = (
        db.query(task.Task)
        .filter(task.Task.id == data.get('task_id'))
        .first()
    )

    if not existing_task:
        raise HTTPException(status_code=404, detail='task not found')

    project_team_ids = [pt.team_id for pt in existing_task.project.teams]

    existing_user = (
        db.query(user.User)
        .filter(user.User.id == data.get('assigned_to'))
        .first()
    )

    if not existing_user:
        raise HTTPException(status_code=404, detail='user not found')
    
    user_team_ids = [ut.team_id for ut in existing_user.teams]

    if not any(tid in project_team_ids for tid in user_team_ids):
        raise HTTPException(
            status_code=400,
            detail="User is not a member of any team assigned to this project"
        )

    existing_task.assigned_to = data.get('assigned_to')

    db.commit()
    db.refresh(existing_task)

    return existing_task


def unassign_task(db, data):
    existing_task = (
        db.query(task.Task)
        .filter(task.Task.id == data.get('task_id'))
        .first()
    )

    if not existing_task:
        raise HTTPException(status_code=404, detail='task not found')
    
    existing_task.assigned_to = None

    db.commit()
    db.refresh(existing_task)

    return existing_task


def update_task(db, data, id):
    existing_task = (
        db.query(task.Task)
        .filter(task.Task.id == id)
        .first()
    )

    if not existing_task:
        raise HTTPException(status_code=404, detail='task not found')
    
    for field, value in data.items():
        setattr(existing_task, field, value)

    db.commit()
    db.refresh(existing_task)

    return existing_task


def get_tasks_based_status(db, status, skip: int = 0, limit: int = 100):
    tasks = db.query(task.Task).filter(task.Task.status == status).all()

    if not tasks :
        raise HTTPException(status_code=404, detail= "tasks not found")

    return tasks


def delete_task(db, id):
    existing_task = db.query(task.Task).filter(task.Task.id == id).first()

    if not existing_task:
        raise HTTPException(status_code=404, detail='there is no task with this id')
    
    db.delete(existing_task)
    db.commit()

    return existing_task