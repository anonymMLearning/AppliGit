import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *

data_to_change = db.session.query(Collab).get(1)
assoFonctions = data_to_change.fonctions
for assoFonction in assoFonctions:
    fonction = assoFonction.fonction
    print(fonction.nom, fonction.tjm)
