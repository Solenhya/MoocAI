from fastapi import Depends, FastAPI , Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .userManagements.auth import get_current_user
from .routers import users,applicationRouter,api
from .admin import userAdmin
app = FastAPI()
app.include_router(users.router,tags=["users"])
app.include_router(userAdmin.router,tags=["admin"])
app.include_router(applicationRouter.router)
app.include_router(api.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/",tags=["redirection"])
async def root():
    response = RedirectResponse(url="/login", status_code=303)
    return response
    return {"message": "Hello MoocAI Applications!"}

@app.get("/health",tags=["check"])
async def health():
    return{"status":"ok"}