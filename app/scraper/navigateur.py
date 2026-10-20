from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def creer_navigateur(invisible=False):
    options = Options()
    if invisible:
        options.add_argument("-headless")
    options.set_preference("intl.accept_languages", "fr-FR")
    return webdriver.Firefox(options=options)