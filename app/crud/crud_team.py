from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.team import Team, TeamMember
from app.schemas import team as team_schema



async def create_team(db: AsyncSession, team_data: team_schema.TeamCreat):
    # Check if team exists
    result = await db.execute(
        select(Team).where(Team.name == team_data.name)
    )
    existing_team = result.scalar_one_or_none()

    if existing_team:
        raise HTTPException(status_code=400, detail="Team already registered")

    new_team = Team(**team_data.dict())
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)

    return new_team



async def get_all_team(db: AsyncSession):
    result = await db.execute(select(Team))
    teams = result.scalars().all()
    return teams  



async def get_a_team(db: AsyncSession, id: int):
    result = await db.execute(select(Team).where(Team.id == id))
    team_obj = result.scalar_one_or_none()

    if not team_obj:
        raise HTTPException(status_code=404, detail="Team not found")

    return team_obj



async def delete_team(db: AsyncSession, id: int):
    result = await db.execute(select(Team).where(Team.id == id))
    team_obj = result.scalar_one_or_none()

    if not team_obj:
        raise HTTPException(status_code=404, detail="Team not found")

    await db.delete(team_obj)
    await db.commit()

    return team_obj



async def update_team(db: AsyncSession, id: int, data: dict):
    result = await db.execute(select(Team).where(Team.id == id))
    team_obj = result.scalar_one_or_none()

    if not team_obj:
        raise HTTPException(status_code=404, detail="Team not found")

    if data.get("name"):
        team_obj.name = data["name"]
    if data.get("description"):
        team_obj.description = data["description"]

    await db.commit()
    await db.refresh(team_obj)

    return team_obj



async def add_member(db: AsyncSession, team_member_data: dict):
    result = await db.execute(
        select(TeamMember).where(
            TeamMember.team_id == team_member_data.get("team_id"),
            TeamMember.user_id == team_member_data.get("user_id")
        )
    )
    existing_member = result.scalar_one_or_none()

    if existing_member:
        raise HTTPException(status_code=400, detail="User already added to team")

    new_member = TeamMember(**team_member_data)
    db.add(new_member)
    await db.commit()
    await db.refresh(new_member)

    return new_member



async def remove_member(db: AsyncSession, id: int):
    result = await db.execute(select(TeamMember).where(TeamMember.id == id))
    existing_member = result.scalar_one_or_none()

    if not existing_member:
        raise HTTPException(status_code=404, detail="User not found in team")

    await db.delete(existing_member)
    await db.commit()

    return existing_member



async def get_team_members(db: AsyncSession, id: int):
    result = await db.execute(select(Team).where(Team.id == id))
    team_obj = result.scalar_one_or_none()

    if not team_obj:
        raise HTTPException(status_code=404, detail="Team not found")

    # team_obj.members should be pre-loaded using selectinload in your query if needed
    users = [member.user for member in team_obj.members]
    return users



async def get_team_projects(db: AsyncSession, id: int):
    result = await db.execute(select(Team).where(Team.id == id))
    team_obj = result.scalar_one_or_none()

    if not team_obj:
        raise HTTPException(status_code=404, detail="Team not found")

    # team_obj.projects should be pre-loaded using selectinload in your query if needed
    projects = [proj.project for proj in team_obj.projects]
    return projects
