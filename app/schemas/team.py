from pydantic import BaseModel
from datetime import datetime

class TeamCreat(BaseModel):
    name: str
    description: str

class ResponseTeam(BaseModel):
    id: int
    name: str
    description: str
    created_by: int
    created_at: datetime

class CreateTeamMember(BaseModel):
    user_id: int
    team_id: int

class ResponseTeamMember(BaseModel):
    id: int
    user_id: int
    team_id: int