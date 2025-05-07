from ..db.mongoDB.mongoConnection import GetConnection , Find 
from .security import get_password_hash , verify_password
import os

def get_user(useName):  
    found = Find("users",filter={"username":useName})
    if(len(found)>0):
        return found[0]

def sign_user(useName,password):
    """Assume que l'user n'existe pas"""
    hashedPassword = get_password_hash(password)
    databaseName = os.getenv("MONGO_DBNAME")
    document = {"username":useName,"hashed_password":hashedPassword}
    with GetConnection() as client:
        client[databaseName]["users"].insert_one(document)

def get_users():
    found = Find("users",projection={"username":1,"roles":1})
    return found