from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException

from app.models import user
from app import schemas
from app.core.security import get_password_hash


async def get_by_username(db: AsyncSession, username: str):
    result = await db.execute(
        select(user.User).where(user.User.username == username)
    )
    return result.scalar_one_or_none()



async def get_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(user.User).where(user.User.email == email)
    )
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, id: int):
    result = await db.execute(
        select(user.User).where(user.User.id == id)
    )
    return result.scalar_one_or_none()



async def create_user(db: AsyncSession, user_data: schemas.user.UserCreate):
    new_user = user.User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user



async def delete_user(db: AsyncSession, username: str):
    result = await db.execute(
        select(user.User).where(user.User.username == username)
    )
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(existing_user)
    await db.commit()

    return user



async def update_user(db: AsyncSession, current_user: user.User, data):
    result = await db.execute(
        select(user.User).where(user.User.username == current_user.username)
    )
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Apply updates
    if data.email:
        existing_user.email = data.email

    if data.username:
        existing_user.username = data.username

    await db.commit()
    await db.refresh(existing_user)

    return existing_user



async def get_all_user(db: AsyncSession):
    result = await db.execute(select(user.User))
    users = result.scalars().all()

    return users   



async def deactivate(db: AsyncSession, username: str):
    result = await db.execute(
        select(user.User).where(user.User.username == username)
    )
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False

    db.add(existing_user)
    await db.commit()
    await db.refresh(existing_user)

    return existing_user



async def activate(db: AsyncSession, username: str):
    result = await db.execute(
        select(user.User).where(user.User.username == username)
    )
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user.is_active = True

    await db.commit()
    await db.refresh(existing_user)

    return existing_user


async def get_user_tasks(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(user.User)
        .options(selectinload(user.User.assigned_tasks))
        .where(user.User.id == user_id)
    )
    existing_user = result.scalar_one()
    return existing_user.assigned_tasks


async def get_user_notifications(db: AsyncSession, user_id: int):
    result = await db.execute(
        select(user.User)
        .options(selectinload(user.User.notifications))
        .where(user.User.id == user_id)
    )
    existing_user = result.scalar_one()
    return existing_user.notifications
