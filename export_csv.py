import csv
import os
from dataclasses import asdict, fields
from datetime import datetime

from config import DOSSIER_DATA
from outils import slugifier
from produit import Produit


class ExportCSV:
    """Ecrit les produits extraits dans un fichier CSV."""

    def __init__(self, mot_cle):
        self.mot_cle = mot_cle

    def enregistrer(self, produits):
        os.makedirs(DOSSIER_DATA, exist_ok=True)
        horodatage = datetime.now().strftime("%Y%m%d_%H%M%S")
        nom_fichier = f"{slugifier(self.mot_cle)}_{horodatage}.csv"
        chemin = os.path.join(DOSSIER_DATA, nom_fichier)
        noms_champs = [champ.name for champ in fields(Produit)]

        with open(chemin, "w", newline="", encoding="utf-8-sig") as fichier:
            ecrivain = csv.DictWriter(fichier, fieldnames=noms_champs)
            ecrivain.writeheader()
            if produits:
                ecrivain.writerows(asdict(produit) for produit in produits)

        print(f"{len(produits)} produit(s) exporté(s) dans {chemin}")