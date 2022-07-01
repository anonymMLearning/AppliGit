import os

import bs4
import requests as requests
from flask import request
from urllib import request
from models import *
from exportExcelMarche import *

bon = db.session.query(Boncomm).all()[-1]
print(bon.num)


