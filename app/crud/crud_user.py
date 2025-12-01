from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from app.models.user import User
from app import schemas
from app.core.security import get_password_hash


async def get_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()



async def get_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()



async def create_user(db: AsyncSession, user: schemas.user.UserCreate):
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user



async def delete_user(db: AsyncSession, username: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return user



async def update_user(db: AsyncSession, current_user: User, data):
    result = await db.execute(
        select(User).where(User.username == current_user.username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Apply updates
    if data.email:
        user.email = data.email

    if data.username:
        user.username = data.username

    await db.commit()
    await db.refresh(user)

    return user



async def get_all_user(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()

    return users   



async def deactivate(db: AsyncSession, username: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user



async def activate(db: AsyncSession, username: str):
    result = await db.execute(
        select(User).where(User.username == username)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = True

    await db.commit()
    await db.refresh(user)

    return user




async def get_user_tasks(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.assigned_tasks
