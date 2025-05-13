from database import SessionLocal
from sqlalchemy import text


def db_connection():
    """create a new sesssion to the database"""
    
    try:
        db = SessionLocal()
        db.execute(text("select 1"))
        print("Connexion reussie")
    except Exception as e :
        print("Erreur de connexion à la base de données :", e)
       
    finally:
        db.close()
    return 


# Test de la connexion à la base de données
# def test_db_connection():
if __name__ == "__main__":
    db_connection()