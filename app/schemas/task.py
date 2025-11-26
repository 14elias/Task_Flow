from pydantic import BaseModel
from datetime import datetime
from app.models.task import TaskStatus


class CreateTask(BaseModel):
    title: str
    details: str
    project_id: int 
    due_date: datetime

class AssignTask(BaseModel):
    assigned_to: int

class UpdateTask(BaseModel):
    title: str
    details: str
    project_id: int 
    due_date: datetime
    assigned_to: int

class ResponseTask(BaseModel):
    title: str
    details: str
    project_id: int 
    due_date: datetime
    assigned_to: int
    priority: int
    status:TaskStatus

    model_config = {
        "from_attributes": True
    }