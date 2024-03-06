from typing import Union, Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes, OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError

from config import SECRET_KEY, ALGORITHM
from repositories.user import UserRepository
from services.users import UserService
# from user.auth import oauth2_scheme
from user.hasher import verify_password
from user.models import User
from user.schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/token",
    scopes={},
)

async def authenticate_user(username: str, password: str) -> Union[User, bool]:  # username = email
    user = await UserService(UserRepository).get_user_by_email(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")  # == email
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await UserService(UserRepository).get_user_by_email(token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user
