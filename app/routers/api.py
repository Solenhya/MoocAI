from fastapi import APIRouter , Depends , Request
from ..userManagements import userAccess
from ..db.postgre.db_connection import get_session
from ..db.mongoDB.mongoConnection import Find ,GetConnection
from ..dependencies import require_roles_any
router = APIRouter()
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent  # points to /app
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
from fastapi.responses import RedirectResponse
from typing import Optional
from ..services.vectorCompare import GetSimilar


@router.get("/filterMessage")
async def FilterMessage(request:Request,text: Optional[str] = None,userData=Depends(require_roles_any(["admin","users"]))):
    limit = 10
    listeId = []
    with get_session() as session:
        results = GetSimilar(text,limit,session)
        for result in results:
            listeId.append(result.id_message)
            print(result.id_message)
    client = GetConnection()
    print(listeId)
    dbName=os.getenv("MONGO_DBNAME")
    collection = client[dbName]["messages"]
    results = CollectResults(collection,listeId)
    client.close()
    return results

#A Modifier pour changer la projection et éventuellement faire un traitement dans le cas ou le sentiments n'a pas encore été traité
def CollectResults(collection,listeId):
    results = collection.find({"_id": {"$in": listeId}},{"_id":1,"body":1})
    return list(results)