import pymongo
import os
from dotenv import load_dotenv
load_dotenv()
def GetConnection():
    return pymongo.MongoClient(os.getenv("MONGO_DB"))

def FindId(id):
    client = GetConnection()
    filter={"_id":id}

    result = client['mooc']['threads'].find(
  filter=filter
    )
    if(len(list(result.clone()))>0):
        return result[0]
    
if __name__=="__main__":
    print(FindId("52ef4b71ab137b00720007d4"))