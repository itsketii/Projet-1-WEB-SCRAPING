import argparse
import os
import sys

from app.controllers.controleur_scraping import ControleurScraping


def main():
    parseur = argparse.ArgumentParser(description="Scraping de résultats Amazon avec Selenium")
    parseur.add_argument("mot_cle", nargs="?",
                         help='produit recherché, ex. "écouteurs" (sans lui, le menu se lance)')
    parseur.add_argument("--local", metavar="FICHIER_HTML",
                         help="travailler sur une page déjà sauvegardée (aucune requête vers Amazon)")
    parseur.add_argument("--images", action="store_true",
                         help="télécharger aussi l'image de chaque produit")
    args = parseur.parse_args()

    if args.local and not os.path.exists(args.local):
        sys.exit(f"Fichier introuvable : {args.local}")

    controleur = ControleurScraping()
    if args.mot_cle is None:
        controleur.demarrer_menu()
    else:
        controleur.lancer(args.mot_cle, args.local, args.images)


if __name__ == "__main__":
    main()