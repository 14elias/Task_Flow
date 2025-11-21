from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.session import Base


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str] = mapped_column(String(500))

    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # relationships
    task: Mapped["Task"] = relationship(back_populates="comments")
    user: Mapped["User"] = relationship(back_populates="comments")
