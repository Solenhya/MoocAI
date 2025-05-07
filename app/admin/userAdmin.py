from fastapi import APIRouter , Depends
from ..userManagements import userAccess
from ..db.mongoDB.mongoConnection import Find ,GetConnection
from ..dependencies import require_roles_any
router = APIRouter(dependencies=[Depends(require_roles_any(["admin"]))])

@router.get("/user_admin")
async def getadminPage():
    #DO i use find or abstraction ? 
    users = userAccess.get_users()
    #TODO
    return {"status":"Success"}


@router.post("/user_admin/{username}/set_roles")
async def setUserRoles(username:str):
    #TODO
    pass