from pydantic import BaseModel
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: str

class ProjectUpdate(BaseModel):
    title: str
    description: str

class ProjectTeam(BaseModel):
    project_id: int
    team_id: int

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    created_by: int
    created_at: datetime

