import os
import urllib.request


def telecharger_image(url, dossier, nom_fichier, delai=10):
    """Télécharge une image. Renvoie le chemin du fichier, ou None si ça échoue."""
    if not url:
        return None

    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier)

    try:
        requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(requete, timeout=delai) as reponse:
            contenu = reponse.read()
        with open(chemin, "wb") as fichier:
            fichier.write(contenu)
        return chemin
    except (OSError, ValueError):
        return None