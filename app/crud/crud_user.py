from sqlalchemy.orm import Session
from app.models.user import User
from app import schemas, models
from app.core.security import get_password_hash

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_by_email(db: Session, email):
    return db.query(User).filter(User.email == email).first()

def create_user(db, user: schemas.user.UserCreate):
    user = models.user.User(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user