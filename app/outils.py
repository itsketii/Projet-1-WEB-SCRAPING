import re
import unicodedata


def slugifier(texte):
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    propre = re.sub(r"[^a-z0-9]+", "_", sans_accents.lower()).strip("_")
    return propre or "produit"