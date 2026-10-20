import os

from config import DELAI_ATTENTE, HEADLESS
from app.outils import slugifier
from app.scraper.scraper_amazon import ScraperAmazon
from app.views.export_view import ExportCSV

DOSSIER_PAGES = "pages"


class ControleurScraping:

    def lancer(self, mot_cle, fichier_local=None):
        """Scrape (ou relit une page locale) puis exporte les produits en CSV."""
        slug = slugifier(mot_cle)

        if fichier_local:
            adresse = ScraperAmazon.url_fichier_local(fichier_local)
        else:
            adresse = ScraperAmazon.url_recherche(mot_cle)

        with ScraperAmazon(invisible=HEADLESS) as robot:
            robot.ouvrir(adresse)
            trouve = robot.attendre_resultats(DELAI_ATTENTE)

            if not fichier_local:
                nom = f"{slug}.html" if trouve else f"{slug}_bloque.html"
                robot.sauvegarder_html(os.path.join(DOSSIER_PAGES, nom))

            produits = robot.extraire_tous() if trouve else []

        ExportCSV(mot_cle).enregistrer(produits)
        return produits