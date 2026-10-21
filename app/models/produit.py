from dataclasses import dataclass
from typing import Optional


@dataclass
class Produit:
    """La "fiche" d'un produit trouvé sur Amazon."""
    nom: Optional[str] = None
    description: Optional[str] = None
    prix: Optional[str] = None
    prix_original: Optional[str] = None
    note: Optional[str] = None
    avis: Optional[str] = None
    ventes: Optional[str] = None
    livraison: Optional[str] = None
    prix_livraison: Optional[str] = None
    best_seller: bool = False
    stock_limite: bool = False
    offre_limitee: bool = False
    image_url: str | None = None
    image_fichier: str | None = None