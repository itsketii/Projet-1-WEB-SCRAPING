import os
import time


from app.scraper.telechargeur_images import telecharger_image
from config import DELAI_ATTENTE, HEADLESS, DOSSIER_DATA
from app.outils import slugifier
from app.scraper.scraper_amazon import ScraperAmazon
from app.views.export_view import ExportCSV
from app.models.depot_produits import DepotProduits
from app.views.vue_console import VueConsole



DOSSIER_PAGES = "pages"
PAUSE_IMAGES = 0.5   # temps de latence en secondes entre deux téléchargements


class ControleurScraping:

    def lancer(self, mot_cle, fichier_local=None, telecharger_images=False):
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

        self.depot.vider()
        self.depot.ajouter_tous(produits)

        if telecharger_images:
            self._telecharger_images(slug)

        ExportCSV(mot_cle).enregistrer(self.depot.tous())
        return self.depot.tous()


    def demarrer_menu(self):
        """Boucle du menu : tourne jusqu'à ce que l'utilisateur quitte."""
        while True:
            self.vue.afficher_menu()
            choix = self.vue.demander_choix()

            if choix == "1":
                mot_cle = self.vue.demander_mot_cle()
                if mot_cle:
                    images = self.vue.demander_oui_non("Télécharger les images ?")
                    self.lancer(mot_cle, telecharger_images=images)
                    self.vue.afficher_message(f"{len(self.depot)} produit(s) enregistré(s).")

            elif choix == "2":
                fichier = self.vue.demander_fichier()
                if not os.path.exists(fichier):
                    self.vue.afficher_message(f"Fichier introuvable : {fichier}")
                else:
                    nom_export = self.vue.demander_mot_cle()
                    images = self.vue.demander_oui_non("Télécharger les images ?")
                    self.lancer(nom_export or "page_locale", fichier, telecharger_images=images)
                    self.vue.afficher_message(f"{len(self.depot)} produit(s) enregistré(s).")

            elif choix == "3":
                self.vue.afficher_produits(self.depot.tous())

            elif choix == "0":
                self.vue.afficher_message("Au revoir !")
                break

            else:
                self.vue.afficher_message("Choix invalide.")


    def __init__(self):
        self.depot = DepotProduits()
        self.vue = VueConsole()


    def _telecharger_images(self, slug):
        """Télécharge l'image de chaque produit du dépôt dans data/images/<recherche>/."""
        dossier = os.path.join(DOSSIER_DATA, "images", slug)
        for numero, produit in enumerate(self.depot.tous(), start=1):
            produit.image_fichier = telecharger_image(
                produit.image_url, dossier, f"{numero:03d}.jpg")
            time.sleep(PAUSE_IMAGES)