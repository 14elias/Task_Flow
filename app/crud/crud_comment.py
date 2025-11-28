from fastapi import HTTPException
from app.models import comment, task, user


def create_comment(db, data, current_user):
    existing_task = db.query(task.Task).filter(task.Task.id == data.get('task_id')).first()

    if not existing_task:
        raise HTTPException(status_code=404, detail='task not found')
    
    print( existing_task)

    if current_user.id != existing_task.assigned_to and current_user.role != user.RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail='you are not allowed to comment')
    
    new_comment = comment.Comment(**data)
    new_comment.user_id = current_user.id


    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


def get_all_comment_of_task(db, task_id):
    existing_task = db.query(task.Task).filter(task.Task.id == task_id).first()

    if not existing_task:
        raise HTTPException(status_code=404, detail='task not found')
    
    comments = existing_task.comments

    if not comments:
        raise HTTPException(status_code=404, detail='comments not found')
    return comments

def delete_comment(db, comment_id, current_user):
    existing_comment = db.query(comment.Comment).filter(comment.Comment.id == comment_id).first()

    if not existing_comment:
        raise HTTPException(status_code=404, detail='there is no comment with the given id')
    
    if existing_comment.user_id != current_user.id:
        raise HTTPException('youa are not allowed to delete this comment')
    
    db.delete(existing_comment)
    db.commit()

    return existing_comment


def update_comment(db, comment_id, current_user, data):
    existing_comment = db.query(comment.Comment).filter(comment.Comment.id == comment_id).first()

    if not existing_comment:
        raise HTTPException(status_code=404, detail='there is no comment with the given id')
    
    if existing_comment.user_id != current_user.id:
        raise HTTPException('youa are not allowed to edit this comment')
    
    existing_comment.content = data.get('content')

    db.commit()
    db.refresh(existing_comment)
    

    return existing_comment