from transformers import pipeline,AutoTokenizer, AutoModelForSequenceClassification
import torch
# Load the classification pipeline with the specified model
pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
model_name = "tabularisai/multilingual-sentiment-analysis"

import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Remonte jusqu'au dossier parent app
sys.path.append(parent_dir)
from db.mongoDB import iterator,mongoConnection
import time
from utils.time_estimation import EstimateRemaining
import torch

#Singleton pattern pour le tokenizer
tokenizer = None
def GetTokenizer():
    global tokenizer
    if tokenizer:
        return tokenizer
    else:
        tokenizer=AutoTokenizer.from_pretrained(model_name)
        return tokenizer
#Singleton pattern pour le model
model = None
def GetModel():
    global model
    if model:
        return model
    else:
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        return model

def InitialiseModele():
    GetTokenizer()
    GetModel()
    print("Modele Initialiser")

def GetSentiment(text:str):
    return pipe(text)

#Récupere le sentiment des textes entre -2 et 2
def GetSentimentValue(texts):
    inputs = GetTokenizer()(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = GetModel()(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    retours = [TranslateSentiment(array) for array in probabilities]
    return retours

#Utiliser la probabilité pour faire la somme retour entre -2 et 2
def TranslateSentiment(sentimentarray):
    sum = (sentimentarray[0]*(-2))+(sentimentarray[1]*(-1))+sentimentarray[3]+sentimentarray[4]*2

    if isinstance(sum, torch.Tensor):
        return sum.item()
    return sum

def AddSentiment():
    with mongoConnection.GetConnection() as client:
        dbName = os.getenv("MONGO_DBNAME")
        numberDoc = mongoConnection.GetCount("messages","G4",client)
        operationName = "sentiment"
        checkpointCollection = client["G4"]["checkpoints"]
        checkpoint = checkpointCollection.find_one({"operation":operationName})

        startValue = 0
        startTime = time.time()
        if checkpoint:
            value = checkpoint.get("checkpoint")
            print(f"Reprise de l'operation au checkpoint {value}")
            startValue=value
        currentPoint=startValue
        for docs in iterator.IterateCheckPoint("messages",projection={"body":1,"_id":1},filter={},session=client,dbName=dbName,chunksize=100,operationName=operationName):
            messages= [message["body"] for message in docs]
            sentiments=GetSentimentValue(messages)
            mongoConnection.InsertBulk(docs,sentiments,"sentiment_tabularisai",client,dbName,"messages")
            currentPoint+=len(docs)
            print(f"Insertion des sentiments en cours : {currentPoint} sur {numberDoc}. Temps restant : {EstimateRemaining(startValue,currentPoint,numberDoc,time.time()-startTime)}")
        
if __name__=="__main__":
    values = GetSentimentValue(["Bonjour le monde","Damn that hot"])
    print(values[0])