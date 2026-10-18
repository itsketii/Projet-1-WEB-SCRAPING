import re
import unicodedata


def slugifier(texte):
    """'Écouteurs sans fil' -> 'ecouteurs_sans_fil' (utilisable comme nom de fichier)."""
    sans_accents = unicodedata.normalize("NFKD", texte).encode("ascii", "ignore").decode()
    propre = re.sub(r"[^a-z0-9]+", "_", sans_accents.lower()).strip("_")
    return propre or "produit"