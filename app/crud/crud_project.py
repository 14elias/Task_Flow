from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project, ProjectTeam
from app.models.team import Team



async def create_project(db: AsyncSession, project_data: dict):
    result = await db.execute(select(Project).where(Project.title == project_data.get("title")))
    existing_project = result.scalar_one_or_none()

    if existing_project:
        raise HTTPException(status_code=400, detail="Project already created")

    new_project = Project(**project_data)
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project



async def delete_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    existing_project = result.scalar_one_or_none()

    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not exist")

    await db.delete(existing_project)
    await db.commit()
    return existing_project



async def get_a_project(db: AsyncSession, project_id: int):
    result = await db.execute(select(Project).where(Project.id == project_id))
    existing_project = result.scalar_one_or_none()

    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not exist")
    
    return existing_project



async def get_all_project(db: AsyncSession):
    result = await db.execute(select(Project))
    projects = result.scalars().all()
    return projects



async def update_project(db: AsyncSession, id: int, data: dict):
    result = await db.execute(select(Project).where(Project.id == id))
    existing_project = result.scalar_one_or_none()

    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not exist")

    if data.get('description'):
        existing_project.description = data['description']
    if data.get('title'):
        existing_project.title = data['title']

    await db.commit()
    await db.refresh(existing_project)
    return existing_project



async def give_project_to_a_team(db: AsyncSession, data: dict):
    result = await db.execute(
        select(ProjectTeam).where(
            ProjectTeam.project_id == data.get('project_id'),
            ProjectTeam.team_id == data.get('team_id')
        )
    )
    existing_project_team = result.scalar_one_or_none()

    if existing_project_team:
        raise HTTPException(status_code=400, detail="Project already given to the team")

    # Check if project exists
    result = await db.execute(select(Project).where(Project.id == data.get('project_id')))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")

    # Check if team exists
    result = await db.execute(select(Team).where(Team.id == data.get('team_id')))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Team not found")

    new_project_team = ProjectTeam(**data)
    db.add(new_project_team)
    await db.commit()
    await db.refresh(new_project_team)

    return new_project_team



async def remove_project_from_a_team(db: AsyncSession, id: int):
    result = await db.execute(select(ProjectTeam).where(ProjectTeam.id == id))
    existing_project_team = result.scalar_one_or_none()

    if not existing_project_team:
        raise HTTPException(status_code=404, detail="ProjectTeam not found")

    await db.delete(existing_project_team)
    await db.commit()
    return existing_project_team



async def project_team(db: AsyncSession, id: int):
    result = await db.execute(select(Project).where(Project.id == id))
    existing_project = result.scalar_one_or_none()

    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not exist")
    
    return existing_project.teams



async def get_project_tasks(db: AsyncSession, id: int):
    result = await db.execute(select(Project).where(Project.id == id))
    existing_project = result.scalar_one_or_none()

    if not existing_project:
        raise HTTPException(status_code=404, detail="Project not exist")
    
    return existing_project.tasks
