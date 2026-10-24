import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import DOSSIER_DATA


def dossier_graphiques():
    dossier = os.path.join(DOSSIER_DATA, "graphiques")
    os.makedirs(dossier, exist_ok=True)
    return dossier


class GraphiqueView:
    """Enregistre des graphiques PNG dans data/graphiques/."""

    def prix_moyen_par_marque(self, lignes, nom_fichier):
        """Renvoie le chemin du PNG, ou None s'il n'y a rien à dessiner."""
        lignes = [ligne for ligne in lignes if ligne["prix_moyen"] is not None]
        if not lignes:
            return None

        marques = [ligne["marque"] for ligne in lignes]
        prix = [ligne["prix_moyen"] for ligne in lignes]
        etiquettes = [
            f"{ligne['prix_moyen']:.2f} €\n({ligne['nombre']} produits)"
            for ligne in lignes
        ]

        figure, axe = plt.subplots(figsize=(8, 5))
        barres = axe.bar(marques, prix)
        axe.bar_label(barres, labels=etiquettes, padding=3)
        axe.set_title("Prix moyen par marque")
        axe.set_ylabel("Prix moyen (€)")
        axe.set_ylim(0, max(prix) * 1.25)
        figure.tight_layout()

        chemin = os.path.join(dossier_graphiques(), nom_fichier)
        figure.savefig(chemin, dpi=150)
        plt.close(figure)
        return chemin

    def evolution_prix(self, mot_cle, lignes, nom_fichier):
        """Renvoie le chemin du PNG, ou None s'il y a moins de 2 points."""
        points = [(ligne[0], ligne[2]) for ligne in lignes if ligne[2] is not None]
        if len(points) < 2:
            return None

        dates = [point[0] for point in points]
        moyennes = [point[1] for point in points]

        figure, axe = plt.subplots(figsize=(8, 5))
        axe.plot(range(len(dates)), moyennes, marker="o")
        axe.set_xticks(range(len(dates)))
        axe.set_xticklabels(dates, rotation=30, ha="right")
        axe.set_title(f"Évolution du prix moyen : {mot_cle}")
        axe.set_ylabel("Prix moyen (€)")
        axe.grid(True, alpha=0.3)
        figure.tight_layout()

        chemin = os.path.join(dossier_graphiques(), nom_fichier)
        figure.savefig(chemin, dpi=150)
        plt.close(figure)
        return chemin
