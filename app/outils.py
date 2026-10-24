import re
import unicodedata
import socket


def normaliser(texte):
    """Met en minuscules et enlève les accents (pour comparer sans se soucier de la casse)."""
    decompose = unicodedata.normalize("NFD", texte or "")
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn").lower()


def slugifier(texte):
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    propre = re.sub(r"[^a-z0-9]+", "_", sans_accents.lower()).strip("_")
    return propre or "produit"


def internet_disponible(hote="www.amazon.fr", port=443, delai=5):
    """True si on peut joindre le site, False sinon (pas de connexion, DNS, site hors ligne)."""
    try:
        with socket.create_connection((hote, port), timeout=delai):
            return True
    except OSError:
        return False