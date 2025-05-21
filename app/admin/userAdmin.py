from fastapi import APIRouter , Depends , Request
from ..userManagements import userAccess
from ..db.mongoDB.mongoConnection import Find ,GetConnection
from ..dependencies import require_roles_any
router = APIRouter(dependencies=[Depends(require_roles_any(["admin"]))])
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent  # points to /app
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
from fastapi.responses import RedirectResponse


roles = ["admin","guest","users"]
@router.get("/user_admin")
async def getadminPage(request:Request):
    #DO i use find or abstraction ? 
    users = userAccess.get_users()
    #TODO

    #return {"status":"Success"}
    return templates.TemplateResponse("userManagement.html",{"request":request,"users":users,"roles":roles})

@router.post("/user_admin")
async def postAdmin(request:Request):
    users=Find("users",projection={"username":1,"_id":0,"roles":1})
    form = await request.form()
    # form is a MultiDict, keys like role_1, role_2 ...
    client = GetConnection()
    dbName = os.getenv("MONGO_DBNAME")
    collection = client[dbName]["users"]
    # Update users roles based on submitted form data
    for user in users:
        role_key = f"role_{user["username"]}"
        if role_key in form:
            new_role = form[role_key]
            print(f"Role key :{role_key},New role : {new_role}, user : {user}")
            if new_role in roles:
                collection.update_one({"username":user["username"]},{"$set": {"roles": [new_role]}})
                #Peut enregistrer les changements et les présenter dans une page avant de retourner a l'accueil
    return RedirectResponse(url="/accueil",status_code=303)
