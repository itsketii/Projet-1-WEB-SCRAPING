import logging
import os

from config import DOSSIER_DATA


def configurer_journal():
    """Prépare le journal et renvoie le logger des opérations de scraping."""
    dossier = os.path.join(DOSSIER_DATA, "journal")
    os.makedirs(dossier, exist_ok=True)
    journal = logging.getLogger("scraper")
    if journal.handlers:
        return journal
    journal.setLevel(logging.INFO)
    fichier = logging.FileHandler(
        os.path.join(dossier, "scraping.log"), encoding="utf-8-sig"
    )
    fichier.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
    )
    journal.addHandler(fichier)
    return journal
