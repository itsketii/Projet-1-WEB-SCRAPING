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
image...). Les doublons sont retirés, les résultats peuvent être filtrés,
analysés (statistiques, comparaison de marques, évolution des prix, graphiques),
puis enregistrés dans des fichiers CSV et dans une base SQLite. Le programme se
pilote depuis un menu console.

> **Attention :** ce projet est pédagogique. Il faut respecter les conditions
> d'utilisation d'Amazon, son fichier `robots.txt`, la législation applicable
> et limiter la fréquence des requêtes.

Ce projet sert à apprendre le web scraping, sur de petites quantités de
données publiques. Le programme fait des pauses entre les actions pour ne pas
surcharger le site. Les conditions d'utilisation d'Amazon encadrent la
collecte automatique de données : il ne faut donc pas s'en servir à des fins
commerciales ni republier les données et les images collectées.

Le projet est réalisé dans un cadre académique, dans le cadre du cours de
Python. Aucune licence n'est définie pour le moment.

**LIMITES DU PROJET**

- Les conditions d'utilisation d'Amazon interdisent l'extraction automatisée :
  il faut garder de **petits volumes**, laisser **plusieurs heures** entre deux
  exécutions et ne pas utiliser les données hors d'un cadre d'étude.
- Si un CAPTCHA apparaît, le programme s'arrête et conserve les articles déjà
  récupérés. Il ne cherche pas à le contourner.
- Pour un usage réel, il faut préférer l'API officielle
  **Product Advertising API** d'Amazon.

---

**STACK TECHNIQUE / OUTILS UTILISÉS**

- Langage : **Python 3** avec l'architecture **MVC**
- Navigateur automatisé : **Firefox**
- Bibliothèques externes :
  * `selenium` : ouverture du navigateur et recherche d'éléments HTML ;
  * `python-dotenv` : lecture facultative d'un fichier `.env` ;
  * `matplotlib` : graphiques enregistrés en PNG.
- Outils intégrés à Python : `argparse`, `csv`, `sqlite3`, `dataclasses`, `re`,
  `unicodedata`, `statistics`, `urllib`, `socket`, `logging`.
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
│   ├── outils.py                    # normaliser, slugifier, vérifier internet
│   ├── journal.py                   # fichier de journal (logging)
│   ├── controllers/
│   │   └── controleur_scraping.py   # orchestre scraping, filtres, export, base, menu
│   ├── models/
│   │   ├── produit.py               # données d'un produit
│   │   ├── depot_produits.py        # stockage en mémoire, doublons, filtre, exclusion
│   │   ├── statistiques.py          # prix, comparaison de marques, variation
│   │   └── base_sqlite.py           # base de données SQLite
│   ├── scraper/
│   │   ├── navigateur.py            # création du navigateur Firefox
│   │   ├── extracteur.py            # sélecteurs CSS et lecture d'un produit
│   │   ├── scraper_amazon.py        # pilotage de la page Amazon
│   │   ├── telechargeur_images.py   # téléchargement des images
│   │   └── erreurs.py               # erreur de connexion
│   └── views/
│       ├── export_view.py           # data.csv par catégorie et recap.csv
│       ├── graphique_view.py        # graphiques PNG (matplotlib)
│       └── vue_console.py           # menu et affichages dans le terminal
│
├── pages/                           # pages HTML sauvegardées (ecouteurs.html = exemple)
└── data/                            # résultats générés (ignorés par Git)
    ├── recap.csv                    # résumé de chaque catégorie scrapée
    ├── base_de_donnees/
    │   └── produits.db              # base SQLite (recherches et produits)
    ├── graphiques/                  # graphiques PNG
    ├── journal/
    │   └── scraping.log             # journal des opérations et des erreurs
    └── tech/
        └── <categorie>/
            ├── data.csv             # produits de la catégorie
            └── images/              # images téléchargées
```

Les fichiers `__init__.py` ne sont pas listés pour garder le schéma lisible.

---

**INSTALLATION & UTILISATION**

### 1. Récupérer le projet et créer l'environnement virtuel

```
git clone https://github.com/itsketii/Projet-1-WEB-SCRAPING.git
cd Projet-1-WEB-SCRAPING
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Installer les dépendances

```
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Firefox doit également être installé sur l'ordinateur.

### 3. Lancer le menu

```
python main.py
```

Le menu propose :

1. lancer un scraping à partir d'un mot-clé (nombre de pages, filtre, mots
   exclus et téléchargement des images au choix) ;
2. analyser une page HTML déjà sauvegardée ;
3. afficher les produits en mémoire ;
4. afficher les statistiques (prix minimum, maximum, moyen, médian, promotions),
   comparer des marques et enregistrer un graphique ;
5. consulter l'historique des recherches enregistrées dans la base SQLite ;
6. suivre l'évolution du prix moyen d'un mot-clé entre plusieurs recherches et
   enregistrer un graphique ;
7. afficher le journal des opérations.

### 4. Lancer une recherche en ligne de commande

```
python main.py "écouteurs sans fil"
```

Options disponibles :

| Option                           | Rôle                                                           |
| -------------------------------- | --------------------------------------------------------------- |
| `--pages 2`                    | nombre de pages de résultats à parcourir                      |
| `--filtre "iphone 18"`         | ne garder que les produits dont le nom contient ces mots        |
| `--exclure "coque etui"`       | retirer les produits dont le nom contient l'un de ces mots      |
| `--images`                     | télécharger l'image de chaque produit                         |
| `--local pages\ecouteurs.html` | travailler sur une page sauvegardée, sans requête vers Amazon |

Exemple, sans aucune requête vers Amazon :

```
python main.py "ecouteurs" --local pages\ecouteurs.html --filtre jbl --exclure filaire
```

Les produits en double (souvent des produits sponsorisés qui reviennent d'une
page à l'autre) sont retirés automatiquement. Sans connexion internet, le
programme affiche un message au lieu de planter.

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
dans la base `data/base_de_donnees/produits.db`, et les graphiques dans
`data/graphiques/`.

Le fichier `data/journal/scraping.log` garde la trace de chaque lancement :
pages lues, pages bloquées, erreurs de connexion, durées.

Si Amazon affiche un captcha ou une page bloquée, la page est sauvegardée avec
le suffixe `_bloque.html` et aucun produit n'est exporté.

---

**DIFFICULTÉS RENCONTRÉES**

- Les pages Amazon peuvent changer de structure, ce qui oblige à adapter les
  sélecteurs utilisés pour trouver les produits.
- Certains produits n'ont pas de prix, d'image ou d'autres informations
  disponibles.
- Les produits sponsorisés peuvent apparaître plusieurs fois et doivent être
  retirés avant l'enregistrement.
- Le chargement des pages peut être long ou interrompu par une page bloquée ou
  un CAPTCHA.
- La gestion des filtres, des exclusions, des statistiques, des graphiques et
  de l'historique a demandé de séparer correctement les responsabilités entre
  les modèles, les vues et le contrôleur.

---

**AUTRICE**

**KOUADIO KETSIA**

Licence 2 Informatique & Génie Logiciel, Institut Ivoirien de Technologie (IIT).

Projet réalisé dans le cadre du cours de Programmation Python.
