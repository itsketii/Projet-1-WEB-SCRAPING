import os
from pathlib import Path
from urllib.parse import quote_plus

from config import DELAI_CHARGEMENT
from app.scraper.navigateur import creer_navigateur
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.scraper.extracteur import CARTES, extraire_produit

class ScraperAmazon:

    URL_RECHERCHE = "https://www.amazon.fr/s?k="
    
    

    def __init__(self, invisible=False):
      self.driver = creer_navigateur(invisible, DELAI_CHARGEMENT)
    
    # --- permet d'écrire : with ScraperAmazon() as robot: ---
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.fermer()

    def fermer(self):
        self.driver.quit()

    # --- adresses à ouvrir ---
    @classmethod
    def url_recherche(cls, mot_cle, page=1):
        adresse = cls.URL_RECHERCHE + quote_plus(mot_cle)
        if page > 1:
            adresse += f"&page={page}"
        return adresse

    @staticmethod
    def url_fichier_local(chemin):
        return Path(chemin).resolve().as_uri()


    # --- actions principales ---
    def ouvrir(self, adresse):
        """True si la page s'est chargée à temps, False si le délai est dépassé."""
        try:
            self.driver.get(adresse)
            return True
        except TimeoutException:
            return False

    def attendre_resultats(self, delai=15):
        """True si les cartes produits apparaissent, False sinon (captcha, blocage...)."""
        try:
            WebDriverWait(self.driver, delai).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, CARTES)))
            return True
        except TimeoutException:
            return False

    def sauvegarder_html(self, chemin):
        """Enregistre la page reçue pour pouvoir régler les sélecteurs hors ligne."""
        os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

   
    def extraire_tous(self):
        """Renvoie la liste de tous les produits de la page."""
        cartes = self.driver.find_elements(By.CSS_SELECTOR, CARTES)
        return [extraire_produit(carte) for carte in cartes]