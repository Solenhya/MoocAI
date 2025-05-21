from fastapi import APIRouter , Depends , Request , HTTPException
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

@router.get("/message/{message_id}")
async def ShowMessage(request:Request,message_id:str,userData=Depends(require_roles_any(["admin","users"]))):
    client = GetConnection()
    dbName=os.getenv("MONGO_DBNAME")
    message = client[dbName]["messages"].find_one(filter={"_id":message_id})
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return templates.TemplateResponse("showMessage.html",{"request":request,"message":message})
    pass