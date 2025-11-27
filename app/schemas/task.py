from pydantic import BaseModel
from datetime import datetime
from app.models.task import TaskStatus


class CreateTask(BaseModel):
    title: str
    details: str
    project_id: int 
    due_date: datetime

class AssignTask(BaseModel):
    task_id: int
    assigned_to: int

class UpdateTask(BaseModel):
    task_id: int
    title: str
    details: str
    project_id: int 
    due_date: datetime
    assigned_to: int

class ResponseTask(BaseModel):
    id: int
    title: str
    details: str
    project_id: int 
    due_date: datetime
    assigned_to: int | None
    priority: int
    status:TaskStatus

    model_config = {
        "from_attributes": True
    }


class UnAssignTask(BaseModel):
    task_id: int
    assigned_to: int


class UpdateTask(BaseModel):
    title: str
    details: str
    project_id: int 
    due_date: datetime
    priority: int
    status:TaskStatus