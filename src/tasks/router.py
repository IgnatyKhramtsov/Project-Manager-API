from typing import Annotated

from fastapi import APIRouter, Security, HTTPException, Query

from repositories.tasks import TaskRepository
from services.tasks import TaskService
from tasks.models import Status
from tasks.schemas import TaskCreate, TaskBase, TaskChange
from user.auth_user import get_current_user
from user.models import User

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


@router.get("/project/{project_id}",
            summary="Получает все задачи из определенного проекта"
            )
async def get_tasks_in_a_specific_project(
        project_id: int,
        current_user: Annotated[User, Security(get_current_user, scopes=["user"])]
) -> list[TaskBase]:
    """
    ## Получает все задачи из проекта
    ### **project_id [int]**: ID проекта, из которого нужно получить все задачи
    """
    project_tasks = await TaskService(TaskRepository).get_tasks(project_id)
    return project_tasks


@router.post("",
             summary="Создает новую задачу"
             )
async def add_task(
        new_task: TaskCreate,
        current_user: Annotated[User, Security(get_current_user, scopes=["user"])]
):
    """
    ## Создет задачу:
    ### - **title [str]**: Название задачи
    ### - **status [str]**: Статус задачи (new, progress, done)
    ### - **type [str]**: Тип (manager, technical_specialist)
    ### - **project_id [int]**: ID проекта
    """
    task = await TaskService(TaskRepository).add_task(new_task, current_user)
    return {"status": "task create"}


@router.delete("/{task_id}",
               summary="Удаляет задачу",
               )
async def delete_task(
        task_id: int,
        current_user: Annotated[User, Security(get_current_user, scopes=["user"])]
):
    """
    ## Удаляет задачу
    ### **task_id [int]**: ID задачи, которую нужно удалить
    """
    res = await TaskService(TaskRepository).del_task(task_id, current_user)
    return {"status": "task delete"}

@router.patch("/{task_id}/status",
              summary="Изменяет статус задачи"
              )
async def change_task_status(
        task_id: int,
        new_status: Status,
        current_user: Annotated[User, Security(get_current_user, scopes=["user"])]
):
    """
    ## Изменяет статус задачи
    ### **task_id [int]**: ID задачи, статус которой нужно изменить
    ### **new_status [str]**: Новый статус задачи (new, progress, done)
    """
    res = await TaskService(TaskRepository).change_status(task_id, new_status)
    return {"status": "task update"}

@router.patch("/{task_id}",
              summary="Изменяет задачу"
              )
async def change_task(
        task_id: int,
        data: TaskChange,
        current_user: Annotated[User, Security(get_current_user, scopes=["admin"])]
):
    """
    ## Изменяет задачу
    ### **task_id [int]**: ID задачи, которую нужно изменить
    ### **data [dict[str | int]]**: Новые данные задачи формата
    #### {
      #### "title": "string",
      #### "status": "new",
      #### "type": "manager",
      #### "project_id": 0
    #### }
    """
    res = await TaskService(TaskRepository).update_task(task_id, data)
    return {"status": "task update"}
