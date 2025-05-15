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
    while True:  # This starts an infinite loop
        # Fetch a batch of documents sorted by seq_number
        cursor = collection.find(
            filter=query_filter,
            projection=projection
        ).sort("seq_number", 1).limit(chunksize)
        docs = list(cursor)  # Convert cursor to a list (to load the documents)
        if not docs:  # This condition checks if the cursor is empty (i.e., no more documents)
            break  # If no more documents are found, we break the loop and stop the generator
        # Yield the current batch of documents
        yield docs
        # Update the last_seen_seq for the next batch
        last_seen_seq = docs[-1]['seq_number']  # Update last_seen_seq for the next iteration
        query_filter["seq_number"] = {"$gt": last_seen_seq}  # Set the filter for the next batch

#Exemple d'utilisation :
"""
# Iterate through the batches of documents
for batch in seq_checkpointed_generator(collection, filter={}, projection={"_id": 1, "seq_number": 1}, chunksize=10000, last_seen_seq=last_checkpoint_seq):
    # Process each batch of documents
    for doc in batch:
        print(doc)  # Process the document as needed
    
    # After processing, update the last_seen_seq for the next iteration
    last_checkpoint_seq = batch[-1]['seq_number']  # Save the last seq_number"""
    
