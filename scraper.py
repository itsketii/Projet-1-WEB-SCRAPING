import os
import re
from pathlib import Path
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from produit import Produit


class ScraperAmazon:
    """Le robot : ouvre une page avec Firefox et en extrait les produits."""

    URL_RECHERCHE = "https://www.amazon.fr/s?k="
    CARTES = 'div[data-component-type="s-search-result"]'

    # champ : (sélecteur CSS, mot que le texte doit contenir ou None)
    SELECTEURS = {
        "description":   ("span.a-size-base.a-color-secondary.title-differentiators.s-line-clamp-1.a-text-normal", None),
        "prix":          ("span.a-price:not([data-a-strike]) span.a-offscreen", None),  # à vérifier sur la page sauvegardée
        "prix_original": ("span.a-price[data-a-strike='true'] span.a-offscreen", None),
        "note":          ("span.a-size-small.a-color-base", None),                       # sélecteur large : à vérifier
        "avis":          ("span.a-size-mini.puis-normal-weight-text.s-underline-text", None),
        "ventes":        ("span.a-size-base.a-color-secondary", "achetés"),
        "livraison":     ("div.udm-primary-delivery-message", None),
    }

    SELECTEURS_OUI_NON = {
        "stock_limite":  ("span.a-size-base.a-color-price", "reste"),
        "offre_limitee": ("span.a-badge-text", "Offre à durée limitée"),
        # "best_seller": ("...", "..."),  # à compléter avec une page qui contient ce badge
    }

    def __init__(self, invisible=False):
        options = Options()
        if invisible:
            options.add_argument("-headless")
        options.set_preference("intl.accept_languages", "fr-FR")
        self.driver = webdriver.Firefox(options=options)

    # --- permet d'écrire : with ScraperAmazon() as robot: ---
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.fermer()

    def fermer(self):
        self.driver.quit()

    # --- adresses à ouvrir ---
    @classmethod
    def url_recherche(cls, mot_cle):
        return cls.URL_RECHERCHE + quote_plus(mot_cle)

    @staticmethod
    def url_fichier_local(chemin):
        return Path(chemin).resolve().as_uri()

    # --- outils internes ---
    @staticmethod
    def _texte(element):
        brut = element.get_attribute("textContent") or ""
        return " ".join(brut.split())

    def _chercher(self, carte, selecteur, contient=None):
        for element in carte.find_elements(By.CSS_SELECTOR, selecteur):
            t = self._texte(element)
            if t and (contient is None or contient in t):
                return t
        return None

    # --- actions principales ---
    def ouvrir(self, adresse):
        self.driver.get(adresse)

    def attendre_resultats(self, delai=15):
        """True si les cartes produits apparaissent, False sinon (captcha, blocage...)."""
        try:
            WebDriverWait(self.driver, delai).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, self.CARTES)))
            return True
        except TimeoutException:
            return False

    def sauvegarder_html(self, chemin):
        """Enregistre la page reçue pour pouvoir régler les sélecteurs hors ligne."""
        os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
        with open(chemin, "w", encoding="utf-8") as f:
            f.write(self.driver.page_source)

    def extraire_produit(self, carte):
        """Transforme UNE carte HTML en objet Produit."""
        produit = Produit()

        h2 = carte.find_elements(By.TAG_NAME, "h2")
        produit.nom = self._texte(h2[0]) if h2 else None

        for champ, (selecteur, contient) in self.SELECTEURS.items():
            setattr(produit, champ, self._chercher(carte, selecteur, contient))

        montant = re.search(r"(\d+,\d+)\s*€", produit.livraison or "")
        produit.prix_livraison = montant.group(1) if montant else None

        for champ, (selecteur, contient) in self.SELECTEURS_OUI_NON.items():
            setattr(produit, champ, self._chercher(carte, selecteur, contient) is not None)

        return produit

    def extraire_tous(self):
        """Renvoie la liste de tous les produits de la page."""
        cartes = self.driver.find_elements(By.CSS_SELECTOR, self.CARTES)
        return [self.extraire_produit(carte) for carte in cartes]