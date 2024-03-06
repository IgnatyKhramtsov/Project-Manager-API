import uuid

from sqlalchemy import Column, String, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from database import Base

UUID_ID = uuid.UUID

class User(Base):
    __tablename__ = "user"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    roles: Mapped[str] = mapped_column(nullable=False, default="user")
