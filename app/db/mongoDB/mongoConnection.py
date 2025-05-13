import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

def GetConnection():
    path = "mongodb://"+os.getenv("MONGO_USER")+":"+ os.getenv("MONGO_PASSWORD")+"@"+os.getenv("MONGO_HOST")
    return pymongo.MongoClient(path)

def FindId(client,id,dbName,collection):
    filter={"_id":id}
    with client[dbName][collection].find(filter=filter) as result:
        if(len(list(result.clone()))>0):
            return result[0]

#Give a simplified tool where 
def Find(collection,filter={},projection={},client=None):
    """
    Deux comportement si on donne une connection qui est gerer a l'exterieur on renvoie le curseur sinon on renvoie une liste de résultat
    En créant et fermant une connection
    """
    close = False
    #Si on n'a pas donner de client on creer une connection et on la ferme
    if(client==None):
        close = True
        client = GetConnection()
        print("connection creer")
    dbName = os.getenv("MONGO_DBNAME")

    cursor = client[dbName][collection].find(filter=filter,projection=projection)
    if(close):
        retour = []
        for i in cursor:
            retour.append(i)
        client.close()
        return retour
    return cursor

if __name__=="__main__":
    pass