import pymongo
import json
import mongoConnection

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
            if(mongoConnection.FindId(id,dbName,collectionName)==None):
                collection.insert_one(i)
                print(f"Inserted data : {count}/{total}")
            if count%500==0:
                print(f"{count} data processed")
            count+=1

def stevefunk(content,client,dataBase,collection):
    username = content.get("username", "")
    courseid = content.get("course_id", "")
    id = content.get("id", "")
    
    children = content.get("children", [])
    endorsed_responses = content.get('endorsed_reponses',[])
    non_endorsed_responses = content.get('non_endorsed_reponses',[])
    
    depth = content.get("depth", "?")
    print(f"{depth} {id} {courseid:30} {username}", flush=True)
    content['_id'] = id

    result = client[dataBase][collection].find_one({'_id' : id})
    if result is None:
        content.pop("children")
        content.pop("endorsed_responses")
        content.pop("non_endorsed_responses")
        client[dataBase][collection].insert_one(content)
    
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
    db = "mooc"
    collection = "fils"
    messageCollection= "messages"
    ImportMany(db,collection,filePath)
    ExtractMessage(db,collection,messageCollection)


if __name__=="__main__":
    #DoFullImport()
    ExtractMessage("mooc","fils","messages")