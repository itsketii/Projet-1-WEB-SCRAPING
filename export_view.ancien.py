import csv
import os

from config import DOSSIER_DATA, FAMILLE
from app.models.base_sqlite import COLONNES


def dossier_categorie(slug):
    """data/tech/<catégorie>"""
    return os.path.join(DOSSIER_DATA, FAMILLE, slug)


class ExportCSV:
    """Écrit les produits d'une catégorie dans data/<famille>/<catégorie>/data.csv."""

    def __init__(self, slug):
        self.slug = slug
        self.dossier = dossier_categorie(slug)

    def enregistrer(self, produits):
        os.makedirs(self.dossier, exist_ok=True)
        chemin = os.path.join(self.dossier, "data.csv")

        with open(chemin, "w", newline="", encoding="utf-8-sig") as fichier:
            ecrivain = csv.writer(fichier)
            ecrivain.writerow(COLONNES)
            for produit in produits:
                ecrivain.writerow([getattr(produit, colonne, None) for colonne in COLONNES])

        print(f"{len(produits)} produit(s) exporté(s) dans {chemin}")
        return chemin