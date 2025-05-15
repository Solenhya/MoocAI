from os.path import  dirname, abspath
import os
import sys

# Add the app directory to sys.path so Alembic can find your modules
sys.path.append(dirname(dirname(__file__)))  # this moves up from alembic/ to app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app')))

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from postgre.database import Base
from sqlalchemy.sql import func


# créer  une classe de modèle pour la table de vectorisation des messages
class MessageVectorization(Base):
    __tablename__= "message_vectorization"
    id_message = Column(Integer, primary_key=True, index=True)
    message = Column(String, index=True, nullable=False)
    embedding_message = Column(String, index=True, nullable=False)
    date_vectorization = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


