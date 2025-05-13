from app.db.mongoDB.mongoConnection import Find
import os
from dotenv import load_dotenv
load_dotenv()

def DoTest():
    result = Find("messages",filter={"username":"qb"},projection={"body":1,"username":1})
    print(result)
if __name__=="__main__":
    DoTest()