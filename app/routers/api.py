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
from ..services.sentiment_tabularisai import GetSentimentValue
from ..utils.sentiment_manipulation import TranslateSentiment

@router.get("/filterMessage",tags=["messages","api"])
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
    results = CollectResultsFilter(collection,listeId)
    client.close()
    return results

#A Modifier pour changer la projection et éventuellement faire un traitement dans le cas ou le sentiments n'a pas encore été traité
def CollectResultsFilter(collection,listeId):
    filter = {"_id":{"$in":listeId}}
    tronqué = GenerateSentiment(collection,filter)
    results = collection.find({"_id": {"$in": listeId}},{"_id":1,"body":1,"sentiment_tabularisai":1})
    results = list(results)
    retour = {"results":results,"tronq":0}
    if tronqué:
        retour["tronq"]=tronqué["tronqué"]
    return retour

#Une fonction qui prend un parameters un filtre et qui va remplir les documents qui n'ont pas encore l'évaluation de sentiment
def GenerateSentiment(collection,filter):
    #Ajout du filtre d'absence d'évaluation
    query_filter = dict(filter)
    query_filter["sentiment_tabularisai"]={"$exists":0}
    resultsNoSent = collection.find(query_filter,{"_id":1,"body":1})
    listeDoc = list(resultsNoSent)
    length = len(listeDoc)
    if(length):
        return
    print(f"Sentiment non traité : {length}")
    if length>100:
        resultsNoSent=collection.find(query_filter,{"_id":1,"body":1}).limit(100)
    listeBodyNoSent = [message["body"] for message in listeDoc]
    listeIdNoSent = [message["_id"] for message in listeDoc]
    listeSentiment = GetSentimentValue(listeBodyNoSent) 
    #Fait l'insertion
    for i in range(len(listeIdNoSent)):
        collection.update_one(
        {"_id": listeIdNoSent[i]},
        {"$set": {"sentiment_tabularisai": listeSentiment[i]}}
        )
    if length>100:
        return length-100


@router.get("/user_messages/{user_name}",tags=["participants","api"])
async def GetUserMessages(request : Request,user_name:str):
    with GetConnection() as client:
        dbName = os.getenv("MONGO_DBNAME")
        collection = client[dbName]["messages"]
        messages = CollectResultsUser(collection,user_name)["results"]
        if not messages:
            return{"Erreur":"Cet utilisateur n'existe pas"}
        return {"messages":messages}
    
@router.get("/user_stats/{user_name}",tags=["participants","api"])
async def GetUserStats(request:Request,user_name:str):
    with GetConnection() as client:
        dbName = os.getenv("MONGO_DBNAME")
        collection = client[dbName]["messages"]
        messages = CollectResultsUser(collection,user_name)["results"]
        if not messages:
            return{"Erreur":"Cet utilisateur n'existe pas"}
        sentiment_results = GetUserStats(messages)
        return{"sentiment_values":sentiment_results}

def CollectResultsUser(collection,username):
    filter = {"username":username}
    tronq = GenerateSentiment(collection,filter)
    query_filter=dict(filter)
    query_filter["sentiment_tabularisai"]={"$exists":1}
    results = collection.find(query_filter,{"_id":1,"body":1,"sentiment_tabularisai":1})
    results = list(results)
    retour = {"results":results,"tronq":0}
    if tronq:
        retour["tronq"]=tronq
    return retour

def GetUserStats(messages):
    messages = list(messages)
    nombreMessages = len(messages)
    minSent = 2 #Set a la valeur max 
    maxSent=-2
    totSent=0
    if nombreMessages==0:
        return

    for message in messages:
        sent = message["sentiment_tabularisai"]
        totSent+=sent

        if sent<minSent:
            minSent = sent
        if sent>maxSent:
            maxSent=sent
    if nombreMessages>0:
        averageSent = totSent/nombreMessages
    else:
        averageSent="Pas de messages"
    retour = {"average":{"label":TranslateSentiment(averageSent),"score":averageSent},
              "min":{"label":TranslateSentiment(minSent),"score":minSent},
              "max":{"label":TranslateSentiment(maxSent),"score":maxSent}}
    return retour