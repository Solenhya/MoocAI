from fastapi import APIRouter , Depends , Request
from ..userManagements import userAccess
from ..db.mongoDB.mongoConnection import Find ,GetConnection
from ..dependencies import require_roles_any
router = APIRouter()
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent  # points to /app
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
from fastapi.responses import RedirectResponse

@router.get("/accueil")
async def PageLogin(request:Request,userData = Depends(require_roles_any(["admin","guest","users"]))):
    return templates.TemplateResponse("accueil.html",{"request":request})

@router.get("/filtrer_message")
async def FilterMessage(request:Request,userData=Depends(require_roles_any(["admin","users"]))):

    return templates.TemplateResponse("filtre.html",{"request":request})