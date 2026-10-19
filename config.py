import os

from dotenv import load_dotenv

# Lit le fichier .env et charge son contenu dans les variables d'environnement
load_dotenv()

# Chaque réglage a une valeur par défaut afin que le programme marche même sans .env
DOSSIER_DATA = os.getenv("DOSSIER_DATA", "data")
HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
DELAI_ATTENTE = int(os.getenv("DELAI_ATTENTE", "15"))