from pydantic import BaseModel
from datetime import datetime


class CreateTask(BaseModel):
    title: str
    details: str
    project_id: int 
    assigned_to: int
    due_date: datetime