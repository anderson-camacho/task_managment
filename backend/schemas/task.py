from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    due_date: Optional[datetime]
    priority: Optional[str] = Field(default="Media", pattern="^(Alta|Media|Baja)$")
    tags: Optional[List[str]] = []

class TaskOut(TaskCreate):
    id: str
    status: str
    created: datetime
