import re
import unicodedata



def _normaliser(texte):
    """Met en minuscules et enlève les accents (pour comparer sans se soucier de la casse)."""
    decompose = unicodedata.normalize("NFD", texte or "")
    return "".join(c for c in decompose if unicodedata.category(c) != "Mn").lower()


class DepotProduits:
    """Garde en mémoire les produits scrapés."""

    def __init__(self):
        self._produits = []

    def ajouter(self, produit):
        self._produits.append(produit)

    def ajouter_tous(self, produits):
        self._produits.extend(produits)

    def tous(self):
        return list(self._produits)

    def vider(self):
        self._produits.clear()

    def __len__(self):
        return len(self._produits)

    def filtrer(self, termes):
        """Ne garde que les produits dont le nom contient TOUS les mots de `termes`.
        Renvoie le nombre de produits écartés."""
        mots = _normaliser(termes).split()
        if not mots:
            return 0

        avant = len(self._produits)
        self._produits = [
            produit for produit in self._produits
            if all(re.search(rf"\b{re.escape(mot)}\b", _normaliser(produit.nom)) for mot in mots)
        ]
        return avant - len(self._produits)