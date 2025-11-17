from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relationships
    manager: Mapped["User"] = relationship()
    tasks: Mapped[list["Task"]] = relationship(back_populates="project")
    teams: Mapped[list["ProjectTeam"]] = relationship(back_populates="project")


class ProjectTeam(Base):
    __tablename__ = "project_teams"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"))

    project: Mapped["Project"] = relationship(back_populates="teams")
    team: Mapped["Team"] = relationship(back_populates="projects")
