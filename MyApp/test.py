import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *

date = db.session.query(Date).get(3653)
print(date)
#print(date.jour,date.mois,date.annee)

