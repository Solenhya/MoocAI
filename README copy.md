#  SmartMooc — Analyse intelligente des forums de MOOC

**SmartMooc** est une application d’intelligence artificielle destinée à **analyser, structurer et enrichir l’expérience des forums pédagogiques** dans les MOOCs.  
Elle permet d’aider les apprenants à retrouver des informations pertinentes, tout en fournissant aux encadrants un outil de **monitoring intelligent**.

---

##  Objectifs du projet

L'application a pour but de :
- **Répondre intelligemment** aux questions d’un utilisateur en analysant les fils de discussion (RAG)
- **Regrouper les discussions par thématiques** automatiquement (clustering)
- **Analyser le sentiment** des messages dans un fil de discussion
- **Identifier des participants similaires** en fonction de leurs interactions (cours suivis, réponses aux mêmes discussions…)

---

## Fonctionnalités principales

| Fonction | Description |
|---------|-------------|
|**Recherche intelligente de discussions** | L’utilisateur pose une question libre ; le système retrouve les fils liés (via recherche sémantique + RAG) |
|**Clustering automatique** | Les fils sont regroupés automatiquement par similarité thématique |
|**Validation de la classification manuelle** | L’application évalue si le champ `courseware_title` est cohérent avec les regroupements obtenus |
|**Analyse de sentiment** | Sur un fil de discussion sélectionné, le système retourne les sentiments dominants des messages |
|**Recherche de participants similaires** | Trouver les utilisateurs ayant eu un comportement/forum/cours similaires |

---

## Architecture fonctionnelle

![Schéma fonctionnel](docs/schema_fonctionnel.png)

- **Frontend** : Interface utilisateur pour l’exploration, les recherches et le monitoring
- **FastAPI** : Orchestrateur des traitements (backend)
- **PostgreSQL** : Stockage structuré des utilisateurs, logs, résultats et embeddings
- **MongoDB** : Stockage des messages de forum bruts et non structurés
- **Services IA** :
  - Sentiment Analysis
  - Clustering des fils
  - RAG pour répondre aux questions libres
  - Recherche de proximité entre participants

---

## Pipeline de traitement

1. **Import des données forum** (`forum_old`)
2. **Nettoyage et structuration** (`MongoDB`)
3. **Indexation des messages pour recherche sémantique** (embeddings → PostgreSQL)
4. **Traitements IA** :
   - RAG (retrieval puis génération)
   - Clustering (UMAP + HDBSCAN ou KMeans)
   - Analyse de sentiment (Transformers ou TextBlob)
   - Recherche de similarité entre utilisateurs
5. **Exposition via API et frontend**

---

## Technologies utilisées

- **FastAPI**, **MongoDB**, **PostgreSQL**
- **spaCy**, **Transformers**, **Faiss / Annoy / pgvector**
- **Pandas, Scikit-learn, UMAP, HDBSCAN**
- **Jinja2 / HTML / JS** (pour le front ou dashboard)

---

## Structure projet proposée

```
smartmooc/
├── api/                     # Backend FastAPI
│   └── routes.py
├── services/
│   ├── sentiment.py
│   ├── clustering.py
│   ├── rag.py
│   └── similarity.py
├── database/
│   ├── postgresql/
│   └── mongodb/
├── data/
│   ├── raw/
│   └── processed/
├── models/
│   └── embeddings/
├── frontend/
│   └── templates/
├── notebooks/
│   └── exploration.ipynbzéa
├── README.md
└── requirements.txt
```

---

## Lancer le projet

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn api.routes:app --reload
```
## Instalation
```bash
  # Installation de l'extension pgvectot
  pip install pgvector

  # Installer sentence-transformers
  pip install -U sentence-transformers
```