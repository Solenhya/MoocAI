import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')) # Remonte jusqu'au dossier parent app
sys.path.append(parent_dir)

from db.postgre.models import MessageVectorization
from services.gemini import getembedding
from db.postgre.db_connection import get_session
from sqlalchemy.dialects.postgresql import insert
from db.mongoDB import mongoConnection
from db.mongoDB import iterator
from utils.time_estimation import EstimateRemaining
import time


# embeddding avec le modèle Gemini   
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


def insert_embed_one(db, message_id: str, message: str,waiting=None,callBefore=None):
    # Récupérer l'embedding
    if waiting and callBefore:
        time_now = time.perf_counter()
        difference = time_now-callBefore
        if(difference<waiting):
            time.sleep(waiting-difference)
            #print(f"waited {waiting-difference}")
        time_before= time.perf_counter()
    message_embed = getembedding(message)
    messages_vectorization = {
        'id_message': message_id,
        'message': message,
        'embedding_message': message_embed
    }

    insert_messages = insert(MessageVectorization).values(messages_vectorization)
    insert_messages = insert_messages.on_conflict_do_update(
        index_elements=['id_message'],
        set_={
            'message': insert_messages.excluded.message,
            'embedding_message': insert_messages.excluded.embedding_message,
            'date_vectorization': insert_messages.excluded.date_vectorization
        }
    )

    db.execute(insert_messages)
    db.commit() 
    if waiting:
        return time_before

# Insérer tous les messages de MongoDB dans PostgreSQL
# en utilisant la fonction d'insertion
def insert_emded_all():
    client = mongoConnection.GetConnection()
    print("Connection MongoDB OK")
    # Récupérer les messages de MongoDB
    cussor_messages = mongoConnection.Find("messages", projection={"_id": 1, "body":1}, client=client)
    print(cussor_messages)
    print("Récupération des messages de MongoDB OK")
    # Afficher le nombre de messages récupérés
    # Insérer les messages dans PostgreSQL
    with get_session() as db:
        compteur = 0
        for doc in cussor_messages:
            insert_embed_one(db, doc["_id"], doc["body"])
            compteur+=1
            if compteur % 100 == 0:
                print(f"Inserted {compteur} messages into postgresql")
    client.close()

def insert_all_checkpoint():
    filename = "checkpoint.txt"
    checkpoint=None
    start =0
    #On creer la connection mongo
    client = mongoConnection.GetConnection()
    numberDoc = mongoConnection.GetCount("messages","G4",client)
    print(f"Traitement de {numberDoc} documents")
    #La ou en est dans le traitement des fichiers
    compteur = 0
    timestart = time.time()
    #Si le fichier checkpoint exist on lis le dernier checkpoint atteint
    if os.path.exists(filename):
        with open(filename, "r") as file:
            checkpoint = int(file.read())
            print(f"Reprise de l'import depuis le checkpoint {checkpoint}")
            compteur = checkpoint
            start = checkpoint
    #On définit les information necessaire a la restriction API
    waiting = 0.455
    timer = time.perf_counter()
    #Dans le context d'une session postgreSQL avec pgVector
    with get_session() as db:
        #On récuperer une liste de document de la collection messages
        for batch in iterator.IterateCheckPoint("messages", filter={}, projection={"_id": 1, "body": 1,"seq_number":1},session=client,dbName=os.getenv("MONGO_DBNAME"),chunksize=100, last_seen_seq=checkpoint):
            for doc in batch:
                #On les insere un par un
                timer = insert_embed_one(db, doc["_id"], doc["body"],waiting=waiting,callBefore=timer)
                currentTime = time.time()
                timeleft = EstimateRemaining(start=start,current=compteur,required=numberDoc,timed=currentTime-timestart)
                compteur+=1
                if compteur % 10 == 0:
                    print(f"Inserted {compteur}/{numberDoc} messages into postgresql en {currentTime-timestart:.2f}s il reste environ {timeleft:.2f}s")
            #On écrit dans le checkpoint le dernier checkpoint atteint
            with open(filename,"w") as file:
                file.write(str(batch[-1]["seq_number"]))


if __name__ == "__main__":
    # Exemple d'utilisation
    # message = "Bonjour, comment ça va ?"
    # embedding = getembed_one(message)
    # print(len(embedding))
    # Afficher l'embedding
    # print(embedding)
    insert_emded_all()