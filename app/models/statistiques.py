import re
import statistics
from collections import Counter


def convertir_rpix(texte):
    if not texte:
        return None
    chiffres = re.sub(r"[^\d]", "", texte).replace(",",".")
    try:
        return float(chiffres)
    except ValueError:
        return None


def calculer_statistiques(produits, nb_marques = 5):
    prix = [p for p in (convertir_rpix(x.prix) for x in produits) if p is not None] 
    marques = Counter(x.nom.split()[0] for x in produits if x.nom)
    return {
        "nombre" : len(produits),
        "sans_prix" : len(produits)-len(prix),
        "prix_min" : min(prix) if prix else None,
        "prix_max" : max(prix) if prix else None,
        "prix_moyen" : statistics.mean(prix) if prix else None,
        "prix_median" : statistics.median(prix) if prix else None,
        "en_promo" : sum(1 for x in produits if x.prix_original),
        "marques" : marques.most_common(nb_marques,)
    }