from fastapi import HTTPException

from projects.schemas import ProjectCreate
from utils.repository import AbstractRepository


class ProjectService:
    def __init__(self, project_repo: AbstractRepository):
        self.project_repo: AbstractRepository = project_repo()

    async def add_project(self, project: ProjectCreate):
        try:
            project_dict = project.model_dump()
            project_i = await self.project_repo.add_project(project_dict)
            return project_i
        except Exception:
            raise HTTPException(status_code=422, detail="Incorrect data")

    async def get_projects(self):
        project_structure = await self.project_repo.get_projects()
        return project_structure

    async def del_project(self, project_id: int):
        try:
            res = await self.project_repo.del_data(project_id)
            return res
        except Exception:
            raise HTTPException(status_code=422, detail="No such project found")

    async def update_project_title(self, new_title: str, project_id: int):
        res = await self.project_repo.update_project_title(new_title, project_id)
        return res
