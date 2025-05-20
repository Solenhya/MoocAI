from app.db.postgre import embedding
from dotenv import load_dotenv
from app.services import sentiment_tabularisai
import sys
import traceback

def launchSentiment():
    try:
        load_dotenv()
        sentiment_tabularisai.InitialiseModele()
        sentiment_tabularisai.AddSentiment()
        print("Insertion faite")
    except Exception as e:
        print(f"Erreur dans l'insertion du sentiment : {e}")
        
    # Get traceback details
        exc_type, exc_value, exc_traceback = sys.exc_info()
        tb = traceback.extract_tb(exc_traceback)

    # Print full traceback info
        for filename, lineno, func, text in tb:
            print(f"Exception occurred in {filename}, line {lineno}, in {func}")
            print(f"    Code: {text}")



if __name__ == "__main__":
    launchSentiment()