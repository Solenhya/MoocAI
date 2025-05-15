from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os




#enbeding avec le modele SentenceTransformer
def getembed_senTransf(messages: list):
    model = SentenceTransformer('all-MiniLM-L6-v2')  # Modèle de Sentence Transformers utilisé
    embedder = model.encode(phrases, show_progress_bar = True)

