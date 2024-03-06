
from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import insert, select, func, update, text
from sqlalchemy.orm import selectinload

from database import async_session_maker
from projects.schemas import ProjectBase
from tasks.models import Task
from tasks.schemas import TaskBase
from user.models import User
from user.schemas import UserRead, UserInDB


class AbstractRepository(ABC):
    @abstractmethod
    async def add_project(self):
        raise NotImplementedError

    @abstractmethod
    async def get_projects(self):
        raise NotImplementedError

    @abstractmethod
    async def del_data(self):
        raise NotImplementedError

    @abstractmethod
    async def update_project_title(self):
        raise NotImplementedError

    @abstractmethod
    async def add_task(self):
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_from_project(self):
        raise NotImplementedError

    @abstractmethod
    async def change_status(self):
        raise NotImplementedError

    @abstractmethod
    async def _get_specific_task(self):
        raise NotImplementedError

    @abstractmethod
    async def _update_task(self):
        raise NotImplementedError


class SQLAlchemyProjectRepository(AbstractRepository):
    model = None

    async def add_project(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_projects(self):
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .options(selectinload(self.model.subprojects))
                .options(selectinload(self.model.tasks))
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()
            result_dto = [ProjectBase.model_validate(row, from_attributes=True) for row in result]
            return result_dto

    async def del_data(self, id: int):
        async with async_session_maker() as session:
            query = await session.get(self.model, id)
            await session.delete(query)
            await session.commit()
            return query

    async def update_project_title(self, new_title: str, project_id: int):
        async with async_session_maker() as session:
            query = await session.get(self.model, project_id)
            query.title = new_title
            await session.commit()
            return query

#########################################################################################
###############################  TASK  REPOSITORY  ######################################
#########################################################################################

    async def add_task(self, data: dict):
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def get_tasks_from_project(self, project_id):
        async with async_session_maker() as session:
            query = (
                select(self.model)
                .where(self.model.project_id == project_id)
            )
            res = await session.execute(query)
            result = res.unique().scalars().all()
            result_dto = [TaskBase.model_validate(row, from_attributes=True) for row in result]
            return result_dto

    async def change_status(self, task_id, new_status):
        async with async_session_maker() as session:
            query = await session.get(self.model, task_id)
            query.status = new_status
            query.updated_status = datetime.utcnow()
            await session.commit()
            return query


    async def _get_specific_task(self, task_id: int) -> Task:
        async with async_session_maker() as session:
            query = await session.get(self.model, task_id)
            return query

    async def _update_task(self, task_id: int, data: dict):
        async with async_session_maker() as session:
            stmt = update(self.model).where(self.model.id == task_id).values(**data)
            res = await session.execute(stmt)
            await session.commit()
            return res



class SQLAlchemyUserRepository:
    model = None

    async def create_user(self, user_data) -> UserRead:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**user_data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            result_dto = UserRead.model_validate(res.scalar_one(), from_attributes=True)
            return result_dto

    async def _get_user_by_email(self, email: str) -> Optional[User]:
        async with async_session_maker() as session:
            stmt = select(self.model).where(
                func.lower(self.model.email) == func.lower(email)
            )
            result = await session.execute(stmt)
            result = result.unique().scalar_one_or_none()
            # result_dto = UserInDB.model_validate(result, from_attributes=True)
            return result