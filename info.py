import MoocAI.app.db.mongoDB.mongoConnection as mongoConnection

def GetNumberThread(threadId):
    result = mongoConnection.FindId()