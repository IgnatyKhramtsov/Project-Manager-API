import uuid

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class UserRead(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    is_active: bool = True
    roles: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    roles: str = "user"

class UserInDB(UserRead):
    hashed_password: str