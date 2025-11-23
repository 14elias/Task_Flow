from fastapi import HTTPException
from app.schemas.task import CreateTask
from app.models  import project, user, task



def create_task(db, data: dict):
    existing_task = (
        db.query(task.Task)
        .filter(
            task.Task.assigned_to == data.get('assigned_to'),
            task.Task.project_id == data.get('project_id')
        ).first()
    )

    if existing_task:
        raise HTTPException(status_code=400, detail='the task allready assigned to the user')
    

    if not db.query(project.Project).filter(project.Project.id == data.get('project_id')).first():
        raise HTTPException(status_code=404, detail='project not found ')

    if not db.query(user.User).filter(user.User.id == data.get('assigned_to')).first():
        raise HTTPException(status_code=404, detail='user not found ')

    new_task = task.Task(**data)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task