from fastapi import HTTPException

from tasks.models import Status
from tasks.schemas import TaskCreateUUID, TaskChange
from user.models import User
from utils.repository import AbstractRepository


class TaskService:

    def __init__(self, project_repo: AbstractRepository):
        self.project_repo: AbstractRepository = project_repo()

    async def add_task(self, task: dict, user: User):
        task = TaskCreateUUID(**task.model_dump(), user_id=user.user_id)
        task_dict = task.model_dump()
        try:
            res = await self.project_repo.add_task(task_dict)
            return res
        except Exception:
            raise HTTPException(status_code=422, detail="Incorrect data")

    async def get_tasks(self, project_id: int):
        res = await self.project_repo.get_tasks_from_project(project_id)
        return res

    async def del_task(self, task_id: int, user: User):
        try:
            task = await self.project_repo._get_specific_task(task_id)
            if task.user_id != user.user_id and user.roles != "admin":
                raise HTTPException(status_code=403, detail="Forbidden")

            res = await self.project_repo.del_data(task_id)
            return res
        except Exception:
            raise HTTPException(status_code=422, detail="No such project found")

    async def change_status(self, task_id: int, new_status: Status):
        res = await self.project_repo.change_status(task_id, new_status)
        return res

    async def update_task(self, task_id: int, status_val: TaskChange):
        task_dict = status_val.model_dump()
        res = await self.project_repo._update_task(task_id, task_dict)
        return res
