# app/api/v1/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from jose import jwt
# from app import crud, schemas
from ...schemas import user
from ... import models
from ...crud import crud_user
from ..deps import get_current_active_user, scopes_for_role
from app.db.session import get_db
from ...core import security
from app.core.config import settings

router = APIRouter()

@router.post("/signup", response_model = user.User)
def signup(user_in: user.UserCreate, db: Session = Depends(get_db)):
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print(f'the plain password the user wrote is {user_in.password}')
    return crud_user.create_user(db, user=user_in)

@router.post("/login", response_model = user.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_by_username(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    final_scopes = scopes_for_role(user.role or '')
    access_token = security.create_access_token({"sub": user.username, "scope": " ".join(final_scopes)})
    refresh_token = security.create_refresh_token({"sub": user.username, "scope": " ".join(final_scopes)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post('/refresh', response_model = user.Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = security.decode_hash_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        username = payload.get('sub')
        scopes = payload.get('scope')
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user = crud_user.get_by_username(db,username)

    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    new_access_token = security.create_access_token({'sub': user.username,'scope':scopes})
    new_refresh_token = security.create_refresh_token({'sub': user.username, 'scope':scopes})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


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

    return f'deleted user->{user}'

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