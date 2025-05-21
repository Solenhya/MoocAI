from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from .userManagements.auth import get_current_user
from .routers import users,applicationRouter
from .admin import userAdmin
app = FastAPI()
app.include_router(users.router)
app.include_router(userAdmin.router)
app.include_router(applicationRouter.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
