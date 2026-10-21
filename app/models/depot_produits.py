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