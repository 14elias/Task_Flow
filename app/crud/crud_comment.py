from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models import comment, task, user



async def create_comment(db: AsyncSession, data: dict, current_user):
    # Check if task exists
    result = await db.execute(select(task.Task).where(task.Task.id == data.get('task_id')))
    existing_task = result.scalar_one_or_none()

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Permission check
    if current_user.id != existing_task.assigned_to and current_user.role != user.RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="You are not allowed to comment")

    new_comment = comment.Comment(**data, user_id=current_user.id)
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)

    return new_comment



async def get_all_comment_of_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(task.Task).where(task.Task.id == task_id))
    existing_task = result.scalar_one_or_none()

    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")

    comments = existing_task.comments
    if not comments:
        return []  # Return empty list instead of raising 404

    return comments



async def delete_comment(db: AsyncSession, comment_id: int, current_user):
    result = await db.execute(select(comment.Comment).where(comment.Comment.id == comment_id))
    existing_comment = result.scalar_one_or_none()

    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if existing_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to delete this comment")

    await db.delete(existing_comment)
    await db.commit()

    return existing_comment



async def update_comment(db: AsyncSession, comment_id: int, current_user, data: dict):
    result = await db.execute(select(comment.Comment).where(comment.Comment.id == comment_id))
    existing_comment = result.scalar_one_or_none()

    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if existing_comment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not allowed to edit this comment")

    existing_comment.content = data.get('content', existing_comment.content)
    await db.commit()
    await db.refresh(existing_comment)

    return existing_comment
