import math
from mongoConnection import GetConnection

def Iterator(collection,filter,projection,session,dbName,chunksize=10000):
    count = collection.count_documents(filter)
    slices = math.ceil(count/chunksize)
    start_from= 0
    for iteration in range(slices):
        cursor = session[dbName][collection].find(filter=filter,projection=projection).skip(start_from).limit(chunksize)
        yield cursor
        start_from+=chunksize

def IterateCheckPoint(collection,filter,projection,session,dbName,chunksize=1000,last_seen_seq=None):
    query_filter = dict(filter)  # Avoid mutating original filter
    if last_seen_seq:
        query_filter["seq_number"] = {"$gt": last_seen_seq}  # Query for seq_number greater than last_seen_seq
    #TODO
    
