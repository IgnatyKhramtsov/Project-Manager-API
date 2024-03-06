import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from tasks.models import Status, Type


class TaskCreate(BaseModel):
    title: str
    status: Status = Status.new
    type: Type
    project_id: int


class TaskCreateUUID(TaskCreate):
    user_id: uuid.UUID


class TaskBase(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    updated_status: datetime


class TaskChange(BaseModel):
    title: Optional[str] = None
    status: Status = None
    type: Type = None
    project_id: int = None