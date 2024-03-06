from typing import Optional, Union, Deque

from pydantic import BaseModel, Field

from tasks.schemas import TaskBase


class ProjectCreate(BaseModel):
    title: str
    # parent_id: None | int | str = "null"
    parent_id: None | int = None


class ProjectBase(ProjectCreate):
    id: int
    tasks: Optional[list[TaskBase]]
    subprojects: Optional[list["ProjectBase"]]

    class Config:
        from_attributes = True

