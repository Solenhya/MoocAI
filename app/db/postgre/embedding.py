import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # Remonte jusqu'au dossier parent app
sys.path.append(parent_dir)

from db.postgre.models import MessageVectorization
from services.gemini import getembedding
from db_connection import get_session
from sqlalchemy.dialects.postgresql import insert
from db.mongoDB import mongoConnection

def getembed_one(message: str):
    message_vector = MessageVectorization(message=message)
    # Récupérer l'embedding
    embedding = getembedding(message_vector.message)
    # Mettre à jour l'objet message_vector avec l'embedding
    message_vector.embedding_message = embedding
    return message_vector 


def insert_embed_(db,id_message: str, message: str):
    message_vector = getembed_one(id_message, message)
    db.add(message_vector)
    db.commit()


def insert_embed_one(db, messages: list):
    messages_vectorization = {
        'id_message': messages.id,
        'message': messages.message,
        'embedding_message': messages.embedding_message,
        'date_vectorization': messages.date
    }

    insert_messages = insert(MessageVectorization).values(messages_vectorization)
    insert_messages = insert_messages.on_conflict_do_update(
        indexelements=['id'],
        set={
            'name': insert_messages.excluded.name,
            'email': insert_messages.excluded.email
        }
    )

    db.execute(insert_messages)
    db.commit() 

# Insérer tous les messages de MongoDB dans PostgreSQL
# en utilisant la fonction d'insertion
def insert_emded_all():
    client = mongoConnection.GetConnection()
    # Récupérer les messages de MongoDB
    cussor_messages = mongoConnection.Find("messages", projection={"_id": 1, "body":1}, client=client)
    # Insérer les messages dans PostgreSQL
    with get_session() as db:
        compteur = 0
        for doc in cussor_messages:
            insert_embed_one(db, doc["_id"], doc["body"])
            compteur+=1
            if compteur % 100 == 0:
                print(f"Inserted {compteur} messages into postgresql")
    client.close()


