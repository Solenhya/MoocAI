from fastapi import APIRouter , Depends , Request , HTTPException
from ..userManagements import userAccess
from ..db.mongoDB.mongoConnection import Find ,GetConnection
from ..dependencies import require_roles_any
from ..services.sentiment_tabularisai import GetSentimentValue
from ..utils.sentiment_manipulation import TranslateSentiment
router = APIRouter()
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent  # points to /app
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
from fastapi.responses import RedirectResponse

from .api import GetUserStats,CollectResultsUser , GenerateSentiment

@router.get("/accueil",tags=["présentation"])
async def PageLogin(request:Request,userData = Depends(require_roles_any(["admin","guest","users"]))):
    return templates.TemplateResponse("accueil.html",{"request":request})

@router.get("/filtrer_message",tags=["messages"])
async def FilterMessage(request:Request,userData=Depends(require_roles_any(["admin","users"]))):

    return templates.TemplateResponse("filtre.html",{"request":request})

@router.get("/message/{message_id}",tags=["messages"])
async def ShowMessage(request:Request,message_id:str,userData=Depends(require_roles_any(["admin","users"]))):
    client = GetConnection()
    dbName=os.getenv("MONGO_DBNAME")
    collection = client[dbName]["messages"]
    GenerateSentiment(collection,{"_id":message_id})
    message = collection.find_one(filter={"_id":message_id})
    sentimentLabel = GetMessageSentimentLabel(message_id,client,dbName)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return templates.TemplateResponse("showMessage.html",{"request":request,"message":message,"sentiment_label":sentimentLabel})


def GetMessageSentimentLabel(id,client,dbName):
    collection = client[dbName]["messages"]
    GenerateSentiment(collection,{"_id":id})
    message = collection.find_one({"_id":id},{"_id":1,"body":1,"sentiment_tabularisai":1})
    print(message)
    sentiment = message["sentiment_tabularisai"]
    if not sentiment:
        sentiment = GetSentimentValue([message["body"]])
        collection.update_one({"_id":message["_id"]},{"$set": {"sentiment_tabularisai": sentiment}})
    return TranslateSentiment(sentiment)

@router.get("/user/{user_name}",tags=["participants"])
async def ShowUser(request :Request,user_name:str):
    with GetConnection() as client:
        dbName = os.getenv("MONGO_DBNAME")
        collection = client[dbName]["messages"]
        userResult = CollectResultsUser(collection,user_name)
        messages = userResult["results"]
        tronq = userResult["tronq"]
        if len(messages)<1:
            print(messages)
            return{"Status":404,"detail":"L'utilisateur n'existe pas"}

        userStats = GetUserStats(messages)
        if not userStats:
            pass
    return templates.TemplateResponse("showUser.html",{"request":request,"user":{"username":user_name},"sentiment_values":userStats,"tronq":tronq})

def GetDefaultUserStats():
    retour = {"average":{"label":"Erreur","score":"Erreur"},
              "min":{"label":"Erreur","score":"Erreur"},
              "max":{"label":"Erreur","score":"Erreur"}}
    return retour

@router.get("/cluster_messages",tags=["messages","clustering"])
async def ClusterMessage(request:Request):
    #TODO
    return templates.TemplateResponse("cluster_message.html",{"request":request})