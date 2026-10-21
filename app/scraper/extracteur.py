import re

from selenium.webdriver.common.by import By

from app.models.produit import Produit

CARTES = 'div[data-component-type="s-search-result"]'

SELECTEURS = {
    "description":   ("span.a-size-base.a-color-secondary.title-differentiators.s-line-clamp-1.a-text-normal", None),
    "prix":          ("span.a-price:not([data-a-strike]) span.a-offscreen", None),
    "prix_original": ("span.a-price[data-a-strike='true'] span.a-offscreen", None),
    "note":          ("span.a-size-small.a-color-base", None),
    "avis":          ("span.a-size-mini.puis-normal-weight-text.s-underline-text", None),
    "ventes":        ("span.a-size-base.a-color-secondary", "achetés"),
    "livraison":     ("div.udm-primary-delivery-message", None),
}

SELECTEURS_OUI_NON = {
    "stock_limite":  ("span.a-size-base.a-color-price", "reste"),
    "offre_limitee": ("span.a-badge-text", "Offre à durée limitée"),
}


def texte(element):
    brut = element.get_attribute("textContent") or ""
    return " ".join(brut.split())


def chercher(carte, selecteur, contient=None):
    for element in carte.find_elements(By.CSS_SELECTOR, selecteur):
        t = texte(element)
        if t and (contient is None or contient in t):
            return t
    return None


def extraire_produit(carte):
    """Transforme UNE carte HTML en objet Produit."""
    produit = Produit()

    h2 = carte.find_elements(By.TAG_NAME, "h2")
    produit.nom = texte(h2[0]) if h2 else None
    image = carte.find_elements(By.CSS_SELECTOR, "img.s-image")
    produit.image_url = image[0].get_attribute("src") if image else None

    for champ, (selecteur, contient) in SELECTEURS.items():
        setattr(produit, champ, chercher(carte, selecteur, contient))

    montant = re.search(r"(\d+,\d+)\s*€", produit.livraison or "")
    produit.prix_livraison = montant.group(1) if montant else None

    for champ, (selecteur, contient) in SELECTEURS_OUI_NON.items():
        setattr(produit, champ, chercher(carte, selecteur, contient) is not None)

    return produit