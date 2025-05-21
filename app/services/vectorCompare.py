from . import gemini
from sqlalchemy import select, literal
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Remonte jusqu'au dossier parent app
sys.path.append(parent_dir)

from db.postgre.db_connection import get_session
from db.postgre.models import MessageVectorization
from pgvector.sqlalchemy import Vector

def getSimilar(text:str,limit:int,session):
    # Query vector (a list or numpy array of floats)
    query_vector = gemini.getembedding(text)

    # Create a literal vector for the query vector
    query_vector_literal = literal(query_vector).cast(Vector(768))

    # Construct the query using the '<=>' cosine distance operator
    results = session.scalars(select(MessageVectorization).order_by(MessageVectorization.embedding_message.cosine_distance(query_vector_literal)).limit(limit))
    print(results)
    return results