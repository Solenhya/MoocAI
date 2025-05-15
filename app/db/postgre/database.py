from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

"""
Module de connexion à la base de données PostgreSQL.
Ce module utilise SQLAlchemy pour établir une connexion à la base de données PostgreSQL.
==> Contient la configuration et l’objet de connexion SQLAlchemy (c'est la "source de vérité").
"""

# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# connexion à postgreSQL
HOST = os.getenv("HOST")
USER = os.getenv("USER")
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")
PASSWORD = os.getenv("PASSWORD")

# Vérifier si toutes les variables d'environnement sont définies
if not all([HOST, USER, DATABASE, PORT, PASSWORD]):
    raise ValueError("Une ou plusieurs variables d'environnement ne sont pas définies.")

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Vérifier si l'URL de la base de données est définie
if not DATABASE_URL:
    raise ValueError("DATABASE_URL n'est pas définie dans la variable d'environnement.")

# Créer un engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo = True) # echo=True pour afficher les requêtes SQL dans la console

# Créer une session SQLAlchemy
SessionLocal = sessionmaker(bind=engine)

# Créer une base ORM pour déclarer les modèles
Base = declarative_base()

