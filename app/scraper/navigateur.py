from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def creer_navigateur(invisible=False, delai_chargement=30):
    options = Options()
    if invisible:
        options.add_argument("-headless")
    options.set_preference("intl.accept_languages", "fr-FR")
    options.page_load_strategy = "eager"      # n'attend pas les images et pubs
    navigateur = webdriver.Firefox(options=options)
    navigateur.set_page_load_timeout(delai_chargement)
    return navigateur