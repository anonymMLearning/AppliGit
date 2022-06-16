import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *
from exportExcelMarche import *

prod = db.session.query(Prod).filter(Prod.annee == 2021, Prod.mois == 1,
                                     Prod.type == "valide").all()
for p in prod:
    print(p.coutTeam)
