# app/api/v1/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from typing import Annotated
# from app import crud, schemas
from app.schemas import user
from app import models, crud
from ..deps import get_current_active_user
from app.db.session import get_db


router = APIRouter()



@router.get('/user/me', response_model = user.User)
def get_me(current_user: Annotated[user.User, Security(get_current_active_user, scopes=["me"])]):
    return current_user


@router.delete('/user/delete')
async def delete_a_user(
    username:str,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["admin"])],
    db:Session = Depends(get_db)
    ):
    user = await crud.crud_user.delete_user(username, db)


    return user

@router.get('/user/all', response_model =list[user.User])
async def get_all_user(
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["admin"])],
    db:Session = Depends(get_db)
    ):

    users = await crud.crud_user.get_all_user(db)
    return users


@router.patch('/user/deactivate', response_model = user.User)
async def deactivate_user(
    username:str,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["admin"])],
    db:Session = Depends(get_db)
):
    user = await crud.crud_user.deactivate(db, username)

    return user


@router.patch('/user/activate', response_model = user.User)
async def activate_user(
    username:str,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["admin"])],
    db:Session = Depends(get_db)
):
    user = await crud.crud_user.activate(db, username)

    return user


@router.patch('/user/update', response_model = user.User)
async def update_user(
    data:user.UserUpdate,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["me"])],
    db:Session = Depends(get_db)
):
    user = await crud.crud_user.update_user(db, current_user, data)

    return user


@router.get('/user/tasks')
async def get_user_tasks(
    id: int,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["me"])],
    db:Session = Depends(get_db)
):
    tasks = await crud.crud_user.get_user_tasks(db, id)

    return tasks


@router.get('/user/notifications')
async def get_user_notifications(
    id: int,
    current_user:Annotated[models.user.User, Security(get_current_active_user, scopes=["me"])],
    db:Session = Depends(get_db)
):
    tasks = await crud.crud_user.get_user_notifications(db, id)

    return tasks