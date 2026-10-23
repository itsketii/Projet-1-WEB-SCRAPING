# **Projet-1-WEB-SCRAPING**

Projet de **web scraping d'Amazon** réalisé dans le cadre du module de
programmation Python.

---

[![](https://media0.giphy.com/media/vgS9c8KaZacV6XIcm9/giphy.gif?cid=ecf05e47kz0lvja06pr9cg647dk8l5p3eaqh18lcpj33p31t&rid=giphy.gif&ct=s)](https://media0.giphy.com/media/vgS9c8KaZacV6XIcm9/giphy.gif?cid=ecf05e47kz0lvja06pr9cg647dk8l5p3eaqh18lcpj33p31t&rid=giphy.gif&ct=s)

---

Le **web scraping**, aussi appelé **harvesting** ou **moissonnage**, consiste à
extraire automatiquement des données présentes sur un site web à l'aide d'un
programme.

Dans ce projet, un robot ouvre les pages de résultats Amazon, repère les cartes
des produits et récupère leurs informations (nom, prix, note, avis, livraison,
image...). Les résultats sont filtrés, analysés, puis enregistrés dans des
fichiers CSV et dans une base SQLite. Le programme se pilote depuis un menu
console.

> **Attention :** ce projet est pédagogique. Il faut respecter les conditions
> d'utilisation d'Amazon, son fichier `robots.txt`, la législation applicable
> et limiter la fréquence des requêtes.

---

**STACK TECHNIQUE / OUTILS UTILISÉS**

- Langage : **Python 3** avec l'architecture **MVC**
- Navigateur automatisé : **Firefox**
- Bibliothèques externes :
  * `selenium` : ouverture du navigateur et recherche d'éléments HTML ;
  * `python-dotenv` : lecture facultative d'un fichier `.env`.
- Outils intégrés à Python : `argparse`, `csv`, `sqlite3`, `dataclasses`, `re`,
  `unicodedata`, `statistics`, `urllib`.
- Gestion du code : `Git` et `GitHub` (une branche par fonctionnalité, versions
  `majeure.intermédiaire.mineure`).

---

**ARCHITECTURE DU PROJET**

```
/Projet-1-WEB-SCRAPING
│
├── main.py                          # point d'entrée (menu ou ligne de commande)
├── config.py                        # réglages du programme
├── requirements.txt                 # dépendances Python
├── README.md                        # présentation du projet
├── .gitignore                       # fichiers exclus de Git
│
├── app/
│   ├── outils.py                    # normaliser et slugifier un texte
│   ├── controllers/
│   │   └── controleur_scraping.py   # orchestre scraping, filtre, export, base, menu
│   ├── models/
│   │   ├── produit.py               # données d'un produit
│   │   ├── depot_produits.py        # stockage en mémoire et filtre
│   │   ├── statistiques.py          # prix et comparaison de marques
│   │   └── base_sqlite.py           # base de données SQLite
│   ├── scraper/
│   │   ├── navigateur.py            # création du navigateur Firefox
│   │   ├── extracteur.py            # sélecteurs CSS et lecture d'un produit
│   │   ├── scraper_amazon.py        # pilotage de la page Amazon
│   │   └── telechargeur_images.py   # téléchargement des images
│   └── views/
│       ├── export_view.py           # data.csv par catégorie et recap.csv
│       └── vue_console.py           # menu et affichages dans le terminal
│
├── pages/                           # pages HTML sauvegardées (ecouteurs.html = exemple)
└── data/                            # résultats générés (ignorés par Git)
    ├── recap.csv                    # résumé de chaque catégorie scrapée
    ├── base_de_donnees/
    │   └── produits.db              # base SQLite (recherches et produits)
    └── tech/
        └── <categorie>/
            ├── data.csv             # produits de la catégorie
            └── images/              # images téléchargées
```

Les fichiers `__init__.py` ne sont pas listés pour garder le schéma lisible.

---

**INSTALLATION & UTILISATION**

### 1. Récupérer le projet et créer l'environnement virtuel

```Shell
git clone https://github.com/itsketii/Projet-1-WEB-SCRAPING.git
cd Projet-1-WEB-SCRAPING
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Installer les dépendances

```Shell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Firefox doit également être installé sur l'ordinateur.

### 3. Lancer le menu

```Shell
python main.py
```

Le menu propose :

1. lancer un scraping à partir d'un mot-clé (nombre de pages, filtre et
   téléchargement des images au choix) ;
2. analyser une page HTML déjà sauvegardée ;
3. afficher les produits en mémoire ;
4. afficher les statistiques (prix minimum, maximum, moyen, médian, promotions)
   et comparer des marques ;
5. consulter l'historique des recherches enregistrées dans la base SQLite.

### 4. Lancer une recherche en ligne de commande

```Shell
python main.py "écouteurs sans fil"
```

Options disponibles :

| Option                           | Rôle                                                           |
| -------------------------------- | --------------------------------------------------------------- |
| `--pages 2`                    | nombre de pages de résultats à parcourir                      |
| `--filtre "iphone 18"`         | ne garder que les produits dont le nom contient ces mots        |
| `--images`                     | télécharger l'image de chaque produit                         |
| `--local pages\ecouteurs.html` | travailler sur une page sauvegardée, sans requête vers Amazon |

Exemple, sans aucune requête vers Amazon :

```Shell
python main.py "ecouteurs" --local pages\ecouteurs.html --filtre jbl
```

### 5. Configuration facultative

Le projet fonctionne sans configuration. Pour modifier les réglages, créer un
fichier `.env` à la racine :

```
HEADLESS=false
DELAI_ATTENTE=15
DOSSIER_DATA=data
FAMILLE=tech
```

- `HEADLESS=true` lance Firefox sans afficher sa fenêtre ;
- `DELAI_ATTENTE=15` attend au maximum 15 secondes les résultats ;
- `DOSSIER_DATA=data` indique où enregistrer les résultats ;
- `FAMILLE=tech` est le dossier de famille de produits dans `data/`.

Le fichier `.env` est ignoré par Git. Le nombre de pages par défaut
(`PAGES_MAX`) et la pause entre deux pages (`PAUSE_PAGES`) se règlent dans
`config.py`.

---

**RÉSULTATS**

Pour chaque catégorie scrapée, les produits sont enregistrés dans
`data/tech/<categorie>/data.csv` (ouvrable avec Excel ou LibreOffice), les
images dans `data/tech/<categorie>/images/`, et la ligne de la catégorie est
mise à jour dans `data/recap.csv`. Toutes les recherches sont aussi conservées
dans la base `data/base_de_donnees/produits.db`.

Si Amazon affiche un captcha ou une page bloquée, la page est sauvegardée avec
le suffixe `_bloque.html` et aucun produit n'est exporté.
