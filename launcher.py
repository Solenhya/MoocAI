from app.db.postgre import embedding
from dotenv import load_dotenv
import os



def main():
    try:
        # Load environment variables from .env file
        load_dotenv()
        embedding.insert_emded_all()
        print("insertion done")
    except Exception as e :
        print("Error during insertion:", e)

if __name__ == "__main__":
    main()