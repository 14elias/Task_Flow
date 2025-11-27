from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.user import User
from app import schemas
from app.core.security import get_password_hash

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_by_email(db: Session, email):
    return db.query(User).filter(User.email == email).first()

def create_user(db, user: schemas.user.UserCreate):
    user = User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def delete_user(username, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

    return user


def update_user(db, current_user, data):
    user = db.query(User).filter(User.username == current_user.username).first()

    if not user:
        raise HTTPException(status_code=404, detail='user not found')

    user.email = data.email
    user.username = data.username

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_all_user(db):
    users = db.query(User).all()

    if not users:
        raise HTTPException(status_code=404, detail='there are not users')
    
    return users


def deactivate(db, username):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def activate(db, username):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_tasks(db, id):
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail='user not exist')
    
    return user.assigned_tasks