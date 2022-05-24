import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *
from exportExcelMarche import *

uos = db.session.query(UO).all()
for uo in uos:
    db.session.delete(uo)

db.session.commit()
