import math
from .mongoConnection import GetConnection

def Iterator(collection,filter,projection,session,dbName,chunksize=10000):
    count = collection.count_documents(filter)
    slices = math.ceil(count/chunksize)
    start_from= 0
    for iteration in range(slices):
        cursor = session[dbName][collection].find(filter=filter,projection=projection).skip(start_from).limit(chunksize)
        yield cursor
        start_from+=chunksize

def IterateCheckPoint(collectionName,filter,projection,session,dbName,chunksize=1000,operationName=None,last_seen_seq=None):
    query_filter = dict(filter)  # Fait une copy du filtre pour ne pas la transformer
    projection["seq_number"]=1
    collection = session[dbName][collectionName]
    checkpointCollection = session[dbName]["checkpoints"]
    if operationName:
        checkpoint = checkpointCollection.find_one({"operation":operationName})
        if checkpoint:
            last_seen_seq=checkpoint.get("checkpoint")
        else:
            ajout = {"operation":operationName,"checkpoint":0}
            checkpointCollection.insert_one(ajout)
    if last_seen_seq:
        query_filter["seq_number"] = {"$gt": last_seen_seq}  # Ne récupere que les documents pas encore traité
    while True:  # Boucle infini
        # Recupere un batch de document en odre croissant de seq
        cursor = collection.find(
            filter=query_filter,
            projection=projection
        ).sort("seq_number", 1).limit(chunksize)
        docs = list(cursor)  # Converti en liste
        if not docs:  # Si on ne récupere pas de liste c'est qu'on est a la fin
            break 
        yield docs# Yield ce batch de document
        last_seen_seq = docs[-1]['seq_number']  # Mets a jour le dernier vu
        if operationName:#Si on a un nom d'opération on mets a jour le checkpoint dans la base de donnée
            checkpointCollection.update_one({"operation":operationName},{"$set":{"checkpoint":last_seen_seq}})
        query_filter["seq_number"] = {"$gt": last_seen_seq}  # Mets a jour le filtre pour le prochain passage
#Exemple d'utilisation :
"""
# Iteration en local
for batch in seq_checkpointed_generator(collection, filter={}, projection={"_id": 1, "seq_number": 1}, chunksize=10000, last_seen_seq=last_checkpoint_seq):
    # Process les document de la liste
    for doc in batch:
        print(doc)  # Process the document as needed
    
    # Apres process on doit gerer nous meme le checkpoint
    last_checkpoint_seq = batch[-1]['seq_number']  
    with open(filename,"w") as file:
        file.write(str(batch[-1]["seq_number"]))

#Iteration en base de donnée
for batch in seq_checkpointed_generator(collection, filter={}, projection={"_id": 1, "seq_number": 1}, chunksize=10000, last_seen_seq=last_checkpoint_seq,operationName="Itere"):
    # Process les document de la liste
    for doc in batch:
        print(doc)  # Process the document as needed
    """
    



