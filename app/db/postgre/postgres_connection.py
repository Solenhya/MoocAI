from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv


# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# connexion à postgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Vérifier si l'URL de la base de données est définie
if not DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas définie dans la variable d'environnement.")

# Créer un engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo = True) # echo=True pour afficher les requêtes SQL dans la console

# Créer une session SQLAlchemy
SessionLocal = sessionmaker(bind=engine)

# Créer une base ORM pour déclarer les modèles
Base = declarative_base()

