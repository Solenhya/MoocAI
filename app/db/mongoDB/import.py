import pymongo
import json
import MoocAI.app.db.mongoDB.mongoConnection as mongoConnection
import os

#Une fonction pour importer depuis un fichier json
def ImportMany(dbName,collectionName,filePath):
    data=[]
    with open(filePath,"r",encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    with mongoConnection.GetConnection() as myclient:
        db = myclient[dbName]
        collection = db[collectionName]
        print(f"Collection {collection}")
        count =0
        total = len(data)
        for i in data:
            id = i["_id"]
            if(mongoConnection.FindId(myclient,id,dbName,collectionName)==None):
                collection.insert_one(i)
                print(f"Inserted data : {count}/{total}")
            if count%500==0:
                print(f"{count} data processed")
            count+=1

#Une fontion recursive pour extraire les message des thread et les inserer dans une nouvelle collection
def stevefunk(content,client,dataBase,collection):
    #Extrait les informations du content qu'on est en train de traiter
    username = content.get("username", "")
    courseid = content.get("course_id", "")
    id = content.get("id", "")
    depth = content.get("depth", "?")

    #Récupere les branches issues de ce content
    children = content.get("children", [])
    endorsed_responses = content.get('endorsed_reponses',[])
    non_endorsed_responses = content.get('non_endorsed_reponses',[])

    #Print l'etat actuel de la fonction
    print(f"{depth} {id} {courseid:30} {username}", flush=True)
    #Assigne l'id mongodb a l'id de la data
    content['_id'] = id

    #Cherche content dans la collection d'insertion
    result = client[dataBase][collection].find_one({'_id' : id})
    if result is None:
        #Retire la structure d'arbre avant de l'inserer dans la collection
        content.pop("children",None)
        content.pop("endorsed_reponses",None)
        content.pop("non_endorsed_reponses",None)
        client[dataBase][collection].insert_one(content)
    
    #Itere recursivement sur les enfants
    for doc in children:
        stevefunk(doc,client,dataBase,collection)
    
    for doc in endorsed_responses:
        stevefunk(doc,client,dataBase,collection)

    for doc in non_endorsed_responses:
        stevefunk(doc,client,dataBase,collection)


def ExtractMessage(dbName,baseCollection,OutCollection):
    with mongoConnection.GetConnection() as client:
        filter={}
        project={
        'content' : 1
        }
        result = client[dbName][baseCollection].find(
        filter=filter,
        projection=project
        )
        for doc in result:
            content = doc["content"]
            print("-" * 100, flush=True)
            stevefunk(content,client,dbName,OutCollection)

def DoFullImport():
    filePath = "MOOC_forum.json"
    db = os.getenv("MONGO_DBNAME")
    collection = "threads"
    messageCollection= "messages"
    ImportMany(db,collection,filePath)
    ExtractMessage(db,collection,messageCollection)


if __name__=="__main__":
    DoFullImport()
    #ExtractMessage(os.getenv("MONGO_DBNAME"),"threads","messages")