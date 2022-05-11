import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *

collab = db.session.query(Collab).all()[-1]
idc = collab.id_collab
imputations = db.session.query(Imputation).filter(Imputation.collab_id == idc).all()
for imputation in imputations:  # On supprime les imputations de ce collaborateur.
    db.session.delete(imputation)
associations = db.session.query(AssociationBoncommCollab).filter(
    AssociationBoncommCollab.collab_id == idc).all()
for assoc in associations:  # On supprime les associations de ce collaborateur.
    db.session.delete(assoc)
associations = db.session.query(AssoCollabFonction).filter(
    AssoCollabFonction.collab_id == idc).all()
for assoc in associations:  # On supprime les associations de ce collaborateur.
    db.session.delete(assoc)
db.session.delete(collab)
db.session.commit()
