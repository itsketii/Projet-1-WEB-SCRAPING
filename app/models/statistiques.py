import re
import statistics

from app.outils import normaliser


def convertir_prix(texte):
    if not texte:
        return None
    chiffres = re.sub(r"[^\d,]", "", texte).replace(",", ".")
    try:
        return float(chiffres)
    except ValueError:
        return None


def _prix_valides(produits):
    return [p for p in (convertir_prix(x.prix) for x in produits) if p is not None]


def calculer_statistiques(produits):
    prix = _prix_valides(produits)
    return {
        "nombre": len(produits),
        "sans_prix": len(produits) - len(prix),
        "prix_min": min(prix) if prix else None,
        "prix_max": max(prix) if prix else None,
        "prix_moyen": statistics.mean(prix) if prix else None,
        "prix_median": statistics.median(prix) if prix else None,
        "en_promo": sum(1 for x in produits if x.prix_original),
    }


def comparer_marques(produits, marques):
    resultat = []
    for marque in marques:
        motif = rf"\b{re.escape(normaliser(marque))}\b"
        concernes = [p for p in produits if re.search(motif, normaliser(p.nom))]
        prix = _prix_valides(concernes)
        resultat.append({
            "marque": marque,
            "nombre": len(concernes),
            "prix_moyen": statistics.mean(prix) if prix else None,
        })
    return resultat

def variation_pourcent(avant, apres):
    """Variation en pourcentage entre deux valeurs, ou None si on ne peut pas la calculer."""
    if not avant or apres is None:
        return None
    return (apres - avant) / avant * 100