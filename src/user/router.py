from typing import Annotated

from fastapi import APIRouter, Security
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from repositories.user import UserRepository
from services.users import UserService
from user.auth_user import get_current_user
from user.models import User
from user.schemas import UserCreate, UserRead

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("",
             summary="Создает нового пользователя",
             status_code=201
             )
async def creat_user(user: UserCreate):
    """
    ## Создает нового пользователя
    ### - **email [str]**: Email нового пользователя
    ### - **password [str]**: Пароль нового пользователя
    ### - **roles [str]**: Роль пользователя (user, admin)
    """
    res = await UserService(UserRepository).create_user(user)
    result = jsonable_encoder(res)
    return JSONResponse(content=result, status_code=HTTP_201_CREATED)


# @router.get("", response_model=UserRead)
# async def get_user_by_email(email: EmailStr):
#     res = await UserService(UserRepository).get_user_by_email(email)
#     return res
