import os
import time
from datetime import datetime


from app.models.base_sqlite import BaseSQLite
from app.models.statistiques import calculer_statistiques, comparer_marques
from app.scraper.telechargeur_images import telecharger_image
from config import DELAI_ATTENTE, HEADLESS, DB_PATH, PAGES_MAX, PAUSE_PAGES
from app.outils import slugifier, internet_disponible
from app.scraper.scraper_amazon import ScraperAmazon
from app.views.export_view import ExportCSV, ExportRecap, dossier_categorie
from app.views.graphique_view import GraphiqueView
from app.models.depot_produits import DepotProduits
from app.views.vue_console import VueConsole
from app.scraper.erreurs import ErreurConnexion

DOSSIER_PAGES = "pages"
PAUSE_IMAGES = 0.5  # temps de latence en secondes entre deux téléchargements


class ControleurScraping:

    def lancer(self, mot_cle, fichier_local=None, telecharger_images=False,
               pages=PAGES_MAX, filtre="", exclure=""):
        """Scrape plusieurs pages (ou relit une page locale), puis exporte en CSV."""
        slug = slugifier(mot_cle)
        self.depot.vider()

        if not fichier_local and not internet_disponible():
            self.vue.afficher_message("Pas de connexion à internet (ou Amazon est injoignable). "
                                      "Vérifiez votre connexion puis réessayez.")
            return []

        try:
            with ScraperAmazon(invisible=HEADLESS) as robot:
                if fichier_local:
                    self._lire_page(robot, ScraperAmazon.url_fichier_local(fichier_local))
                else:
                    for page in range(1, pages + 1):
                        adresse = ScraperAmazon.url_recherche(mot_cle, page)
                        if not self._lire_page(robot, adresse, f"{slug}_p{page}"):
                            break  # page bloquée ou vide : on arrête
                        if page < pages:
                            time.sleep(PAUSE_PAGES)
        except ErreurConnexion as erreur:
            self.vue.afficher_message(f"Erreur de connexion : {erreur}.")
            if len(self.depot) == 0:
                return []
            self.vue.afficher_message("Les pages déjà récupérées sont conservées.")

        doublons = self.depot.dedoublonner()
        if doublons:
            self.vue.afficher_message(f"{doublons} doublon(s) retiré(s).")    

        if filtre:
            ecartes = self.depot.filtrer(filtre)
            self.vue.afficher_message(f"Filtre « {filtre} » : {ecartes} produit(s) écarté(s).")

        if exclure:
            retires = self.depot.exclure(exclure)
            self.vue.afficher_message(f"Exclusion « {exclure} » : {retires} produit(s) retiré(s).")    

        if len(self.depot) == 0:
            self.vue.afficher_message("Aucun produit à enregistrer : rien n'est écrit sur le disque.")
            return []

        if telecharger_images:
            self._telecharger_images(slug)

        ExportCSV(slug).enregistrer(self.depot.tous())
        ExportRecap().mettre_a_jour(slug, self.depot.tous())
        self.base.enregistrer(mot_cle, self.depot.tous())
        self.vue.afficher_message(
            f"{len(self.depot)} produit(s) sauvegardé(s) dans la base SQLite."
        )
        return self.depot.tous()

    def _lire_page(self, robot, adresse, nom_page=None):
        """Ouvre une page, la sauvegarde si on donne un nom, ajoute ses produits au dépôt.
        Renvoie True si des résultats ont été trouvés."""
        if not robot.ouvrir(adresse):
            self.vue.afficher_message(f"Chargement trop long, page ignorée : {adresse}")
            return False
        trouve = robot.attendre_resultats(DELAI_ATTENTE)

        if nom_page:
            nom = f"{nom_page}.html" if trouve else f"{nom_page}_bloque.html"
            robot.sauvegarder_html(os.path.join(DOSSIER_PAGES, nom))

        if trouve:
            self.depot.ajouter_tous(robot.extraire_tous())
        return trouve

    def demarrer_menu(self):
        """Boucle du menu : tourne jusqu'à ce que l'utilisateur quitte."""
        while True:
            self.vue.afficher_menu()
            choix = self.vue.demander_choix()

            if choix == "1":
                mot_cle = self.vue.demander_mot_cle()
                if mot_cle:
                    pages = self.vue.demander_nombre_pages(PAGES_MAX)
                    filtre = self.vue.demander_filtre()
                    exclusion = self.vue.demander_exclusion()
                    images = self.vue.demander_oui_non("Télécharger les images ?")
                    self.lancer(mot_cle, telecharger_images=images, pages=pages,
                                filtre=filtre, exclure=exclusion)
                    self.vue.afficher_message(f"{len(self.depot)} produit(s) enregistré(s).")

            elif choix == "2":
                fichier = self.vue.demander_fichier()
                if not os.path.exists(fichier):
                    self.vue.afficher_message(f"Fichier introuvable : {fichier}")
                else:
                    nom_export = self.vue.demander_mot_cle()
                    filtre = self.vue.demander_filtre()
                    exclusion = self.vue.demander_exclusion()
                    images = self.vue.demander_oui_non("Télécharger les images ?")
                    self.lancer(
                        nom_export or "page_locale", fichier,
                        telecharger_images=images, filtre=filtre, exclure=exclusion
                    )
                    self.vue.afficher_message(f"{len(self.depot)} produit(s) enregistré(s).")

            elif choix == "3":
                self.vue.afficher_produits(self.depot.tous())

            elif choix == "4":
                produits = self.depot.tous()
                self.vue.afficher_statistiques(calculer_statistiques(produits))
                if produits:
                    marques = self.vue.demander_marques()
                    if marques:
                        lignes = comparer_marques(produits, marques)
                        self.vue.afficher_comparaison_marques(lignes)
                        if self.vue.demander_oui_non("Enregistrer un graphique ?"):
                            nom = f"marques_{datetime.now():%Y%m%d_%H%M%S}.png"
                            chemin = self.graphiques.prix_moyen_par_marque(lignes, nom)
                            self.vue.afficher_message(
                                f"Graphique enregistré : {chemin}" if chemin
                                else "Rien à dessiner (aucun prix pour ces marques)."
                            )

            elif choix == "5":
                self.vue.afficher_historique(self.base.lister_recherches())

            elif choix == "6":
                mots_cles = self.base.lister_mots_cles()
                self.vue.afficher_mots_cles(mots_cles)
                if mots_cles:
                    mot_cle = self.vue.demander_mot_cle_analyse()
                    lignes = self.base.evolution_prix(mot_cle)
                    self.vue.afficher_evolution_prix(mot_cle, lignes)
                    if len(lignes) >= 2 and self.vue.demander_oui_non("Enregistrer un graphique ?"):
                        chemin = self.graphiques.evolution_prix(
                            mot_cle, lignes, f"evolution_{slugifier(mot_cle)}.png")
                        self.vue.afficher_message(
                            f"Graphique enregistré : {chemin}" if chemin
                            else "Rien à dessiner (pas assez de prix).")

            elif choix == "0":
                self.vue.afficher_message("Au revoir !")
                break

            else:
                self.vue.afficher_message("Choix invalide.")

    def __init__(self):
        self.depot = DepotProduits()
        self.vue = VueConsole()
        self.base = BaseSQLite(DB_PATH)
        self.graphiques = GraphiqueView()

    def _telecharger_images(self, slug):
        """Télécharge l'image de chaque produit dans la catégorie exportée."""
        dossier = os.path.join(dossier_categorie(slug), "images")
        for numero, produit in enumerate(self.depot.tous(), start=1):
            produit.image_fichier = telecharger_image(
                produit.image_url, dossier, f"{numero:03d}.jpg"
            )
            time.sleep(PAUSE_IMAGES)
