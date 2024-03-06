import enum
from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from user.models import User


intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow
    )]
updated_status = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]


class Status(str, enum.Enum):
    new = "new"
    progress = "progress"
    done = "done"


class Type(str, enum.Enum):
    manager = "manager"
    technical_specialist = "technical specialist"



class Project(Base):
    __tablename__ = "project"

    id: Mapped[intpk]
    title: Mapped[str]
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"), default=None)

    tasks: Mapped[Optional[list["Task"]]] = relationship(
        back_populates="project",
        cascade="all, delete",
        passive_deletes=True,
    )
    subprojects: Mapped[Optional[list["Project"]]] = relationship(
        cascade="all, delete",
        passive_deletes=True,
    )



class Task(Base):
    __tablename__ = "task"

    id: Mapped[intpk]
    title: Mapped[str]
    status: Mapped[Status] = mapped_column(default=Status.new)
    type: Mapped[Type]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    updated_status: Mapped[updated_status]
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.user_id", ondelete="SET NULL"), nullable=True)


    project: Mapped["Project"] = relationship(
        back_populates="tasks",
    )