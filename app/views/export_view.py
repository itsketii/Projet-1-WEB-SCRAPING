import csv
import os

from config import DOSSIER_DATA, FAMILLE
from app.models.base_sqlite import COLONNES
from app.models.statistiques import calculer_statistiques


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


class ExportRecap:
    """Tient à jour data/recap.csv : une ligne par catégorie scrapée."""

    ENTETE = ["nb_total_categories_scrapees", "categorie", "nombre_produits",
              "prix_moyen", "prix_max", "prix_min"]

    def __init__(self):
        self.chemin = os.path.join(DOSSIER_DATA, "recap.csv")

    def mettre_a_jour(self, slug, produits):
        """Ajoute ou remplace la ligne de la catégorie, puis réécrit le fichier."""
        if not produits:
            return
        stats = calculer_statistiques(produits)

        def arrondi(valeur):
            return "" if valeur is None else round(valeur, 2)

        lignes = self._lire()
        lignes[slug] = {
            "nombre_produits": stats["nombre"],
            "prix_moyen": arrondi(stats["prix_moyen"]),
            "prix_max": arrondi(stats["prix_max"]),
            "prix_min": arrondi(stats["prix_min"]),
        }
        self._ecrire(lignes)

    def _lire(self):
        lignes = {}
        if os.path.exists(self.chemin):
            with open(self.chemin, newline="", encoding="utf-8-sig") as fichier:
                for ligne in csv.DictReader(fichier):
                    lignes[ligne["categorie"]] = ligne
        return lignes

    def _ecrire(self, lignes):
        os.makedirs(DOSSIER_DATA, exist_ok=True)
        total = len(lignes)
        with open(self.chemin, "w", newline="", encoding="utf-8-sig") as fichier:
            ecrivain = csv.writer(fichier)
            ecrivain.writerow(self.ENTETE)
            for categorie in sorted(lignes):
                ligne = lignes[categorie]
                ecrivain.writerow([total, categorie, ligne["nombre_produits"],
                                   ligne["prix_moyen"], ligne["prix_max"], ligne["prix_min"]])