from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

# from auth.base_config import auth_backend, current_user, fastapi_users
# from auth.models import User
# from auth.schemas import UserRead, UserCreate

from fastapi.security import SecurityScopes, OAuth2PasswordBearer

from tasks.router import router as router_task
from projects.router import router as router_project
from user.auth import router as router_auth
from user.router import router as router_user

app = FastAPI(
    title='Project Manager API',
    docs_url="/"
)



app.include_router(router_user)
app.include_router(router_project)
app.include_router(router_task)
app.include_router(router_auth)

#
# @app.get("/ping")
# async def ping():
#     return {"status": " ok"}

# if __name__ == "__main__":
#     uvicorn.run(f"main:app", port=8006, reload=True)


