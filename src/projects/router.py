from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from repositories.projects import ProjectRepository
from services.projects import ProjectService
from projects.schemas import ProjectCreate, ProjectBase
from user.auth_user import get_current_user
from user.models import User

router = APIRouter(
    prefix="/projects",
    tags=["Project"],
    # dependencies=[]
)


@router.get("",
            summary="Выводит структуру проектов"
            )
async def get_all_project(
        current_user: Annotated[User, Security(get_current_user, scopes=["user"])]
):
    """
    ### Выводит структуру проектов
    """
    result = await ProjectService(ProjectRepository).get_projects()
    return result


@router.post("",
             summary="Добавляет новый проект/подпроект"
             )
async def add_project(
        new_project: ProjectCreate,
        current_user: Annotated[User, Security(get_current_user, scopes=["admin"])]
):
    """
    ## Добавляет новый проект/подпроект
    ### **title [str]**: Название проекта
    ### **parent_id [None | int]**: ID проекта, к которому относится. По умолчанию None
    """
    project = await ProjectService(ProjectRepository).add_project(new_project)
    result = jsonable_encoder(project)
    return JSONResponse(content=result, status_code=HTTP_201_CREATED)


@router.delete("/{project_id}",
               summary="Удаляет проект/подпроект"
               )
async def delete_project(
        project_id: int,
        current_user: Annotated[User, Security(get_current_user, scopes=["admin"])]
):
    """
    ## Удаляет проект/подпроект
    ### **project_id [int]**: ID проекта, который нужно удалить
    # (Удаляет каскадно все задачи и проекты, которые к нему относятся)
    """
    res = await ProjectService(ProjectRepository).del_project(project_id)
    return {"status": "project delete"}


@router.patch("/{project_id}/{new_title}",
              summary="Изменяет название проекта/подпроекта"
              )
async def update_project_title(
        new_title: str,
        project_id: int,
        current_user: Annotated[User, Security(get_current_user, scopes=["admin"])]
):
    """
    ## Изменяет название проекта/подпроекта
    ### **new_title [str]**: Новое название проекта
    ### **project_id [int]**: ID проекта, который нужно изменить
    """
    res = await ProjectService(ProjectRepository).update_project_title(new_title, project_id)
    return {"status": "project update"}
