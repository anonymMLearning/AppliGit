import os

import bs4
import requests as requests
# from flask import request
from urllib import request
from models import *

collab1 = Collab("nom1", "prenom1", 1)
collab2 = Collab("nom2", "prenom2", 1)
collabs = [collab1, collab2]


# bc1.collabs.append(collab1)
# bc1.collabs.append(collab2)
# db.session.add(bc1)
# db.session.commit()
# print(bc1.collabs.nom)

def getURL(page):
    """

    :param page: html of web page (here: Python home page)
    :return: urls in that page
    """
    start_link = page.find("a href")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1: end_quote]
    return url


# url = os.environ["REQUEST_URL"]
# r = requests.get(url)
# id_collab = r.url[39:]
# print(id_collab)

# dates = db.session.query(Date).filter(Date.annee == 2022, Date.mois == 2).all()
# for date in dates :
# print(date.jour,date.mois,date.annee)


imp = db.session.query(Imputation).all()
# for i in imp:
# print(i.joursAllouesTache)
jours = db.session.query(Imputation).filter(Imputation.acti_id == 1, Imputation.collab_id == 1,
                                            Imputation.date_id == 35).all()
# print(jours[0].get_jours())


imps = db.session.query(Imputation).filter(Imputation.collab_id == 1, Imputation.date_id == 35).all()
# for i in imps:
# print(i.joursAllouesTache)

# print(Date(26, 3, 2022).transfoDate().weekday())
# print(columnMois(1, 2022))
# print(columnMois(2, 2022))
# print(column)
numSemaine = 1

dates = db.session.query(Date).filter(Date.mois == 1, Date.annee == 2022).all()
date_access = []
for date in dates:
    if date.numSemaine() == numSemaine:
        date_access.append(date)
# print(date_access)
"""
collab = db.session.query(Collab).get(1)
boncomms = collab.boncomms
dates = db.session.query(Date).filter(Date.mois == 2, Date.annee == 2022).all()
columns = columnMois(2, 2022)
imput = []
for boncomm in boncomms:
    for column in columns:
        numSemaine = column[0]
        date_access = []
        jourImpute = 0
        for date in dates:
            if date.numSemaine() == numSemaine:
                date_access.append(date)
        #print(date_access)
        for jour in date_access:
            imputation = db.session.query(Imputation).filter(Imputation.date_id == jour.id_date,
                                                        Imputation.collab_id == 1,
                                                        Imputation.acti_id == boncomm.id_acti).all()
            #print(imputation)
           #if imputation[0].get_jours() == 1:
                #jourImpute += 1
        imput.append([numSemaine, jourImpute])

imp = db.session.query(Imputation).filter(Imputation.date_id == 35,
                                                        Imputation.collab_id == 1,
                                                        Imputation.acti_id == 1).all()

imp = db.session.query(Imputation).all()
#print(imp[0].get_jours())
"""
"""
collabs=db.session.query(Collab).all()
#print(collabs)
collab = collabs[0]
#print(collab.nom)
boncomms = collab.boncomms
#print(boncomms)
for boncomm in boncomms:
    if boncomm.nbCongesTot !=0:
        print(boncomm.activite)
        boncomms.remove(boncomm)
#print(boncomms)"""

collabs = db.session.query(Collab).all()
# for collab in collabs:

# print(collab.boncomms)
"""
data2 = db.session.query(Boncomm).filter(Boncomm.nbJoursFormation == 0, Boncomm.nbCongesTot == 0,
                                                                         Boncomm.nbJoursAutre == 0).all()
                                        
print(data2)
for boncomm in data2:
    print(boncomm.collabs[0].collab)

collab = db.session.query(Collab).get(1)
assos = collab.boncomms
boncomms = []
for asso in assos:
    boncomms.append(asso.boncomm)
print(boncomms)
for boncomm in boncomms:
    imputation = db.session.query(Imputation).filter(
        Imputation.acti_id == boncomm.id_acti,
        Imputation.collab_id == 2,
        Imputation.date_id == 3
    ).all()
    if imputation[0] == []:
        print(imp)"""

boncomm = db.session.query(Boncomm).get(1)
data = []
# for boncomm in boncomms:
# print(boncomm)
"""collabs = db.session.query(Collab).all()
data = []
for collab in collabs:
    boncomms = collab.boncomms
    for i in range(len(boncomms)):
        print(boncomms[i].boncomm)
collabs = boncomm.collabs
for collab in collabs:
    print(collab.collab.id_collab)

boncomm = db.session.query(Boncomm).get(5)
print(boncomm.activite)
assocs=db.session.query(AssociationBoncommCollab).filter(AssociationBoncommCollab.boncomm_id==5).all()
for assoc in assocs:
    print(assoc.joursAllouesBC)

collabs = db.session.query(Collab).all()
imputations = db.session.query(Imputation).all()
boncomms = []
bons = db.session.query(Boncomm).filter(Boncomm.nbJoursFormation == 0, Boncomm.nbCongesTot == 0,
                                        Boncomm.nbJoursAutre == 0).all()
bonsGDP = []
for bon in bons:  # On ne veut pas les parts de GdP
    if bon.activite[0:4] == "CP -":
        bonsGDP.append(bon)
        bons.remove(bon)
print(len(bons))
print(len(bonsGDP))"""

collab = db.session.query(Collab).get(5)
assos = collab.boncomms
for asso in assos:
    if asso.boncomm.nbCongesTot != 0:
        conges = boncomm

date = db.session.query(Date).filter(Date.annee == 2021, Date.mois == 2, Date.jour == 22).all()
date = date[0]
imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                          Imputation.collab_id == collab.id_collab,
                                          Imputation.acti_id == conges.id_acti).all()[0]
imp.joursAllouesTache = 1
db.session.commit()
