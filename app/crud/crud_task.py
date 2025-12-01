from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import task, project, user
from app.schemas.task import CreateTask



async def create_task(db: AsyncSession, data: dict):
    # Check if project exists
    result = await db.execute(
        select(project.Project).where(project.Project.id == data.get("project_id"))
    )
    existing_project = result.scalar_one_or_none()
    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Optional: check if assigned_to exists
    if data.get("assigned_to"):
        result = await db.execute(
            select(user.User).where(user.User.id == data.get("assigned_to"))
        )
        assigned_user = result.scalar_one_or_none()
        if not assigned_user:
            raise HTTPException(status_code=404, detail="Assigned user not found")

    new_task = task.Task(**data)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    return new_task



async def get_tasks(db: AsyncSession):
    result = await db.execute(select(task.Task))
    tasks = result.scalars().all()
    return tasks  # empty list is fine; no need to raise 404



async def assign_task(db: AsyncSession, data: dict):
    result = await db.execute(select(task.Task).where(task.Task.id == data.get("task_id")))
    existing_task = result.scalar_one_or_none()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    
    result = await db.execute(select(user.User).where(user.User.id == data.get("assigned_to")))
    existing_user = result.scalar_one_or_none()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    
    project_team_ids = [pt.team_id for pt in existing_task.project.teams]
    user_team_ids = [ut.team_id for ut in existing_user.teams]

    if not any(tid in project_team_ids for tid in user_team_ids):
        raise HTTPException(
            status_code=400,
            detail="User is not a member of any team assigned to this project"
        )

    existing_task.assigned_to = data.get("assigned_to")
    await db.commit()
    await db.refresh(existing_task)

    return existing_task



async def unassign_task(db: AsyncSession, data: dict):
    result = await db.execute(select(task.Task).where(task.Task.id == data.get("task_id")))
    existing_task = result.scalar_one_or_none()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.assigned_to = None
    await db.commit()
    await db.refresh(existing_task)

    return existing_task



async def update_task(db: AsyncSession, data: dict, id: int):
    result = await db.execute(select(task.Task).where(task.Task.id == id))
    existing_task = result.scalar_one_or_none()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    for field, value in data.items():
        setattr(existing_task, field, value)

    await db.commit()
    await db.refresh(existing_task)

    return existing_task



async def get_tasks_based_status(db: AsyncSession, status: str, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(task.Task).where(task.Task.status == status).offset(skip).limit(limit)
    )
    tasks = result.scalars().all()
    return tasks  



async def delete_task(db: AsyncSession, id: int):
    result = await db.execute(select(task.Task).where(task.Task.id == id))
    existing_task = result.scalar_one_or_none()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    await db.delete(existing_task)
    await db.commit()

    return existing_task
