import argparse
import os
import sys

from config import DELAI_ATTENTE, HEADLESS
import export_csv
from outils import slugifier
from scraper import ScraperAmazon

DOSSIER_PAGES = "pages"


def main():
    parseur = argparse.ArgumentParser(description="Scraping de résultats Amazon avec Selenium")
    parseur.add_argument("mot_cle", help='produit recherché, ex. "écouteurs"')
    parseur.add_argument("--local", metavar="FICHIER_HTML",
                         help="travailler sur une page déjà sauvegardée (aucune requête vers Amazon)")
    args = parseur.parse_args()

    slug = slugifier(args.mot_cle)

    if args.local:
        if not os.path.exists(args.local):
            sys.exit(f"Fichier introuvable : {args.local}")
        adresse = ScraperAmazon.url_fichier_local(args.local)
    else:
        adresse = ScraperAmazon.url_recherche(args.mot_cle)

    with ScraperAmazon(invisible=HEADLESS) as robot:
        robot.ouvrir(adresse)
        trouve = robot.attendre_resultats(DELAI_ATTENTE)

        if not args.local:
            nom = f"{slug}.html" if trouve else f"{slug}_bloque.html"
            robot.sauvegarder_html(os.path.join(DOSSIER_PAGES, nom))

        produits = robot.extraire_tous() if trouve else []

    exporteur = getattr(export_csv, "ExportCSV")
    exporteur(args.mot_cle).enregistrer(produits)


if __name__ == "__main__":
    main()