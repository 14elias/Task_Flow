# app/api/v1/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
# from app import crud, schemas
from ...schemas import user
from ...crud import crud_user
from app.db.session import get_db
from app.core.security import verify_password, create_access_token

router = APIRouter()

@router.post("/signup")
def signup(user_in: user.UserCreate, db: Session = Depends(get_db)):
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print(f'the plain password the user wrote is {user_in.password}')
    return crud_user.create_user(db, user=user_in)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud_user.get_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    print(user)

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
