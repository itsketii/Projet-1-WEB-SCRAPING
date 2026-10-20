import argparse
import os
import sys

from app.controllers.controleur_scraping import ControleurScraping


def main():
    parseur = argparse.ArgumentParser(description="Scraping de résultats Amazon avec Selenium")
    parseur.add_argument("mot_cle", help='produit recherché, ex. "écouteurs"')
    parseur.add_argument("--local", metavar="FICHIER_HTML",
                         help="travailler sur une page déjà sauvegardée (aucune requête vers Amazon)")
    args = parseur.parse_args()

    if args.local and not os.path.exists(args.local):
        sys.exit(f"Fichier introuvable : {args.local}")

    ControleurScraping().lancer(args.mot_cle, args.local)


if __name__ == "__main__":
    main()