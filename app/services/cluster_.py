import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))  # Remonte jusqu'au dossier parent app
sys.path.append(parent_dir)


from bertopic import BERTopic
from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic.representation import KeyBERTInspired, MaximalMarginalRelevance, PartOfSpeech
from sentence_transformers import SentenceTransformer

import pandas as pd
import numpy as np
import ast
from app.db.postgre.db_connection import get_session

import google.generativeai as genai
from dotenv import load_dotenv

import pickle
import json
import re

# Charger les variables d'environnement depuis le .env
load_dotenv()

# Récupérer les messages et leurs embeddings depuis la base de données
def fetch_messages(limit=1000):
    """ 
        Récupérer les messages de la table message_vectorisation et de renvoyer une liste de chaines de caractères
        Args:
            limit (int): le nombre de messages à récupérer
    """
    query = f"""
        SELECT message, embedding_message
        FROM message_vectorization
        WHERE embedding_message IS NOT NULL
        LIMIT {limit};
    """

    with get_session() as session:
        bind = session.get_bind()
        df = pd.read_sql(query, bind)
        df["embedding_message"] = df["embedding_message"].apply(ast.literal_eval)
        messages = df["message"].tolist()
        embeddings = np.array(df["embedding_message"].tolist())
    return messages, embeddings

# Fonction pour le clustering des messages
# Utilise le modèle BERTopic pour regrouper les messages en fonction de leurs embeddings
def cluster_messages(messages, embeddings):
    topic_model = BERTopic(
        embedding_model=SentenceTransformer("paraphrase-MiniLM-L6-v2"),
        umap_model=UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric='cosine', random_state=42),
        hdbscan_model=HDBSCAN(min_cluster_size=30, metric='euclidean', prediction_data=True),
        vectorizer_model=CountVectorizer(min_df=2, ngram_range=(1, 2)),
        representation_model={
            "KeyBERT": KeyBERTInspired(),
            "MMR": MaximalMarginalRelevance(diversity=0.3),
            "POS": PartOfSpeech("fr_core_news_md"),
        },
        top_n_words=10,
        verbose=True
    )

    topics, probs = topic_model.fit_transform(messages, embeddings)
    return topic_model, topics

# Fonction pour générer des labels pour les topics
# Utilise le modèle Gemini pour générer des labels basés sur les mots-clés des topics

def generate_labels_with_gemini(topic_model):
    # 1) configure l’API
    genai.configure(api_key=os.getenv("SECRET_KEY_GEMINI"))

    # 2) config de génération
    gen_cfg = genai.GenerationConfig(
        temperature=0.7,
        max_output_tokens=512,
        top_p=0.95,
        top_k=40
    )

    # 3) instancie le modèle “flash”
    model = genai.GenerativeModel(
        "models/gemini-1.5-flash",
        generation_config=gen_cfg
    )

    # 4) collecte les topics + mots-clés
    info = topic_model.get_topic_info()
    lines = []
    for _, row in info.iterrows():
        tid = int(row["Topic"])
        if tid < 0:
            continue
        kws = ", ".join(w for w, _ in topic_model.get_topic(tid)[:5])
        lines.append(f"{tid}: {kws}")

    prompt = (
        "Voici mes thèmes identifiés (id: mots-clés). "
        "Pour chacun, propose un titre court et explicite. "
        "Réponds **uniquement** au format JSON `{id: label}`.\n\n"
        + "\n".join(lines)
    )

    # 5) appel à Gemini
    response = model.generate_content(prompt)

    # 6) on extrait le premier candidat quel que soit son attribut
    cand = None
    if hasattr(response, "candidates") and response.candidates:
        cand = response.candidates[0]
    elif hasattr(response, "generations") and response.generations:
        cand = response.generations[0][0]

    if cand is None:
        raise RuntimeError(f"Réponse inattendue de Gemini : {response!r}")

    # 7) récupère le contenu du candidat
    raw = getattr(cand, "output", None) or getattr(cand, "content", None) or getattr(cand, "text", None) or cand

    # 8) coercition en str pour la regex
    if not isinstance(raw, (str, bytes)):
        raw = str(raw)
    text = raw if isinstance(raw, str) else raw.decode()

    # 9) extrait le JSON entouré de ```json ...``` ou pas
    m = re.search(r"```json\s*(.*?)\s*```", text, flags=re.DOTALL)
    payload = m.group(1) if m else re.sub(r"^```(?:json)?|```$", "", text).strip()

    # 10) parse
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        print(" Impossible de parser la réponse JSON :", payload)
        return {}
    
# Fonction pour sauvegarder les resultats
# Enregistre le modèle BERTopic, les messages, les embeddings et les labels dans un répertoire spécifié
def save_results(topic_model, messages, embeddings, labels, output_dir="bertopic_output"):
    os.makedirs(output_dir, exist_ok=True)

    topic_model.save(os.path.join(output_dir, "bertopic_model"))
    with open(os.path.join(output_dir, "data.pkl"), "wb") as f:
        pickle.dump({"messages": messages, "embeddings": embeddings}, f)

    df = topic_model.get_topic_info()
    df["Label"] = df["Topic"].map(labels)
    df.to_csv(os.path.join(output_dir, "topics_with_labels.csv"), index=False)

    print(" Résultats enregistrés.")

# Fonction pour lister les modèles disponibles dans Gemini
# Utilise l'API de Gemini pour récupérer la liste des modèles disponibles
def list_gemini_models():
    genai.configure(api_key=os.getenv("SECRET_KEY_GEMINI"))
    models = list(genai.list_models())
    print("Modèles dispo :", [m for m in models])
    # ou pour ne montrer que les noms :
    # print("Modèles dispo :", [m.name for m in models])
    return models



if __name__ == "__main__":
    messages, embeddings = fetch_messages(1000)
    topic_model, topics = cluster_messages(messages, embeddings)
    labels = generate_labels_with_gemini(topic_model)
    
    # 1) On transforme ce dict en DataFrame
    df_labels = pd.DataFrame.from_dict(labels, orient="index", columns=["Label"])
    df_labels.index.name = "Topic"
    df_labels = df_labels.reset_index()  # on passe l'index Topic en colonne

    # 2) On fusionne avec ton DataFrame topics_info (le result_info retourné par get_clusters)
    df_topics = result_info.copy()  # ou topic_model.get_topic_info()
    df_labeled = df_topics.merge(df_labels, on="Topic", how="left")

    # 3) On l’affiche / sauve
    print(df_labeled.head())
    df_labeled.to_csv("topics_with_labels.csv", index=False)

    save_results(topic_model, messages, embeddings, labels)
    print("Clustering et étiquetage terminés.")
    
