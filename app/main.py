from fastapi import Depends, FastAPI
from fastapi.staticfiles import StaticFiles

from .dependencies import get_token_header
from .routers import users

app = FastAPI(dependencies=[Depends(get_token_header)])
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
