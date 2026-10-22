import re

def normaliser(texte):
    """Met en minuscules et enlève les accents (pour comparer sans se soucier de la casse)."""
    decompose = unicodedata.normalize("NFD", texte or "")
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn").lower()

import unicodedata


def slugifier(texte):
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    propre = re.sub(r"[^a-z0-9]+", "_", sans_accents.lower()).strip("_")
    return propre or "produit"