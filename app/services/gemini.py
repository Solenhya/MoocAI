from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables
key = os.getenv("SECRET_KEY_GEMINI")
client = genai.Client(api_key=key)

#Taille 768
def getembedding(text:str):
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    )
    return result.embeddings[0].values


if __name__ == "__main__":
    # Exemple d'utilisation
    text = "Bonjour, comment ça va ?"
    embedding = getembedding(text)
    print(len(embedding))
    # Afficher l'embedding
    print(embedding)