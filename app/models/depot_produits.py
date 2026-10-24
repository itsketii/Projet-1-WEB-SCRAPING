import re

from app.outils import normaliser


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
        mots = normaliser(termes).split()
        if not mots:
            return 0

        avant = len(self._produits)
        self._produits = [
            produit for produit in self._produits
            if all(re.search(rf"\b{re.escape(mot)}\b", normaliser(produit.nom)) for mot in mots)
        ]
        return avant - len(self._produits)

    def exclure(self, termes):
        """Retire les produits dont le nom contient AU MOINS UN des mots de `termes`.
        Renvoie le nombre de produits retirés."""
        mots = normaliser(termes).split()
        if not mots:
            return 0

        avant = len(self._produits)
        self._produits = [
            produit for produit in self._produits
            if not any(re.search(rf"\b{re.escape(mot)}\b", normaliser(produit.nom)) for mot in mots)
        ]
        return avant - len(self._produits)

    def dedoublonner(self):
        """Retire les produits dont le nom a déjà été vu (on garde le premier).
        Renvoie le nombre de doublons retirés."""
        deja_vus = set()
        uniques = []
        for produit in self._produits:
            cle = normaliser(produit.nom)
            if cle and cle in deja_vus:
                continue
            deja_vus.add(cle)
            uniques.append(produit)

        retires = len(self._produits) - len(uniques)
        self._produits = uniques
        return retires