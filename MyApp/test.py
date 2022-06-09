import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *
from exportExcelMarche import *


scr = db.session.query(SCR).all()
for s in scr:
    print(s.collabs)
