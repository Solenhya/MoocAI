from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables
key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=key)

#Taille 768
def getembedding(text:str):
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text,
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
    )
    return result.embeddings[0].values