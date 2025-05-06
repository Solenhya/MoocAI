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
    
if __name__=="__main__":
    path = "mongodb://"+os.getenv("MONGO_USER")+":"+ os.getenv("MONGO_PASSWORD")+"@"+os.getenv("MONGO_HOST")
    print(path)