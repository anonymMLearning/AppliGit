import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *

dates = db.session.query(Date).filter(Date.annee < 2024, Date.annee > 2021, Date.mois < 6, Date. mois > 1).all()
for date in dates:
    print(date.annee, date.mois)
