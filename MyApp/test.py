import os

import bs4
import requests as requests
from flask import request
from urllib import request
from models import *
from exportExcelMarche import *

collab = db.session.query(Collab).all()[0]
print(collab.scrs)


