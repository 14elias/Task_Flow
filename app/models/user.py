from sqlalchemy import String, Boolean, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from enum import Enum as PyEnum

from .base import Base


class RoleEnum(PyEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"
    CLIENT = "client"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[RoleEnum] = mapped_column(Enum(RoleEnum), default=RoleEnum.MEMBER)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    teams: Mapped[list["TeamMember"]] = relationship(back_populates="user")
    assigned_tasks: Mapped[list["Task"]] = relationship(back_populates="assignee")
    comments: Mapped[list["Comment"]] = relationship(back_populates="user")
    notifications: Mapped[list["Notification"]] = relationship(back_populates="user")
    managed_projects: Mapped[list["Project"]] = relationship(back_populates="manager")
