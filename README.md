# **Projet-1-WEB-SCRAPPING**

Projet de **web scraping d'Amazon** réalisé dans le cadre du module de
programmation Python.

---

![](https://media0.giphy.com/media/vgS9c8KaZacV6XIcm9/giphy.gif?cid=ecf05e47kz0lvja06pr9cg647dk8l5p3eaqh18lcpj33p31t&rid=giphy.gif&ct=s)

---

Le **web scraping**, aussi appelé **harvesting** ou **moissonnage**, consiste à
extraire automatiquement des données présentes sur un site web à l'aide d'un
programme.

Dans ce projet, un robot ouvre une page de résultats Amazon, repère les cartes
des produits, récupère leurs informations et les enregistre dans un fichier
CSV. Le projet permet donc de découvrir la récupération, le nettoyage et le
stockage de données web.

> **Attention :** ce projet est pédagogique. Il faut respecter les conditions
> d'utilisation d'Amazon, son fichier `robots.txt`, la législation applicable
> et limiter la fréquence des requêtes.

---

**OBJECTIF DU PROJET**

L'objectif est d'apprendre à :

- lancer une recherche à partir d'un mot-clé ;
- automatiser un navigateur avec Selenium ;
- attendre le chargement d'une page dynamique ;
- repérer des éléments HTML avec des sélecteurs CSS ;
- transformer les informations trouvées en objets Python ;
- sauvegarder une page HTML pour pouvoir la réutiliser hors ligne ;
- exporter les résultats dans un fichier CSV.

Le programme extrait notamment le nom, le prix, la note, le nombre d'avis, les
informations de livraison et certains badges affichés sur les produits.

---

**STACK TECHNIQUE / OUTILS UTILISÉS**

- Langage de programmation : **Python 3**
- Navigateur automatisé : **Firefox**
- Bibliothèques et outils utilisés :
  - `selenium` : ouverture du navigateur et recherche d'éléments HTML ;
  - `python-dotenv` : lecture facultative d'un fichier `.env` ;
  - `argparse` : lecture des commandes du terminal ;
  - `csv` : création des fichiers CSV ;
  - `dataclasses` : représentation des produits ;
  - `os`, `pathlib`, `re` et `unicodedata` : outils intégrés à Python ;
  - `Git` et `GitHub` : gestion du code.

Les dépendances installables sont indiquées dans
[`requirements.txt`](requirements.txt). Les outils `requests`, `pandas`,
`Scrapy`, `lxml` et `SQLite` ne sont pas utilisés dans la version actuelle du
programme.

---

**ARCHITECTURE DU PROJET**

```text
/Projet-1-WEB-SCRAPPING
│
├── main.py              # point d'entrée du programme
├── scraper.py           # navigateur Selenium et extraction HTML
├── produit.py           # modèle de données d'un produit
├── export_csv.py        # enregistrement des produits en CSV
├── outils.py            # fonctions utilitaires
├── config.py            # réglages du programme
├── requirements.txt     # dépendances Python
├── README.md            # présentation du projet
├── .gitignore           # fichiers exclus de Git
├── pages/               # pages HTML sauvegardées automatiquement
└── data/                # fichiers CSV créés automatiquement
```

Un guide personnel plus détaillé se trouve dans
[`docs/Help.md`](docs/Help.md). Ce fichier est
volontairement exclu de Git afin de rester un support de travail personnel.

---

**DONNÉES SCRAPÉES**

Le scraping porte sur les produits visibles dans les résultats Amazon, par
exemple :

- les ordinateurs portables ;
- les supports pour ordinateur et téléphone ;
- les souris Bluetooth ;
- les casques audio ;
- les écouteurs sans fil ;
- les autres accessoires électroniques.

Les champs récupérés peuvent être :
`nom`, `description`, `prix`, `prix_original`, `note`, `avis`, `ventes`,
`livraison`, `prix_livraison`, `best_seller`, `stock_limite` et
`offre_limitee`.

Certains champs peuvent rester vides, car Amazon ne les affiche pas toujours
ou peut modifier la structure de ses pages.

---

**INSTALLATION & UTILISATION**

### 1. Créer l'environnement virtuel

Dans PowerShell, depuis le dossier du projet :

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Installer les dépendances

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Firefox doit également être installé sur l'ordinateur.

### 3. Lancer une recherche

```powershell
python main.py "écouteurs sans fil"
```

Le programme crée alors notamment :

```text
pages/ecouteurs_sans_fil.html
data/ecouteurs_sans_fil_AAAAMMJJ_HHMMSS.csv
```

La date et l'heure sont ajoutées au nom du fichier CSV. Chaque exécution
conserve donc son propre résultat au lieu d'écraser le fichier précédent.

La page HTML est sauvegardée pour pouvoir vérifier les sélecteurs et refaire
une extraction sans envoyer une nouvelle requête à Amazon :

```powershell
python main.py "écouteurs sans fil" --local pages\ecouteurs_sans_fil.html
```

### 4. Configuration facultative

Le projet fonctionne sans configuration supplémentaire. Pour modifier ses
réglages, créer un fichier `.env` à la racine :

```dotenv
HEADLESS=false
DELAI_ATTENTE=15
DOSSIER_DATA=data
```

- `HEADLESS=true` lance Firefox sans afficher sa fenêtre ;
- `DELAI_ATTENTE=15` attend au maximum 15 secondes les résultats ;
- `DOSSIER_DATA=data` indique où enregistrer les fichiers CSV.

Le fichier `.env` est ignoré par Git.

---

**RÉSULTAT / ANALYSE**

Pour chaque produit trouvé, une ligne est ajoutée au fichier CSV. Le fichier
peut ensuite être ouvert avec Excel, LibreOffice ou un autre outil d'analyse.

Si Amazon affiche un captcha ou une page bloquée, le programme sauvegarde la
page avec le suffixe `_bloque.html` et n'exporte aucun produit trouvé.

---

**DÉFIS RENCONTRÉS**

- Les pages Amazon sont dynamiques : il faut attendre l'apparition des
  résultats avec `WebDriverWait`.
- Les sélecteurs CSS peuvent changer lorsque le site modifie son HTML.
- Amazon peut afficher un captcha ou bloquer une requête.
- Les accents et les espaces doivent être nettoyés pour créer des noms de
  fichiers valides.
- Les valeurs extraites sont conservées comme texte et peuvent être absentes.

La sauvegarde locale des pages permet de régler les sélecteurs sans refaire
constamment des requêtes vers Amazon.

---

**CONCLUSION**

Ce projet présente les principales étapes d'un web scraper : recevoir une
entrée, ouvrir une page, attendre son contenu, extraire les données, les
transformer en objets Python et les exporter dans un fichier réutilisable.

Il constitue une base pour ajouter plus tard du nettoyage de données, des
analyses statistiques ou une base de données.
