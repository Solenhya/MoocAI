
#http://localhost:11434/api/embed -d '{"model": "snowflake-arctic-embed:22m", "keep_alive": -1, "input":"Hello, ceci est mon message"}'

import requests
import json

model = "snowflake-arctic-embed:22m"
url = "http://localhost:11434/api/embed"

#Length 384 .... donc pas utilisable sur la meme table
def get_embedding(text:str):
    payload = {
    "model": model,
    "keep_alive": -1,
    "input": text
    }
    response = requests.post(url, json=payload)
    retour = response.json()["embeddings"]
    return retour,response

if __name__ == "__main__":
    test = "Bonjour le monde"
    retour,reponse = get_embedding(test)
    print(len(retour[0]))