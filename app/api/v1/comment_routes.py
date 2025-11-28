from fastapi import APIRouter, Depends, Security
from sqlalchemy.orm import Session
from typing import Annotated

from app.api import deps
from app.models import user
from app.schemas import comment
from app.crud import crud_comment


router = APIRouter()

@router.post('/comment/create', response_model=comment.ResponseComment)
def create_comment(
    data: comment.CreateComment,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["me"])],
    db: Session = Depends(deps.get_db)
):
    data = data.model_dump()
    comment = crud_comment.create_comment(db=db, data=data, current_user=current_user)

    return comment

@router.get('/comment/get_all_comment', response_model=list[comment.ResponseComment])
def get_all_comment_task(
    task_id: int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["me"])],
    db: Session = Depends(deps.get_db)
):
    comments = crud_comment.get_all_comment_of_task(db,task_id)

    return comments

@router.delete('/comment/delete', response_model=comment.ResponseComment)
def comment_delete(
    comment_id: int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["me"])],
    db: Session = Depends(deps.get_db)
):
    comments = crud_comment.delete_comment(db,comment_id, current_user)

    return comments


@router.patch('/comment/edit', response_model=comment.ResponseComment)
def comment_edit(
    data: comment.EditComment,
    comment_id: int,
    current_user: Annotated[user.User, Security(deps.get_current_active_user, scopes=["me"])],
    db: Session = Depends(deps.get_db)
):
    updated_comment = crud_comment.update_comment(
        db=db,
        data= data.model_dump(),
        current_user=current_user,
        comment_id=comment_id
    )

    return updated_comment