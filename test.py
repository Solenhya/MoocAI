from app.db.mongoDB.mongoConnection import Find
import os
from dotenv import load_dotenv
load_dotenv()
from app.db.mongoDB import addSequential
def DoTest():
    result = Find("messages",projection={"body":1,"username":1})
    print(result)

if __name__=="__main__":
    #DoTest()
    print("Done")