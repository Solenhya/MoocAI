from os.path import  dirname
import os
import sys

# Add the app directory to sys.path so Alembic can find your modules
sys.path.append(dirname(dirname(__file__)))  # this moves up from alembic/ to app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from sqlalchemy import Column, Integer, String, DateTime
from postgre.database import Base
from sqlalchemy.sql import func

# Importer le type VECTOR
from pgvector.sqlalchemy import Vector

# créer  une classe de modèle pour la table de vectorisation des messages
class MessageVectorization(Base):
    __tablename__= "message_vectorization"
    id_message = Column(String, primary_key=True, index=True)
    message = Column(String, nullable=False)
    embedding_message = Column(Vector(768), nullable=False) # adapter au modèle Gemini
    date_vectorization = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

