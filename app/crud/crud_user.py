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