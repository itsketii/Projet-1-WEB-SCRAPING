class VueConsole:
    """Interaction avec l'utilisateur dans le terminal."""

    def afficher_menu(self):
        print("\n=== Scraper Amazon ===")
        print("1. Lancer un scraping (mot-clé)")
        print("2. Analyser une page HTML sauvegardée")
        print("3. Afficher les produits en mémoire")
        print("4. Statistiques")
        print("5. Historique des recherches (base SQLite)")
        print("0. Quitter")

    def demander_choix(self):
        return input("Votre choix : ").strip()

    def demander_mot_cle(self):
        return input("Produit à rechercher : ").strip()

    def demander_fichier(self):
        return input("Chemin de la page HTML : ").strip().strip('"')

    def afficher_message(self, texte):
        print(texte)

    def afficher_produits(self, produits):
        if not produits:
            print("Aucun produit en mémoire.")
            return
        for i, produit in enumerate(produits, start=1):
            nom = (produit.nom or "(sans nom)")[:60]
            print(f"{i}. {nom} | {produit.prix or 'prix inconnu'}")

    def demander_oui_non(self, question):
        return input(f"{question} (o/n) : ").strip().lower() == "o"

    def demander_nombre_pages(self, defaut):
        saisie = input(f"Nombre de pages [{defaut}] : ").strip()
        return int(saisie) if saisie.isdigit() and int(saisie) > 0 else defaut

    def demander_filtre(self):
        return input("Filtre sur le nom (si vous ne voulez pas filtrer appuyez sur entrer) : ").strip()

    def afficher_statistiques(self, stats):
        if stats["nombre"] == 0:
            print("Aucun produit en mémoire : lancez d'abord un scraping.")
            return

        def euros(valeur):
            return "n/a" if valeur is None else f"{valeur:.2f} €".replace(".", ",")

        print("\n=== Statistiques ===")
        print(f"Produits : {stats['nombre']} ({stats['sans_prix']} sans prix)")
        print(f"Prix minimum : {euros(stats['prix_min'])}")
        print(f"Prix maximum : {euros(stats['prix_max'])}")
        print(f"Prix moyen   : {euros(stats['prix_moyen'])}")
        print(f"Prix médian  : {euros(stats['prix_median'])}")
        print(f"Produits en promotion : {stats['en_promo']}")

    def demander_marques(self):
        saisie = input("Marques à comparer, séparées par des espaces (ex. jbl samsung apple, vide = aucune) : ")
        return saisie.split()

    def afficher_comparaison_marques(self, lignes):
        print("\n=== Comparaison des marques ===")
        for ligne in lignes:
            prix = "n/a" if ligne["prix_moyen"] is None else f"{ligne['prix_moyen']:.2f} €".replace(".", ",")
            print(f"{ligne['marque']} : {ligne['nombre']} produit(s), prix moyen {prix}")

    def afficher_historique(self, lignes):
        if not lignes:
            print("Aucune recherche enregistrée dans la base.")
            return
        print("\n=== Historique des recherches ===")
        for identifiant, mot_cle, date, nombre in lignes:
            print(f"#{identifiant} | {date} | {mot_cle} | {nombre} produit(s)")

    def demander_exclusion(self):
        return input("Mots à exclure(vide = aucun) : ").strip()       