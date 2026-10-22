class VueConsole:
    """Interaction avec l'utilisateur dans le terminal."""

    def afficher_menu(self):
        print("\n=== Scraper Amazon ===")
        print("1. Lancer un scraping (mot-clé)")
        print("2. Analyser une page HTML sauvegardée")
        print("3. Afficher les produits en mémoire")
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