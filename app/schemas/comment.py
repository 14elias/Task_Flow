from pydantic import BaseModel
from datetime import datetime


class CreateComment(BaseModel):
    content: str
    task_id: int


class ResponseComment(BaseModel):
    id: int
    content: str
    task_id: int
    user_id: int
    created_at: datetime

class EditComment(BaseModel):
    content: str