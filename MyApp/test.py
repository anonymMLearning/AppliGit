import os

import bs4
import requests as requests
from flask import request
from urllib import request
from models import *
from exportExcelMarche import *

bcs = db.session.query(Boncomm).all()
for bc in bcs:
    print(bc.id_acti)
