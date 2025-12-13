from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeMeta

from app.db.session import Base, engine
from app.models.user import User
from app.models.project import Project, ProjectTeam
from app.models.team import Team, TeamMember
from app.models.notification import Notification
from app.models.comment import Comment
from app.models.task import Task, TaskStatus

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)