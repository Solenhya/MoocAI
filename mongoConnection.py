import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
def GetConnection():
    path = "mongodb://"+os.getenv("MONGO_USER")+":"+os.getenv("MONGO_PASSWORD")+"@"+os.getenv("MONGO_HOST")
    return pymongo.MongoClient(path)

def FindId(id,dbName,collection):
    client = GetConnection()
    filter={"_id":id}
    with client[dbName][collection].find(filter=filter) as result:
        if(len(list(result.clone()))>0):
            return result[0]
    
if __name__=="__main__":
    print(FindId("52ef4b71ab137b00720007d4","mooc","threads"))