#  SmartMooc — Analyse intelligente des forums de MOOC
SmartMooc est une application d’intelligence artificielle destinée à analyser, structurer et enrichir l’expérience des forums pédagogiques dans les MOOCs.  

---
## Installation
Version de python requise : 3.12
```bash
python -m venv venv
source venv\Scritps\activate (linux: venv/bin/activate)
pip install -r requirements.txt
cd app
fastapi run main.py
```
## Fonctionallité
  - **Message similaire**: Explorer les messages par similarité
  - **Dashboard Message**: Des informations sur le message : Auteur , Sentiment

## Technologies utilisées

- **FastAPI**, **MongoDB**, **PostgreSQL/pgvector**
- **spaCy**, **Transformers** , **gemini**
- **Pandas, Scikit-learn, UMAP, HDBSCAN**
- **Jinja2 / HTML / JS** (pour le front ou dashboard)
