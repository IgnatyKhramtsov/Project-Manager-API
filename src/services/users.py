from typing import Optional

from fastapi import HTTPException

from user.hasher import get_password_hash
from user.models import User

class UserService:
    def __init__(self, project_repo):
        self.project_repo = project_repo()

    async def create_user(self, data: dict):
        user_dict = data.model_dump()
        password = user_dict.pop("password")
        user_dict["hashed_password"] = get_password_hash(password)
        try:
            res = await self.project_repo.create_user(user_dict)
            return res
        except Exception:
            raise HTTPException(status_code=422, detail="Incorrect data")

    async def get_user_by_email(self, email: str) -> Optional[User]:
        res = await self.project_repo._get_user_by_email(email)
        return res