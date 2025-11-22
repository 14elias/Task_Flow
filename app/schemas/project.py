from pydantic import BaseModel
from datetime import datetime

class ProjectCreate(BaseModel):
    title: str
    description: str

class ProjectUpdate(BaseModel):
    title: str
    description: str


