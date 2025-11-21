from sqlalchemy import String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum as PyEnum

from app.db.session import Base


class TaskStatus(PyEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    details: Mapped[str] = mapped_column(String(500), nullable=True)

    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING)
    priority: Mapped[int] = mapped_column(Integer, default=1)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"))
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"))

    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relationships
    project: Mapped["Project"] = relationship(back_populates="tasks")
    assignee: Mapped["User"] = relationship(back_populates="assigned_tasks")
    comments: Mapped[list["Comment"]] = relationship(back_populates="task")
