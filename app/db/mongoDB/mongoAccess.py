import os
def GetMessagesCollection(client):
    dbName = os.getenv("MONGO_DBNAME")
    return client[dbName]["messages"]

def GetFilsCollection(client):
    dbName = os.getenv("MONGO_DBNAME")
    return client[dbName]["threads"]

def GetCheckpointCollection(client):
    dbName = os.getenv("MONGO_DBNAME")
    return client[dbName]["checkpoints"]