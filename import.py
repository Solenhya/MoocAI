import pymongo
import json
import mongoConnection

def ImportMany(dbName,collectionName,filePath):
    myclient = mongoConnection.GetConnection()
    data=[]
    with open(filePath,"r",encoding='utf-8') as file:
        for line in file:
            data.append(json.loads(line))
    db = myclient[dbName]
    print(db)
    collection = db[collectionName]
    print(f"Collection {collection}")
    count =0
    total = len(data)
    for i in data:
        id = i["_id"]
        if(mongoConnection.FindId(id)==None):
            collection.insert_one(i)
            print(f"Inserted data : {count}/{total}")
        count+=1


if __name__=="__main__":
    filePath = "MOOC_forum.json"
    db = "mooc"
    collection = "test"
    ImportMany(db,collection,filePath)