from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from user.auth_user import authenticate_user
from user.schemas import Token
from user.security import create_access_token

router = APIRouter(
    prefix="",
    tags=["Token"],
)

scope = {
    "user": ["user"],
    "admin": ["admin", "user"]
}


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email, "scopes": scope[user.roles]},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")
