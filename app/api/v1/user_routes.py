# app/api/v1/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated
from jose import jwt
# from app import crud, schemas
from ...schemas import user
from ... import models
from ...crud import crud_user
from ..deps import get_current_active_user
from app.db.session import get_db
from ...core import security
from app.core.config import settings

router = APIRouter()



@router.get('/user/me', response_model = user.User)
def get_me(current_user: Annotated[user.User, Security(get_current_active_user, scopes=["me"])]):
    print(current_user)
    return current_user

@router.delete('/user/delete')
def delete_user(
    username:str,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["admin"])],
    db:Session = Depends(get_db)
    ):

    user = db.query(models.user.User).filter(models.user.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()

    return user

@router.get('/user/all', response_model =list[user.User])
def get_all_user(
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["admin"])],
    db:Session = Depends(get_db)
    ):

    users = db.query(models.user.User).all()
    return users

@router.patch('/user/deactivate', response_model = user.User)
def deactivate_user(
    username:str,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["admin"])],
    db:Session = Depends(get_db)
):
    user = db.query(models.user.User).filter(models.user.User.username == username).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@router.patch('/user/update', response_model = user.User)
def update_user(
    data:user.UserUpdate,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["me"])],
    db:Session = Depends(get_db)
):
    user = db.query(models.user.User).filter(models.user.User.username == current_user.username).first()
    user.email = data.email
    user.username = data.username

    db.add(user)
    db.commit()
    db.refresh(user)

    return user