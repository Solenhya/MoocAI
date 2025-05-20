from pymongo import UpdateOne
from .mongoConnection import GetConnection
# Set up an empty list to hold update operations
updates = []
client = GetConnection()
try:
    collection = client["G4"]["messages"]
    cursor = collection.find()
    print(f"Connection Creer")
    # Counter to create a sequential field
    seq_number = 1

    for doc in cursor:
        # Prepare the update operation
        updates.append(UpdateOne(
            {"_id": doc["_id"]},  # match by the document's _id
            {"$set": {"seq_number": seq_number}}  # set the sequential field
        ))
        # Increment the counter
        seq_number += 1
        # If the list grows large, execute in batches to prevent memory overload
        if len(updates) >= 1000:  # Adjust batch size as needed
            collection.bulk_write(updates)
            updates = []  # Clear the list for the next batch
            print(f"Updated in bulk {seq_number} done")
    # Final batch
    if updates:
        collection.bulk_write(updates)
    print("Sequence ajoutée")
    collection.create_index([("seq_number", 1)]) 
    print("Index créer")
except Exception as e:
    print(f"Erreur : {e}")
finally:
    client.close()