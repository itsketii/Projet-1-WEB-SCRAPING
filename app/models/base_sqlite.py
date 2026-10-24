import os
import sqlite3
from contextlib import closing
from datetime import datetime

from app.models.statistiques import convertir_prix

COLONNES = [
    "nom", "description", "prix", "prix_original", "note", "avis", "ventes",
    "livraison", "prix_livraison", "image_url", "image_fichier",
    "stock_limite", "offre_limitee",
]
COLONNES_OUI_NON = ("stock_limite", "offre_limitee")

SCHEMA = """
CREATE TABLE IF NOT EXISTS recherches (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    mot_cle TEXT NOT NULL,
    date    TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS produits (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    recherche_id   INTEGER NOT NULL REFERENCES recherches(id),
    nom            TEXT,
    description    TEXT,
    prix           TEXT,
    prix_original  TEXT,
    note           TEXT,
    avis           TEXT,
    ventes         TEXT,
    livraison      TEXT,
    prix_livraison TEXT,
    image_url      TEXT,
    image_fichier  TEXT,
    stock_limite   INTEGER,
    offre_limitee  INTEGER,
    prix_num       REAL
);
"""


class BaseSQLite:
    """Enregistre les recherches et leurs produits dans un fichier SQLite."""

    def __init__(self, chemin):
        self.chemin = chemin
        dossier = os.path.dirname(chemin)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        with closing(sqlite3.connect(self.chemin)) as connexion:
            connexion.executescript(SCHEMA)
            connexion.commit()

    def enregistrer(self, mot_cle, produits):
        """Crée une recherche et y rattache les produits. Renvoie l'id de la recherche."""
        colonnes = ["recherche_id"] + COLONNES + ["prix_num"]
        requete = (f"INSERT INTO produits ({', '.join(colonnes)}) "
                   f"VALUES ({', '.join('?' * len(colonnes))})")

        with closing(sqlite3.connect(self.chemin)) as connexion:
            curseur = connexion.execute(
                "INSERT INTO recherches (mot_cle, date) VALUES (?, ?)",
                (mot_cle, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            recherche_id = curseur.lastrowid

            for produit in produits:
                valeurs = []
                for champ in COLONNES:
                    valeur = getattr(produit, champ, None)
                    if champ in COLONNES_OUI_NON:
                        valeur = int(bool(valeur))
                    valeurs.append(valeur)
                valeurs.append(convertir_prix(produit.prix))
                connexion.execute(requete, (recherche_id, *valeurs))

            connexion.commit()
        return recherche_id

    def lister_recherches(self):
        """Renvoie des tuples (id, mot_cle, date, nombre de produits), la plus récente d'abord."""
        with closing(sqlite3.connect(self.chemin)) as connexion:
            return connexion.execute(
                "SELECT r.id, r.mot_cle, r.date, COUNT(p.id) "
                "FROM recherches r LEFT JOIN produits p ON p.recherche_id = r.id "
                "GROUP BY r.id ORDER BY r.id DESC").fetchall()

    def lister_mots_cles(self):
        """Renvoie des tuples (mot_cle, nombre de recherches), les plus fréquents d'abord."""
        with closing(sqlite3.connect(self.chemin)) as connexion:
            return connexion.execute(
                "SELECT mot_cle, COUNT(*) FROM recherches "
                "GROUP BY mot_cle ORDER BY COUNT(*) DESC, mot_cle").fetchall()

    def evolution_prix(self, mot_cle):
        """Pour chaque recherche d'un mot-clé (de la plus ancienne à la plus récente),
        renvoie (date, nombre de prix, prix moyen, prix minimum, prix maximum)."""
        with closing(sqlite3.connect(self.chemin)) as connexion:
            return connexion.execute(
                "SELECT r.date, COUNT(p.prix_num), AVG(p.prix_num), "
                "       MIN(p.prix_num), MAX(p.prix_num) "
                "FROM recherches r JOIN produits p ON p.recherche_id = r.id "
                "WHERE r.mot_cle = ? GROUP BY r.id ORDER BY r.id", (mot_cle,)).fetchall()   