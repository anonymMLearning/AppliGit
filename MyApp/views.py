import os

import bs4
import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

if __name__ == "__main__":
    app.run()

# Config options - Make sure you created a 'config.py' file.
app.config.from_object('config')

# Create database connection object
db = SQLAlchemy(app)

from .models import *
from datetime import datetime

""" --- Accueil et initialisation de la BDD --- """


@app.route('/')
def acceuil():
    """
        Amène à la page d'accueil du site.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page d'acceuil avec les Collaborateurs pour qu'il s'affiche dans le formulaire de création d'un bon de commande.
    """
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('accueil.html', data=data)


@app.route('/init_db')
def init_db():
    """
        Initialise la base de donnée.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page d'acceuil avec la base de données initialisée, vide.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()
    return render_template('accueil.html')


@app.route('/see_conges')
def see_conges():
    conges = db.session.query(Boncomm).filter(Boncomm.nbJoursFormation == 0, Boncomm.caAtos == 0,
                                              Boncomm.nbJoursAutre == 0)
    collabs = db.session.query(Collab).filter(Collab.access != 4)
    return render_template('conges.html', conges=conges, collabs=collabs)


""" --- Partie collaborateur : enregistrer, modifier, effacer, voir ---"""


@app.route('/see_data_collab')
def see_data_collab():
    """
        Permet d'accéder à la page HTML contenant la liste des collaborateurs.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page HTML avec la liste des collaborateurs.
    """
    data = db.session.query(Collab).all()
    return render_template('collab.html', data=data)


@app.route('/save_collab', methods=['GET', 'POST'])
def save_collab():
    """
        Permet d'enregistrer un nouveau collaborateur.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page d'acceuil, en lui renvoyant les données des collaborateurs actualisées.
    """
    nom = request.form['nom']
    prenom = request.form['prenom']
    access = request.form['access']
    nbCongesTot = request.form['nbCongesTot']
    nom_conges = "Congés de " + nom + prenom
    collab = Collab(nom, prenom, access)
    conges = Boncomm(nom_conges, "", 0, 0, 0, 0, 0, 0, "", "", "", 0, "", 0, nbCongesTot, 0, 0)
    conges.collabs.append(collab)
    db.session.add(collab)
    db.session.add(conges)
    db.session.commit()
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('accueil.html', data=data)


@app.route('/deletecollab/<idc>')
def delete_collab(idc):
    """
        Permet de supprimer un collaborateur.

        Parameters
        ----------
        id
            id du collaborateur à supprimer.
        Returns
        -------
        render_template
            renvoie la page HTML avec la liste des collaborateurs, avec la liste des collaborateurs actualisée.
    """
    data_to_delete = db.session.query(Collab).get(idc)
    imputations = db.session.query(Imputation).filter(Imputation.collab_id == idc)
    for imputation in imputations:
        db.session.delete(imputation)
    db.session.delete(data_to_delete)
    db.session.commit()
    data = db.session.query(Collab).all()
    return render_template("collab.html", data=data)


@app.route('/modif_collab/<idc>', methods=['GET', 'POST'])
def modif_collab(idc):
    """
        Permet de modifier les attributs d'un collaborateur.

        Parameters
        ----------
        id
            id du collaborateur à modifier.
        Returns
        -------
        render_template
            renvoie la page HTML avec la liste des collaborateurs, avec la liste des collaborateurs actualisée.
    """
    nom = request.form['nom']
    prenom = request.form['prenom']
    access = request.form['access']
    data_to_change = db.session.query(Collab).get(idc)
    if nom != "":  # On ne modifie pas si l'utilisateur ne veut pas modifier le nom = champ vide
        data_to_change.nom = nom
    if prenom != "":  # On ne modifie pas si l'utilisateur ne veut pas modifier le prenom = champ vide
        data_to_change.prenom = prenom
    if access != data_to_change.access:  # On ne modifie pas si l'utilisateur ne veut pas modifier l'access
        data_to_change.access = access
    db.session.commit()
    data = db.session.query(Collab).all()
    return render_template('collab.html', data=data)


""" --- Partie Activite : enregistrer, modifier, effacer, voir --- """


@app.route('/see_data_boncomm')
def see_data_boncomm():
    """
        Permet de voir l'ensemble des activités.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page HTML avec la liste des activités, en lui donnant les données nécessaires à sa construction.
    """
    data2 = db.session.query(Boncomm).filter(Boncomm.nbJoursFormation == 0, Boncomm.nbCongesTot == 0,
                                             Boncomm.nbJoursAutre == 0).all()
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('activite.html', data=data, data2=data2)


@app.route('/save_formation', methods=['GET', 'POST'])
def save_formation():
    activite = request.form['activite2']
    com = request.form['com2']
    anneeTarif = request.form['anneeTarif2']
    horsProjet = request.form['hprojet']
    nbJoursFormation = request.form['nbjoursformation']
    formation = Boncomm(activite, com, anneeTarif, 0, 0, 0, 0, 0, "", "", "", 0, horsProjet, nbJoursFormation, 0, 0,
                        0)
    ids = request.form.getlist('collabs2')
    for idc in ids:
        data = db.session.query(Collab).get(idc)
        formation.collabs.append(data)
        data.boncomms.append(formation)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(formation.id_acti, idc, date.id_date, 0)
            db.session.add(imp)
    db.session.add(formation)
    db.session.commit()
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('accueil.html', data=data)


@app.route('/save_autre', methods=['GET', 'POST'])
def save_autre():
    activite = request.form['activite3']
    com = request.form['com3']
    anneeTarif = request.form['anneeTarif3']
    nbJoursAutre = request.form['nbjoursautre']
    formation = Boncomm(activite, com, anneeTarif, 0, 0, 0, 0, 0, "", "", "", 0, "", 0, 0, 0, nbJoursAutre)
    ids = request.form.getlist('collabs2')
    for idc in ids:
        data = db.session.query(Collab).get(idc)
        formation.collabs.append(data)
        data.boncomms.append(formation)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(formation.id_acti, idc, date.id_date, 0)
            db.session.add(imp)
    db.session.add(formation)
    db.session.commit()
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('accueil.html', data=data)


@app.route('/save_boncomm', methods=['GET', 'POST'])
def save_bonComm():
    """
        Permet de créer un nouveau bon de commande.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page d'acceuil.
    """
    activite = request.form['activite']
    com = request.form['com']
    anneeTarif = request.form['anneeTarif']
    caAtos = request.form['caAtos']
    jourThq = request.form['jourThq']
    partGDP = request.form['partGDP']
    delais = request.form['delais']
    montantHT = request.form['montantHT']
    partEGIS = request.form['partEGIS']
    num = request.form['num']
    poste = request.form['poste']
    projet = request.form['projet']
    tjm = request.form['tjm']
    bon = Boncomm(activite, com, anneeTarif, caAtos, int(jourThq) - int(partGDP), delais, montantHT, partEGIS, num,
                  poste, projet,
                  tjm, "", 0, 0, 0, 0)
    bonGDP = Boncomm('CP - ' + activite, com, anneeTarif, caAtos, partGDP, delais, montantHT, partEGIS, num, poste,
                     projet,
                     tjm, "", 0, 0, 0, 0)
    ids = request.form.getlist('collabs')
    for idc in ids:
        data = db.session.query(Collab).get(idc)
        bon.collabs.append(data)
        data.boncomms.append(bon)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(bon.id_acti, idc, date.id_date, 0)
            db.session.add(imp)

    idGDP = request.form.getlist('collabsGDP')
    for idc in idGDP:
        data = db.session.query(Collab).get(idc)
        bonGDP.collabs.append(data)
        data.boncomms.append(bonGDP)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(bonGDP.id_acti, idc, date.id_date, 0)
            db.session.add(imp)
    db.session.add(bon)
    db.session.add(bonGDP)
    db.session.commit()
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('accueil.html', data=data)


@app.route('/modif_activite/<idb>', methods=['GET', 'POST'])
def modif_activite(idb):
    """
        Permet de modifier les attributs d'un bon de commande.

        Parameters
        ----------
        id
            id du bon de commande à modifier.
        Returns
        -------
        render_template
            renvoie la page HTML avec la liste des bons de commandes, avec cette liste actualisée.
    """
    activite = request.form['activite']
    com = request.form['com']
    anneeTarif = request.form['anneeTarif']
    caAtos = request.form['caAtos']
    jourThq = request.form['jourThq']
    partGDP = request.form['partGDP']
    delais = request.form['delais']
    montantHT = request.form['montantHT']
    partEGIS = request.form['partEGIS']
    num = request.form['num']
    poste = request.form['poste']
    projet = request.form['projet']
    tjm = request.form['tjm']
    data_to_change = db.session.query(Boncomm).get(idb)
    if activite != "":
        data_to_change.activite = activite
    if com != "":
        data_to_change.com = com
    if anneeTarif != data_to_change.anneeTarif:
        data_to_change.anneeTarif = anneeTarif
    if caAtos != data_to_change.caAtos:
        data_to_change.caAtos = caAtos
    if jourThq != data_to_change.jourThq:
        data_to_change.jourThq = jourThq
    if partGDP != data_to_change.partGDP:
        data_to_change.partGDP = partGDP
    if delais != data_to_change.delais:
        data_to_change.delais = delais
    if montantHT != data_to_change.montantHT:
        data_to_change.montantHT = montantHT
    if partEGIS != data_to_change.partEGIS:
        data_to_change.partEGIS = partEGIS
    if num != "":
        data_to_change.num = num
    if poste != "":
        data_to_change.poste = poste
    if projet != "":
        data_to_change.projet = projet
    if tjm != data_to_change.tjm:
        data_to_change.tjm = tjm
    ids = request.form.getlist('collabs')
    for idc in ids:
        data = db.session.query(Collab).get(idc)
        data_to_change.collabs.append(data)
        data.boncomms.append(data_to_change)
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(data_to_change.id_acti, idc, date.id_date, 0)
            db.session.add(imp)

    db.session.commit()
    data2 = db.session.query(Boncomm).filter(Boncomm.nbJoursFormation == 0, Boncomm.nbCongesTot == 0,
                                             Boncomm.nbJoursAutre == 0).all()
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('activite.html', data=data, data2=data2)


@app.route('/see_save_activite')
def see_save_activite():
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('saveactivite.html', data=data)


@app.route('/deleteactivite/<idb>')
def delete_activite(idb):
    """
        Permet de supprimer un bon de commande.

        Parameters
        ----------
        idb
            id du bon de commande à supprimer.
        Returns
        -------
        render_template
            renvoie la page HTML avec la liste des bons de commande, avec cette liste actualisée.
    """
    data_to_delete = db.session.query(Boncomm).get(idb)
    db.session.delete(data_to_delete)
    db.session.commit()
    data2 = db.session.query(Boncomm).all()
    return render_template("activite.html", data2=data2)


""" --- Partie Date : voir, enregistrer ---"""


@app.route('/init_date')
def init_date():
    """
        Initialise la base de donnée.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page d'acceuil avec la base de données initialisée, vide.
    """
    for annee in range(10):
        for mois in range(12):
            if mois == 1:  # Mois de février
                for jour in range(28):
                    db.session.add(Date(jour + 1, mois + 1, 2022 + annee))
                if ((2022 + annee) - 2020) % 4 == 0:  # Année bisextile
                    db.session.add(Date(29, 2, 2022 + annee))
            else:
                for jour in range(30):  # Ajout des 31 pour les mois concernés
                    db.session.add(Date(jour + 1, mois + 1, 2022 + annee))
        db.session.add(Date(31, 1, 2022 + annee))
        db.session.add(Date(31, 3, 2022 + annee))
        db.session.add(Date(31, 5, 2022 + annee))
        db.session.add(Date(31, 7, 2022 + annee))
        db.session.add(Date(31, 8, 2022 + annee))
        db.session.add(Date(31, 10, 2022 + annee))
        db.session.add(Date(31, 12, 2022 + annee))
        db.session.commit()
        data = db.session.query(Collab).filter(Collab.access != 4).all()
    return render_template('accueil.html', data=data)


@app.route('/see_data_date')
def see_data_date():
    """
        Amène à la page HTML montrant l'ensemble des dates.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page HTML avec l'ensemble des dates enregistrées dans la BDD.
    """
    data3 = db.session.query(Date).all()
    return render_template('date.html', data3=data3)


""" --- Partie Imputation : enregistrer, voir ---"""


@app.route('/save_imputation/<idc>/<annee>/<mois>', methods=['GET', 'POST'])
def save_imputation(idc, annee, mois):
    """
        Permet créer une nouvelle imputation.

        Parameters
        ----------
        idc
            id du collaborateur associé
        idb
            id du bon de commande associé
        idd
            id de la date associée

        Returns
        -------
        render_template
            renvoie la page HTML avec l'ensemble des imputations associées à ce collaborateur.
    """
    columns = columnMois(mois, annee)
    collab = db.session.query(Collab).get(idc)
    boncomms = collab.boncomms
    for boncomm in boncomms:  # On enlève les congés associés au collaborateur
        if boncomm.nbCongesTot != 0:
            boncomms.remove(boncomm)
    data_boncomms = []  # liste qui contiendra pour chasue bon de commande l'imputation sur chaque semaine
    for boncomm in boncomms:
        imputBC = []
        for column in columns:
            numSemaine = column[0]
            jours = request.form[str(boncomm.id_acti) + "/" + str(numSemaine)]
            dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
            date_access = []  # Toutes les dates de la semaine en cours où l'on peut imputer
            for date in dates:
                if date.numSemaine() == numSemaine:
                    date_access.append(date)
            for jour in date_access:  # On supprime les imputations sur ces dates pour récréer en fonction du nombre
                # de jours nécessaires
                imp = db.session.query(Imputation).filter(Imputation.collab_id == idc,
                                                          Imputation.date_id == jour.id_date,
                                                          Imputation.acti_id == boncomm.id_acti).all()
                db.session.delete(imp[0])
            for i in range(int(jours)):  # On crée int(jours) imputation sur les jours de cette semaine
                date = date_access[i]
                imp = Imputation(boncomm.id_acti, idc, date.id_date, 1)
                db.session.add(imp)
            for j in range(len(date_access) - int(
                    jours)):  # Pour les jours restants, on recrée des imputations avec le nombre de jours alloués = 0
                date = date_access[int(jours) + j]
                imp = Imputation(boncomm.id_acti, idc, date.id_date, 0)
                db.session.add(imp)

            imputBC.append([numSemaine, int(jours)])
        data_boncomms.append([boncomm, imputBC])
        db.session.commit()
    columns = columnMois(mois, annee)
    dates = db.session.query(Date).filter(Date.annee == annee, Date.mois == mois).all()
    mois = dates[0].mois
    annee = dates[0].annee
    return render_template('imputcollab.html', boncomms=data_boncomms, columns=columns, collab=collab, annee=annee,
                           mois=mois)


@app.route('/see_imput_collab/<idc>')
def see_imput_collab(idc):
    """
        Permet de voir les imputations d'un collaborateur.

        Parameters
        ----------
        idc
            id du collaborateur
        Returns
        -------
        render_template
            renvoie la page HTML avec les imputations du collaborateurs, en lui donnant les données nécessaires à sa construction.
    """
    collab = db.session.query(Collab).get(idc)
    boncomms = collab.boncomms
    for boncomm in boncomms:
        if boncomm.nbCongesTot != 0:
            boncomms.remove(boncomm)
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    columns = columnMois(mois,
                         annee)  # On calcule les numéros de semaines et nombres de jours dispo pour le mois en cours
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    data_boncomms = []
    for boncomm in boncomms:
        imput = []
        for column in columns:
            numSemaine = column[0]
            date_access = []
            jourImpute = 0
            for date in dates:
                if date.numSemaine() == numSemaine:
                    date_access.append(date)
            for jour in date_access:
                imputation = db.session.query(Imputation).filter(Imputation.acti_id == boncomm.id_acti,
                                                                 Imputation.collab_id == idc,
                                                                 Imputation.date_id == jour.id_date
                                                                 ).all()
                if imputation[0].get_jours() == 1:
                    jourImpute += 1  # En fonction du nb d'imputation avec le nombre de jours alloués = 1, on calcule le
                    # nb de jours imputés sur la semaine
            imput.append([numSemaine, jourImpute])
        data_boncomms.append([boncomm, imput])
    return render_template('imputcollab.html', boncomms=data_boncomms, collab=collab, columns=columns,
                           annee=annee, mois=mois)


@app.route('/see_imput_global')
def see_imput_global():
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
    for i in range(len(bons)):
        boncomms.append([i, bons[i], bonsGDP[i]])

    valeursBoncomms = []
    valeursBoncommsGDP = []
    for j in range(len(boncomms)):
        valeurs = valeursGlobales(boncomms[j][1])
        valeursGDP = valeursGlobales(boncomms[j][2])
        valeursBoncomms.append(valeurs)
        valeursBoncommsGDP.append(valeursGDP)

    return render_template('imputglobal.html', collabs=collabs, boncomms=boncomms,
                           imputations=imputations,
                           valeursBoncomms=valeursBoncomms, valeursBoncommsGDP=valeursBoncommsGDP)
