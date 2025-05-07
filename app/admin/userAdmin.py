from fastapi import APIRouter
from ..userManagements import userAccess
from ..db.mongoDB.mongoConnection import Find ,GetConnection
router = APIRouter()

@router.get("/user_admin")
async def getadminPage():
    #DO i use find or abstraction ? 
    users = userAccess.get_users()
    #TODO
    pass

@router.post("/user_admin/{username}/set_roles")
async def setUserRoles(username:str):
    #TODO
    pass