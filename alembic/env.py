from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from os.path import  dirname
import os
import sys
from pathlib import Path

# Add the app directory to sys.path so Alembic can find your modules
BASE_DIR = Path(__file__).resolve().parent.parent  # MoocAI/
APP_DIR = BASE_DIR / "app"
sys.path.append(str(APP_DIR))

from dotenv import load_dotenv
from app.db.postgre.database import Base  # <- ton Base
from app.db.postgre.models import  MessageVectorization # importe le.s  modèle.s
from dotenv import load_dotenv


# Charger les variables d'environnement à partir du fichier .env
load_dotenv()

# Charger les variables d'environnement
HOST = os.getenv("HOST")
USER = os.getenv("USER")  
DATABASE = os.getenv("DATABASE")
PORT = os.getenv("PORT")
PASSWORD = os.getenv("PASSWORD")
DATABASE_URL = os.getenv("DATABASE_URL")

# L' URL de la base de données est construite à partir des variables d'environnement

DATABASE_URL = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from app.db.postgre import models
target_metadata = models.Base.metadata  # <- le Base.metadata du système de gestion de base de données

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
