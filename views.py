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

from .exportExcel import *
from .models import *
from datetime import datetime

"""----------------------------------------- Gestion des différentes erreurs ----------------------------------------"""


@app.errorhandler(404)
def error404(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 404


@app.errorhandler(500)
def error500(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 500


@app.errorhandler(400)
def error400(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 400


@app.errorhandler(401)
def error401(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 401


@app.errorhandler(403)
def error403(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 403


@app.errorhandler(405)
def error405(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 405


@app.errorhandler(404)
def error404(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 404


@app.errorhandler(502)
def error502(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 502


@app.errorhandler(503)
def error401(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 503


@app.errorhandler(504)
def error504(e):
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('error.html', e=e, data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr), 504


"""------------------------------------------------------------------------------------------------------------------"""

""" --- Accueil, initialisation de la BDD et données d'imputation --- """


@app.route('/')
def acceuil():
    """
        Amène à la page d'accueil du site.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page d'acceuil.
    """
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    # On montre dans la barre de navigation que les collaborateurs de l'équipe MS4 :
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('accueil.html', data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr)


@app.route('/export_excel', methods=['GET', 'POST'])
def export_excel_imputations():
    """
        Exporte les données de la base sous format excel.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page d'acceuil.
    """
    export_excel()  # Appel de la méthode codée dans le fichier exportExcel.py
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    moisStr = stringMois(str(mois))
    return render_template('accueil.html', data_navbar=data_navbar, mois=mois, annee=annee, moisStr=moisStr)


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
    for annee in range(10):
        for mois in range(12):
            prodValide = Prod(mois + 1, 2021 + annee, "valide", 0, 0, 0, 4, 0)
            prodValide.coutTeam = 0  # Si ces 2 lignes ne sont pas rajoutées, coutTeam et jourMoisTeam sont = None,
            prodValide.jourMoisTeam = 18  # seule solution que j'ai trouvé pour résoudre le problème est de réaffecter une valeur.
            db.session.add(prodValide)
            prodReel = Prod(mois + 1, 2021 + annee, "reel", 0, 0, 0, 2, 0)
            prodReel.coutTeam = 0
            prodReel.jourMoisTeam = 18
            db.session.add(prodReel)
            if mois == 1:  # Mois de février
                for jour in range(28):
                    # 500 le TJM init, 6 le nombre de membres dans l'équipe init, 400 le SCR moyen retenu :
                    db.session.add(Date(jour + 1, mois + 1, 2021 + annee, 0, 500, 6, 400))
                if ((2021 + annee) - 2020) % 4 == 0:  # Année bisextile
                    db.session.add(Date(29, 2, 2021 + annee, 0, 500, 6, 400))
            else:
                for jour in range(30):  # Ajout des 31 pour les mois concernés
                    db.session.add(Date(jour + 1, mois + 1, 2021 + annee, 0, 500, 6, 400))
        db.session.add(Date(31, 1, 2021 + annee, 0, 500, 6, 400))
        db.session.add(Date(31, 3, 2021 + annee, 0, 500, 6, 400))
        db.session.add(Date(31, 5, 2021 + annee, 0, 500, 6, 400))
        db.session.add(Date(31, 7, 2021 + annee, 0, 500, 6, 400))
        db.session.add(Date(31, 8, 2021 + annee, 0, 500, 6, 400))
        db.session.add(Date(31, 10, 2021 + annee, 0, 500, 6, 400))
        db.session.add(Date(31, 12, 2021 + annee, 0, 500, 6, 400))
    db.session.commit()
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data = db.session.query(Collab).filter(Collab.access != 4).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    return render_template('accueil.html', data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/see_conges')
def see_conges():
    """
        Amène à la page des congés.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page des congés avec les données nécessaires à sa construction.
    """
    data_collabs = db.session.query(Collab).all()
    collabs = []
    conges = []
    dateNow = str(datetime.now())
    mois_courant = int(dateNow[5:7])
    annee_courant = int(dateNow[:4])
    for i in range(len(data_collabs)):  # On va récupérer les congés de chaque collaborateur
        assos = data_collabs[i].boncomms
        for asso in assos:  # On va récupérer uniquement les congés dans les activités de ce collaborateur
            if asso.boncomm.nbCongesTot != 0:  # Cette asso est celle liée aux congés du collaborateur
                conges.append(asso.boncomm)
                congesAn = 0  # Sur la page, la colonne congés posés ne contient que ceux de l'année en cours
                imputations = db.session.query(Imputation).filter(Imputation.acti_id == asso.boncomm.id_acti,
                                                                  Imputation.collab_id == data_collabs[i].id_collab,
                                                                  Imputation.joursAllouesTache != 0,
                                                                  Imputation.type == "client").all()
                for imputation in imputations:
                    date = db.session.query(Date).get(imputation.date_id)
                    if date.annee == annee_courant:
                        congesAn += imputation.joursAllouesTache
        collabs.append([i, data_collabs[i], congesAn])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])

    return render_template('conges.html', conges=conges, collabs=collabs, data_navbar=data_navbar,
                           mois_courant=mois_courant,
                           annee_courant=annee_courant)


@app.route('/see_poser_conges/<idc>', methods=['GET', 'POST'])
def see_poser_conges(idc):
    """
        Amène à la page pour poser des congés pour un collaborateur, en demandant à l'utilisateur de choisir le mois
        et l'année.

        Parameters
        ----------
        idc
            id du collaborateur
        Returns
        -------
        render_template
            renvoie la page pour poser des congés avec les données nécessaires à sa construction.
    """
    mois = request.form['mois']
    annee = request.form['annee']
    dates = db.session.query(Date).filter(Date.annee == annee, Date.mois == mois).all()
    collab = db.session.query(Collab).get(idc)
    assos = collab.boncomms
    for asso in assos:  # On récupère uniquement les congés du collab parmis ses activités.
        if asso.boncomm.nbCongesTot != 0:
            conges = asso.boncomm
    lignes_date = []
    columns = columnMoisWeekEnd(mois, annee)
    """---------- Cas de la première ligne ----------  """
    numLigne = 0
    ligne_1 = []
    nbJoursSem1 = columns[0][1]
    for i in range(7 - nbJoursSem1):  # Pour les jours du mois précédent, on met des cases vides dans le tableau.
        ligne_1.append(["", 0, "Ne pas remplir"])
    numSem1 = columns[0][0]
    i = 0
    date = dates[i]
    while date.numSemaine() == numSem1:  # Pour les jours de la première semaine du mois.
        if date.estFerie():
            case = "Férié"
            i += 1
            ligne_1.append([date, 1, case])  # On met de base 1 si le jour est férié.
        else:
            case = "Disponible"
            i += 1
            imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                      Imputation.collab_id == idc,
                                                      Imputation.acti_id == conges.id_acti,
                                                      Imputation.type == "client").all()
            ligne_1.append([date, imp[0].joursAllouesTache, case])
        date = dates[i]
    lignes_date.append([numLigne, ligne_1])
    """---------- Cas des autres lignes ----------  """
    nbSemaine = len(columns)
    for k in range(nbSemaine - 2):  # On ne compte pas la première et la dernière.
        numLigne = k + 1
        ligne = []
        numSem = columns[k + 1][0]  # de la 2ème à l'avant dernière.
        for date in dates:  # On ne fait la méthode que sur les jours de la semaine choisi en début de boucle for.
            if date.numSemaine() == numSem:
                if date.estFerie():
                    case = "Férié"
                    ligne.append([date, 1, case])
                else:
                    case = "Disponible"
                    imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                              Imputation.collab_id == idc,
                                                              Imputation.acti_id == conges.id_acti,
                                                              Imputation.type == "client").all()
                    ligne.append([date, imp[0].joursAllouesTache, case])
        lignes_date.append([numLigne, ligne])
    """---------- Cas de la dernière ligne ----------  """
    dern_ligne = []
    numLigne = nbSemaine - 1
    nbJoursDernSem = columns[-1][1]
    numDernSem = columns[-1][0]
    for date in dates:  # On va remplir les cases de la dernière lignes pour les derniers jours du mois.
        if date.numSemaine() == numDernSem:
            if date.estFerie():
                case = "Férié"
                dern_ligne.append([date, 1, case])
            else:
                case = "Disponible"
                imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                          Imputation.collab_id == idc,
                                                          Imputation.acti_id == conges.id_acti,
                                                          Imputation.type == "client").all()
                dern_ligne.append([date, imp[0].joursAllouesTache, case])
    for i in range(
            7 - nbJoursDernSem):  # Pour le reste des jours de la semaine, cases vides car jours du mois suivant.
        dern_ligne.append(["", 0, "Ne pas remplir"])
    lignes_date.append([numLigne, dern_ligne])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collaborateur in data:
        data_navbar.append([collaborateur.abreviation(), collaborateur])
    dateNow = str(datetime.now())
    mois_courant = int(dateNow[5:7])
    annee_courant = int(dateNow[:4])
    moisStr = stringMois(str(mois))
    return render_template('poseconges.html', idc=idc, lignes_date=lignes_date, data_navbar=data_navbar,
                           mois_courant=mois_courant,
                           annee_courant=annee_courant, mois=mois, annee=annee, moisStr=moisStr)


@app.route('/poser_conges/<idc>/<annee>/<mois>', methods=['GET', 'POST'])
def poser_conges(idc, mois, annee):
    """
        Enregistre les congés remplis par le collaborateur sur le mois et l'année précedemment sélectionné.

        Parameters
        ----------
        idc
            id du collaborateur
        mois
            mois choisit par le collaborateur
        annee
            annee choisit par le collaborateur
        Returns
        -------
        render_template
            renvoie la page des congés avec les données nécessaires à sa construction.
    """
    dateNow = str(datetime.now())
    mois_courant = int(dateNow[5:7])
    annee_courant = int(dateNow[:4])
    collab = db.session.query(Collab).get(idc)
    assos = collab.boncomms
    for asso in assos:
        if asso.boncomm.nbCongesTot != 0:
            conges = asso.boncomm
    data_dates = db.session.query(Date).filter(Date.annee == annee, Date.mois == mois).all()
    columns = columnMoisWeekEnd(mois, annee)
    dates = []  # Liste contenant les dates et les cases vides du formulaire pour faire correspondre les id
    nbJoursSem1 = columns[0][1]
    for i in range(7 - nbJoursSem1):  # Construction identique à la méthode see_poser_conges
        dates.append("")
    for date in data_dates:
        dates.append(date)
    nbJoursDernSem = columns[-1][1]
    for i in range(7 - nbJoursDernSem):
        dates.append("")
    nbJourPose = 0
    for j in range(len(dates)):  # On parcourt chaque case du tableau
        date = dates[j]
        if date != "" and not date.estFerie():  # On n'applique la méthode que sur les jours non fériés
            jourPose = request.form[str(j + 1)]
            if jourPose != "":
                imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                          Imputation.collab_id == idc,
                                                          Imputation.acti_id == conges.id_acti, ).all()
                if imp[0].joursAllouesTache != jourPose:
                    previousJourPose = imp[0].joursAllouesTache
                    diffJourPose = float(jourPose) - previousJourPose  # écart entre jours posés avant/après
                    imp[0].joursAllouesTache = jourPose
                    imp[1].joursAllouesTache = jourPose
                    nbJourPose += float(
                        diffJourPose)  # Contiendra la différence des congés entre avant et après l'enregistrement
    conges.nbCongesPose += nbJourPose
    db.session.commit()
    data_collabs = db.session.query(Collab).all()
    collabs = []
    conges = []
    for i in range(len(data_collabs)):
        assos = data_collabs[i].boncomms
        for asso in assos:
            if asso.boncomm.nbCongesTot != 0:
                conges.append(asso.boncomm)
                congesAn = 0
                imputations = db.session.query(Imputation).filter(Imputation.acti_id == asso.boncomm.id_acti,
                                                                  Imputation.collab_id == data_collabs[i].id_collab,
                                                                  Imputation.joursAllouesTache != 0,
                                                                  Imputation.type == "client").all()
                for imputation in imputations:
                    date = db.session.query(Date).get(imputation.date_id)
                    if date.annee == annee_courant:
                        congesAn += imputation.joursAllouesTache
        collabs.append([i, data_collabs[i], congesAn])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])

    return render_template('conges.html', conges=conges, collabs=collabs, data_navbar=data_navbar,
                           mois_courant=mois_courant,
                           annee_courant=annee_courant)


@app.route('/see_archives')
def see_archives():
    """
        Amène à la page des données d'imputation.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page des données d'imputation avec les données nécessaires à sa construction.
    """
    collabs = db.session.query(Collab).all()  # On montre même les collaborateur DP et partis
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in data:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('menuarchives.html', collabs=collabs, data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/see_archives_collab', methods=['GET', 'POST'])
def see_archives_collab():
    """
        Amène à la page des imputations pour un collab, un mois et une annee choisit.

        Parameters
        ----------

        Returns
        -------
        render_template
            renvoie la page des imputations voulues avec les données nécessaires à sa construction.
    """
    idc = request.form['collab']
    mois = request.form['mois']
    annee = request.form['annee']
    collab = db.session.query(Collab).get(idc)
    assos = collab.boncomms
    boncomms = []
    for i in range(len(assos)):  # On va séparer les congés des autres activités
        boncomm = assos[i].boncomm
        if boncomm.nbCongesTot == 0:
            boncomms.append(boncomm)
        elif boncomm.nbCongesTot != 0:
            conges = boncomm
    columns = columnMois(mois,
                         annee)  # On calcule les numéros de semaines et nombres de jours dispo pour le mois en cours
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    data_boncomms = []
    calcJoursDispo = True  # Variable pour calculer une seule fois les jours dispos par semaine dans la boucle des dates
    for i in range(len(boncomms)):  # Pour chaque activité qui sera une ligne du tableau
        imput = []
        for column in columns:
            numSemaine = column[0]
            date_access = []
            jourImpute = 0
            for date in dates:
                if date.numSemaine() == numSemaine:
                    date_access.append(date)
            for jour in date_access:
                if calcJoursDispo:  # On calcule une seule fois les jours dispo dans la semaine par rapport aux
                    # congés posés
                    jour_conges = db.session.query(Imputation).filter(
                        Imputation.acti_id == conges.id_acti,
                        Imputation.collab_id == idc,
                        Imputation.date_id == jour.id_date
                    ).all()[0].joursAllouesTache
                    if jour_conges != 0:  # Si un congés est posé cette semaine, on enlève 1 jour de disponible dans
                        # cette dernière.
                        column[1] -= jour_conges
                imputation = db.session.query(Imputation).filter(
                    Imputation.acti_id == boncomms[i].id_acti,
                    Imputation.collab_id == idc,
                    Imputation.date_id == jour.id_date, Imputation.type == "client"
                ).all()
                if imputation[0].joursAllouesTache != 0:
                    jourImpute += imputation[
                        0].joursAllouesTache  # En fonction du nombre d'imputation avec le nombre de jours alloués != 0,
                    # on calcule le nb de jours imputés sur la semaine.
            imput.append([numSemaine, float(jourImpute)])
        calcJoursDispo = False
        assoCollabBC = db.session.query(AssociationBoncommCollab).filter(
            AssociationBoncommCollab.collab_id == idc,
            AssociationBoncommCollab.boncomm_id == boncomms[i].id_acti).all()
        imputations = db.session.query(Imputation).filter(Imputation.acti_id == boncomms[i].id_acti,
                                                          Imputation.collab_id == idc,
                                                          Imputation.joursAllouesTache != 0,
                                                          Imputation.type == "client").all()
        dejaConso = 0  # On va récupèrer les données de ce qui est déjà conso et ce qu'il reste à faire.
        for imputation in imputations:
            dejaConso += imputation.joursAllouesTache
        joursAlloues = assoCollabBC[0].joursAllouesBC  # jours alloués à ce collab sur ce BC
        data_boncomms.append([boncomms[i], imput, joursAlloues, joursAlloues - dejaConso])
    data = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collaborateur in data:
        data_navbar.append([collaborateur.abreviation(), collaborateur])
    dateNow = str(datetime.now())
    mois_courant = int(dateNow[5:7])
    annee_courant = int(dateNow[:4])
    moisStr = stringMois(mois)
    return render_template('imputcollab.html', boncomms=data_boncomms, collab=collab, columns=columns,
                           annee=annee, mois=mois, moisStr=moisStr, data_navbar=data_navbar,
                           mois_courant=mois_courant,
                           annee_courant=annee_courant)


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
    collabs = db.session.query(Collab).all()
    data = []
    for collab in collabs:
        assos = collab.boncomms
        boncomms = []
        for i in range(len(assos)):  # On ne prendra pas les congés et les bons sur lequel on a modifié ses jours
            # alloués en les passant à 0.
            boncomm = assos[i].boncomm
            if boncomm.nbCongesTot == 0 and assos[i].joursAllouesBC != 0 and boncomm.etat != 'TE':
                boncomms.append(boncomm)
        data.append(
            [collab, boncomms])  # Si on veut afficher les BC auquels le collab est lié, ils sont contenu dans boncomms
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    data_collab = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collaborateur in data_collab:
        data_navbar.append([collaborateur.abreviation(), collaborateur])
    return render_template('collab.html', data=data, mois=mois, annee=annee, data_navbar=data_navbar)


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
    nom = request.form['nom_save']
    prenom = request.form['prenom_save']
    access = request.form['access_save']
    nbCongesTot = request.form['conges_save']
    nom_conges = "Congés de " + nom + " " + prenom  # Nom générique pour les congés d'un collab
    collab = Collab(nom, prenom, access, "", 0)
    collab.gcm_id = 0  # Pour les futures versions, on initialise le GCM lié au collab
    # On crée les congés du collaborateur
    conges = Boncomm(nom_conges, "", "", 0, 0, 0, 0, 0, 0, "", "", "", 0, "", "", "", "", "", "", "", "", 0,
                     nbCongesTot, 0, 0, "", "", "", "", 0)
    assoc = AssociationBoncommCollab(joursAllouesBC=int(nbCongesTot))
    assoc.collab = collab
    conges.collabs.append(assoc)  # On crée l'association entre les congés et le collab
    db.session.add(collab)
    db.session.add(conges)
    dates = db.session.query(Date).all()
    for date in dates:  # Initilialise les imputations à 0 sur toutes les dates pour les congés.
        imp = Imputation(conges.id_acti, collab.id_collab, date.id_date, 0, "client")
        impAtos = Imputation(conges.id_acti, collab.id_collab, date.id_date, 0, "atos")
        db.session.add(imp)
        db.session.add(impAtos)
    db.session.commit()
    collabs = db.session.query(Collab).all()
    data = []
    for collab in collabs:
        boncomms = collab.boncomms
        data_to_add = []
        for i in range(len(boncomms)):
            boncomm = boncomms[i].boncomm
            if boncomm.nbCongesTot == 0:
                data_to_add.append(boncomm)
        data.append([collab, data_to_add])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    return render_template('collab.html', data=data, mois=mois, annee=annee, data_navbar=data_navbar)


@app.route('/modif_collab/<idc>', methods=['GET', 'POST'])
def modif_collab(idc):
    """
    Permet de modifier les attributs d'un collaborateur.

    Parameters
    - ---------
    idc
        id du collaborateur à modifier.

    Returns
    - ------
    render_template
        renvoie la page HTML avec la liste des collaborateurs, avec la liste des collaborateurs actualisée.
    """
    nom = request.form['nom2']
    prenom = request.form['prenom2']
    access = request.form['access2']
    newConges = request.form['conges']
    data_to_change = db.session.query(Collab).get(idc)  # Collab à modifier
    prevConges = data_to_change.boncomms[0].boncomm.nbCongesTot
    if nom != "":  # On ne modifie pas si l'utilisateur ne veut pas modifier le nom = champ vide
        data_to_change.nom = nom
    if prenom != "":  # On ne modifie pas si l'utilisateur ne veut pas modifier le prenom = champ vide
        data_to_change.prenom = prenom
    if access != data_to_change.access:  # On ne modifie pas si l'utilisateur ne veut pas modifier l'access
        data_to_change.access = access
    if newConges != prevConges:  # On ne modifie pas si l'utilisateur ne veut pas modifier les jours de congés
        data_to_change.boncomms[0].boncomm.nbCongesTot = newConges
    db.session.commit()
    collabs = db.session.query(Collab).all()
    data = []
    for collab in collabs:
        boncomms = collab.boncomms
        data_to_add = []
        for i in range(len(boncomms)):
            boncomm = boncomms[i].boncomm
            if boncomm.nbCongesTot == 0:
                data_to_add.append(boncomm)
        data.append([collab, data_to_add])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    return render_template('collab.html', data=data, mois=mois, annee=annee, data_navbar=data_navbar)


@app.route('/deletecollab/<idc>')
def delete_collab(idc):
    """
    Permet de supprimer un collaborateur.

    Parameters
    - ---------
    idc
        id du collaborateur à supprimer.

    Returns
    - ------
    render_template
        renvoie la page HTML avec la liste des collaborateurs, avec cette liste actualisée.
    """
    data_to_delete = db.session.query(Collab).get(idc)
    imputations = db.session.query(Imputation).filter(Imputation.collab_id == idc).all()
    for imputation in imputations:  # On supprime les imputations de ce collaborateur.
        db.session.delete(imputation)
    associations = db.session.query(AssociationBoncommCollab).filter(
        AssociationBoncommCollab.collab_id == idc).all()
    for assoc in associations:  # On supprime les associations de ce collaborateur.
        db.session.delete(assoc)
    db.session.delete(data_to_delete)
    db.session.commit()
    collabs = db.session.query(Collab).all()
    data = []
    for collab in collabs:
        boncomms = collab.boncomms
        data_to_add = []
        for i in range(len(boncomms)):
            boncomm = boncomms[i].boncomm
            if boncomm.nbCongesTot == 0:
                data_to_add.append(boncomm)
        data.append([collab, data_to_add])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    return render_template('collab.html', data=data, mois=mois, annee=annee, data_navbar=data_navbar)


""" - -- Partie Activite: enregistrer, modifier, effacer, voir - -- """


@app.route('/see_data_boncomm')
def see_data_boncomm():
    """
    Permet de voir l'ensemble des activités.

    Parameters
    - ---------

    Returns
    - ------
    render_template
    """
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []  # On sépare les BC et GDP des Autres et Formations
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":  # On traite le cas des BC de GdP avec le BC qui lui est associé
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés qu'on ne veut pas afficher
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/save_formation', methods=['GET', 'POST'])
def save_formation():
    """
    Permet de créer une formation.

    Parameters
    - ---------

    Returns
    - ------
    render_template
    """
    activite = request.form['activite2']
    com = request.form['com2']
    anneeTarif = request.form['anneeTarif2']
    horsProjet = request.form['hprojet']
    nbJoursFormation = request.form['nbjoursformation']
    formation = Boncomm(activite, "", com, anneeTarif, 0, nbJoursFormation, 0, 0, 0, "", "", "", 0, "", "", "", "", "",
                        "", "", horsProjet, nbJoursFormation, 0, 0, 0, "", "", "", "", 0)
    ids = request.form.getlist('collabs2')
    for idc in ids:  # Pour tous les collabs sélectionnés dans la création de la formation
        data = db.session.query(Collab).get(idc)
        assoc = AssociationBoncommCollab(joursAllouesBC=nbJoursFormation)
        assoc.collab = data
        formation.collabs.append(assoc)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(formation.id_acti, idc, date.id_date, 0, "client")
            impAtos = Imputation(formation.id_acti, idc, date.id_date, 0, "atos")
            db.session.add(imp)
            db.session.add(impAtos)
    db.session.add(formation)
    db.session.commit()
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/save_autre', methods=['GET', 'POST'])
def save_autre():
    """
    Permet de créer une autre activité.

    Parameters
    - ---------

    Returns
    - ------
    render_template
    """

    activite = request.form['activite3']
    com = request.form['com3']
    anneeTarif = request.form['anneeTarif3']
    nbJoursAutre = request.form['nbjoursautre']
    horsProjet = request.form['horsProjet']
    autre = Boncomm(activite, "", com, anneeTarif, 0, nbJoursAutre, 0, 0, 0, "", "", "", 0, "", "", "", "", "", "", "",
                    horsProjet, 0, 0, 0, nbJoursAutre, "", "", "", "", 0)
    ids = request.form.getlist('collabs3')
    for idc in ids:  # Pour tous les collabs sélectionnés dans la création de l'activité.
        data = db.session.query(Collab).get(idc)
        assoc = AssociationBoncommCollab(joursAllouesBC=nbJoursAutre)
        assoc.collab = data
        autre.collabs.append(assoc)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates.
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(autre.id_acti, idc, date.id_date, 0, "client")
            db.session.add(imp)
            impAtos = Imputation(autre.id_acti, idc, date.id_date, 0, "atos")
            db.session.add(impAtos)
    db.session.add(autre)
    db.session.commit()
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/save_boncomm', methods=['GET', 'POST'])
def save_bonComm():
    """
    Permet de créer un nouveau bon de commande.

    Parameters
    - ---------

    Returns
    - ------
    render_template
    """
    activite = request.form['activiteBC']
    com = request.form['comBC']
    anneeTarif = request.form['anneeTarifBC']
    caAtos = request.form['caAtosBC']
    jourThq = request.form['jourThqBC']
    partGDP = request.form['partGDPBC']
    delais = request.form['delaisBC']
    montantHT = request.form['montantHTBC']
    partEGIS = request.form['partEGISBC']
    num = request.form['numBC']
    poste = request.form['posteBC']
    projet = request.form['projetBC']
    tjm = request.form['tjmBC']
    # Le bon contiendra que les jours de Prod :
    bon = Boncomm(activite, "", com, anneeTarif, caAtos, int(jourThq) - int(partGDP), delais, montantHT, partEGIS,
                  num, poste, projet, tjm, "", "", "", "", "", "", "", "", 0, 0, 0, 0, "", "", "", "", 0)
    # La partie GDP du bon contiendra les jours de GDP
    bonGDP = Boncomm('CP - ' + activite, "", com, anneeTarif, caAtos, partGDP, delais, montantHT, partEGIS, num, poste,
                     projet, tjm, "", "", "", "", "", "", "", "", 0, 0, 0, 0, "", "", "", "", 0)
    ids = request.form.getlist('collabsBC')
    for idc in ids:  # Pour tous les collabs sélectionnés.
        joursAllouesBon = request.form['joursBC' + str(idc)]  # Jours qui lui seront attribués sur ce bon.
        data = db.session.query(Collab).get(idc)
        assoc = AssociationBoncommCollab(joursAllouesBC=joursAllouesBon)
        assoc.collab = data
        assoc.boncomm = bon
        bon.collabs.append(assoc)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates.
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(bon.id_acti, idc, date.id_date, 0, "client")
            db.session.add(imp)
            impAtos = Imputation(bon.id_acti, idc, date.id_date, 0, "atos")
            db.session.add(impAtos)
    # La GDP est gérée par CDE ou AVA :
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    for collaborateur in collGDP:
        joursAllouesBon = request.form[
            'joursGDP' + collaborateur.abreviation()]  # Jours qui lui seront attribués sur ce bon.
        data = db.session.query(Collab).get(collaborateur.id_collab)
        assoc = AssociationBoncommCollab(joursAllouesBC=joursAllouesBon)
        assoc.collab = data
        assoc.boncomm = bonGDP
        bonGDP.collabs.append(assoc)
        # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates.
        dates = db.session.query(Date).all()
        for date in dates:
            imp = Imputation(bonGDP.id_acti, collaborateur.id_collab, date.id_date, 0, "client")
            impAtos = Imputation(bonGDP.id_acti, collaborateur.id_collab, date.id_date, 0, "atos")
            db.session.add(imp)
            db.session.add(impAtos)
    db.session.add(bon)
    db.session.add(bonGDP)
    db.session.commit()
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/modif_boncomm/<idb>', methods=['GET', 'POST'])
def modif_boncomm(idb):
    """
    Permet de modifier les attributs d'une activité.

    Parameters
    - ---------
    idb
        id du bon de commande à modifier.

    Returns
    - ------
    render_template
    """
    activite = request.form['activite']
    com = request.form['com']
    anneeTarif = request.form['anneeTarif']
    caAtos = request.form['caAtos']
    jourThq = request.form['jourThq']
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
    for idc in ids:  # On va modifier les attributions des jours à imputer pour les collabs sélectionnés
        joursAllouesBon = request.form['jours' + str(idc)]
        assoc = db.session.query(AssociationBoncommCollab).filter(AssociationBoncommCollab.collab_id == idc,
                                                                  AssociationBoncommCollab.boncomm_id == idb).all()
        if assoc != []:  # Si le collab imputait déjà sur ce bon
            assoc[0].joursAllouesBC = joursAllouesBon
        else:
            data = db.session.query(Collab).get(idc)
            assoc2 = AssociationBoncommCollab(joursAllouesBC=joursAllouesBon)
            assoc2.collab = data
            assoc2.boncomm = data_to_change
            data_to_change.collabs.append(assoc2)
            # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates
            dates = db.session.query(Date).all()
            for date in dates:
                imp = Imputation(data_to_change.id_acti, idc, date.id_date, 0, "client")
                db.session.add(imp)
                impAtos = Imputation(data_to_change.id_acti, idc, date.id_date, 0, "atos")
                db.session.add(impAtos)
    db.session.commit()
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collaborateur in collaborateurs:
        data_navbar.append([collaborateur.abreviation(), collaborateur])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/modif_activite/<idb>', methods=['GET', 'POST'])
def modif_activite(idb):
    """
    Permet de modifier les attributs d'une activité.

    Parameters
    - ---------
    idb
        id de l'activité à modifier.

    Returns
    - ------
    render_template
    """
    activite = request.form['activite']
    com = request.form['com']
    anneeTarif = request.form['anneeTarif']
    jourThq = request.form['jourThq']
    horsProjet = request.form['horsProjet']
    data_to_change = db.session.query(Boncomm).get(idb)
    if data_to_change.nbJoursFormation == 0:
        if data_to_change.nbJoursAutre != jourThq:
            data_to_change.nbJoursAutre = jourThq
            data_to_change.jourThq = jourThq
    else:
        if data_to_change.nbJoursFormation != jourThq:
            data_to_change.nbJoursFormation = jourThq
            data_to_change.jourThq = jourThq
    if activite != "":
        data_to_change.activite = activite
    if com != "":
        data_to_change.com = com
    if horsProjet != "":
        data_to_change.horsProjet = horsProjet
    if anneeTarif != data_to_change.anneeTarif:
        data_to_change.anneeTarif = anneeTarif
    ids = request.form.getlist('collabs')
    for idc in ids:  # On va modifier les attributions des jours à imputer pour les collabs sélectionnés
        assoc = db.session.query(AssociationBoncommCollab).filter(AssociationBoncommCollab.collab_id == idc,
                                                                  AssociationBoncommCollab.boncomm_id == idb).all()
        if assoc != []:  # Si le collab imputait déjà sur ce bon
            assoc[0].joursAllouesBC = jourThq
        else:
            data = db.session.query(Collab).get(idc)
            assoc2 = AssociationBoncommCollab(joursAllouesBC=jourThq)
            assoc2.collab = data
            assoc2.boncomm = data_to_change
            data_to_change.collabs.append(assoc2)
            # On initialise une imputation nulle pour chaque collab sur le bon, pour toutes les dates
            dates = db.session.query(Date).all()
            for date in dates:
                imp = Imputation(data_to_change.id_acti, idc, date.id_date, 0, "client")
                db.session.add(imp)
                impAtos = Imputation(data_to_change.id_acti, idc, date.id_date, 0, "atos")
                db.session.add(impAtos)
    db.session.commit()
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collaborateur in collaborateurs:
        data_navbar.append([collaborateur.abreviation(), collaborateur])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/modif_etat/<idb>', methods=['GET', 'POST'])
def modif_etat(idb):
    """
    Permet de modifier l'état de l'activité.

        Parameters
    - ---------
    idb
        id de l'activité à modifier.
    Returns
    - ------
    render_template
    """
    etat = request.form['etat']
    boncomm = db.session.query(Boncomm).get(idb)
    if boncomm.caAtos != 0:  # Si c'est un BC, on modifie son état et celui de son activité GdP
        if boncomm.activite[0:4] != "CP -":
            boncomm.etat = etat
            boncommGDP = db.session.query(Boncomm).get(str(int(idb) + 1))
            boncommGDP.etat = etat
    elif boncomm.activite[0:4] != "CP -":  # Le cas des GdP est traité avec sa part production
        boncomm.etat = etat
    db.session.commit()
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


@app.route('/deleteactivite/<idb>')
def delete_activite(idb):
    """
    Permet de supprimer une activité.

    Parameters
    - ---------
    idb
        id du BC à supprimer.
    Returns
    - ------
    """
    activite_to_delete = db.session.query(Boncomm).get(idb)
    # On supprime toutes les imputations et associations de cette activité.
    if activite_to_delete.caAtos != 0:  # Si c'est un BC, on le supprime lui et sa part GdP
        if activite_to_delete.activite[0:4] != "CP -":  # La part GdP est traitée par la part production
            actiGDP_to_delete = db.session.query(Boncomm).get(
                str(int(idb) + 1))  # Id suivant est celui de la part GDP
            imputations = db.session.query(Imputation).filter(Imputation.acti_id == idb).all()
            imputationsGDP = db.session.query(Imputation).filter(Imputation.acti_id == str(int(idb) + 1)).all()
            for imputation in imputations:
                db.session.delete(imputation)
            for imputationGDP in imputationsGDP:
                db.session.delete(imputationGDP)
            associations = db.session.query(AssociationBoncommCollab).filter(
                AssociationBoncommCollab.boncomm_id == idb).all()
            associationsGDP = db.session.query(AssociationBoncommCollab).filter(
                AssociationBoncommCollab.boncomm_id == str(int(idb) + 1)).all()
            for assoc in associations:
                db.session.delete(assoc)
            for assocGDP in associationsGDP:
                db.session.delete(assocGDP)
            db.session.delete(activite_to_delete)
            db.session.delete(actiGDP_to_delete)
    elif activite_to_delete.activite[0:4] != "CP -":  # Le cas des GdP est traité avec sa part production
        imputations = db.session.query(Imputation).filter(Imputation.acti_id == idb).all()
        for imputation in imputations:  # On supprime toutes les imputations
            db.session.delete(imputation)
        associations = db.session.query(AssociationBoncommCollab).filter(
            AssociationBoncommCollab.boncomm_id == idb).all()
        for assoc in associations:  # On supprime toutes les associations
            db.session.delete(assoc)
        db.session.delete(activite_to_delete)
    db.session.commit()
    ava = db.session.query(Collab).filter(Collab.nom == "Vieira").all()[0]
    cde = db.session.query(Collab).filter(Collab.nom == "Damotte").all()[0]
    collGDP = [ava, cde]
    boncomms = db.session.query(Boncomm).all()
    data_boncomm = []
    data_reste = []
    for i in range(len(boncomms)):
        boncomm = boncomms[i]
        if boncomm.activite[0:4] != "CP -":
            if boncomm.caAtos != 0:  # c'est un BC, et non pas une formation ou autre
                collabs = boncomm.collabs
                # Dans l'ordre, si c'est un BC, il y a forcément ensuite sa partie GDP
                collabsGDP = boncomms[i + 1].collabs
                data_boncomm.append([boncomm, collabs, boncomms[i + 1], collabsGDP])
            elif boncomm.nbCongesTot == 0:  # Autres activités, sauf les congés
                collabs = boncomm.collabs
                data_reste.append([boncomm, collabs])
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('activite.html', data_boncomm=data_boncomm, data_reste=data_reste, collabs=collabs,
                           data_navbar=data_navbar, mois=mois, annee=annee)


""" - -- Partie Date: voir, enregistrer - --"""


@app.route('/see_data_date')
def see_data_date():
    """
    Amène à la page HTML montrant l'ensemble des dates.

    Parameters
    - ---------

    Returns
    - ------
    render_template
    """
    data3 = db.session.query(Date).all()
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('date.html', data3=data3, data_navbar=data_navbar, mois=mois, annee=annee)


""" - -- Partie Imputation: enregistrer, voir - --"""


@app.route('/save_imputation/<idc>/<annee>/<mois>', methods=['GET', 'POST'])
def save_imputation(idc, annee, mois):
    """
    Permet de créer une nouvelle imputation.

    Parameters
    - ---------
    idc
        id du collaborateur associé
    annee
        annee sur laquelle on va enregistrer les imputations.
    mois
        mois sur lequel on va enregistrer les imputations

    Returns
    - ------
    render_template
    """
    columns = columnMois(mois, annee)
    collab = db.session.query(Collab).get(idc)
    assos = collab.boncomms
    boncomms = []
    for i in range(len(assos)):  # On sépare les congés du reste.
        boncomm = assos[i].boncomm
        if boncomm.nbCongesTot == 0 and assos[i].joursAllouesBC != 0 and boncomm.etat == "":
            boncomms.append(boncomm)
        elif boncomm.nbCongesTot != 0:
            conges = boncomm
    # Principe de construction identique à la méthode see_archive
    data_boncomms = []  # liste qui contiendra pour chaque bon de commande l'imputation sur chaque semaine
    calcJoursDispo = True  # Variable pour calculer une seule fois les jours dispos par semaine dans la boucle des
    # dates.
    for i in range(len(boncomms)):
        imputBC = []
        for column in columns:
            numSemaine = column[0]
            jours = request.form[str(boncomms[i].id_acti) + "/" + str(numSemaine)]
            dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
            date_access = []  # Toutes les dates de la semaine en cours où l'on peut imputer
            for date in dates:
                if date.numSemaine() == numSemaine:
                    date_access.append(date)
            for jour in date_access:  # On supprime les imputations sur ces dates pour récréer en fonction du nombre
                # de jours nécessaires
                if calcJoursDispo:  # On calcule une seule fois les jours dispo dans la semaine par rapport aux
                    # congés posés
                    jourConges = db.session.query(Imputation).filter(
                        Imputation.acti_id == conges.id_acti,
                        Imputation.collab_id == idc,
                        Imputation.date_id == jour.id_date, Imputation.type == "client").all()[0].joursAllouesTache
                    if jourConges != 0:  # Si un congés est posé, on enlève 1 ou 0.5 jour de disponible
                        column[1] -= jourConges
                imps = db.session.query(Imputation).filter(Imputation.collab_id == idc,
                                                           Imputation.date_id == jour.id_date,
                                                           Imputation.acti_id == boncomms[i].id_acti).all()
                for imp in imps:
                    db.session.delete(imp)
            for k in range(int(jours[0])):  # On prend la partie entière des jours posés, et on impute tant de jours
                date = date_access[k]
                imp = Imputation(boncomms[i].id_acti, idc, date.id_date, 1, "client")
                impAtos = Imputation(boncomms[i].id_acti, idc, date.id_date, 1, "atos")
                db.session.add(imp)
                db.session.add(impAtos)

            if len(jours) > 1:  # Pour les float du type 2.0, 3.5, etc ...
                if jours[1] == "." or jours[1] == ",":  # On est bien sur un chiffre a demi-journée
                    if jours[2] == "5":  # Si une demi-journée est imputée
                        date = date_access[int(jours[0])]
                        imp = Imputation(boncomms[i].id_acti, idc, date.id_date, 0.5, "client")
                        impAtos = Imputation(boncomms[i].id_acti, idc, date.id_date, 0.5, "atos")
                        db.session.add(imp)
                        db.session.add(impAtos)
                        for j in range(len(date_access) - int(jours[0])):  # Sinon on met le reste à 0
                            date = date_access[int(jours[0]) + j]
                            imp = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "client")
                            impAtos = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "atos")
                            db.session.add(imp)
                            db.session.add(impAtos)
                    else:
                        for j in range(len(date_access) - int(
                                jours[
                                    0])):  # Pour les jours restants, imputations avec le nombre de jours alloués = 0
                            date = date_access[int(jours[0]) + j]
                            imp = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "client")
                            impAtos = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "atos")
                            db.session.add(imp)
                            db.session.add(impAtos)
                else:
                    for k in range(
                            int(jours[
                                    1])):  # On prend la partie entière des jours posés, et on impute tant de jours
                        date = date_access[k]
                        imp = Imputation(boncomms[i].id_acti, idc, date.id_date, 1, "client")
                        db.session.add(imp)
                        impAtos = Imputation(boncomms[i].id_acti, idc, date.id_date, 1, "atos")
                        db.session.add(impAtos)
                    for j in range(len(date_access) - int(
                            jours[1])):  # Pour les jours restants, imputations avec le nombre de jours alloués = 0
                        date = date_access[int(jours[1]) + j]
                        imp = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "client")
                        db.session.add(imp)
                        impAtos = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "atos")
                        db.session.add(impAtos)
            else:  # Pour les formats entiers type 1, 2, etc...
                for j in range(len(date_access) - int(
                        jours[0])):  # Pour les jours restants, imputations avec le nombre de jours alloués = 0
                    date = date_access[int(jours[0]) + j]
                    imp = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "client")
                    db.session.add(imp)
                    impAtos = Imputation(boncomms[i].id_acti, idc, date.id_date, 0, "atos")
                    db.session.add(impAtos)

            imputBC.append([numSemaine, jours])
        imputations = db.session.query(Imputation).filter(Imputation.acti_id == boncomms[i].id_acti,
                                                          Imputation.collab_id == idc,
                                                          Imputation.joursAllouesTache != 0,
                                                          Imputation.type == "client").all()
        dejaConso = 0
        for imputation in imputations:
            dejaConso += imputation.joursAllouesTache
        assoCollabBC = db.session.query(AssociationBoncommCollab).filter(
            AssociationBoncommCollab.collab_id == idc,
            AssociationBoncommCollab.boncomm_id == boncomms[i].id_acti).all()
        joursAlloues = assoCollabBC[0].joursAllouesBC
        # Données pour ce qui est déjàa consommés et reste à faire :
        data_boncomms.append([boncomms[i], imputBC, float(joursAlloues), float(joursAlloues) - float(dejaConso)])
        db.session.commit()
        calcJoursDispo = False  # Une fois calculés, pas besoin de recalculer les jours dispos par semaine.
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collaborateur in collaborateurs:
        data_navbar.append([collaborateur.abreviation(), collaborateur])
    dateNow = str(datetime.now())
    mois_courant = int(dateNow[5:7])
    annee_courant = int(dateNow[:4])
    moisStr = stringMois(mois)
    return render_template('imputcollab.html', boncomms=data_boncomms, columns=columns, collab=collab, annee=annee,
                           mois=mois, moisStr=moisStr, data_navbar=data_navbar, mois_courant=mois_courant,
                           annee_courant=annee_courant)


@app.route('/see_imput_collab/<idc>/<annee>/<mois>')
def see_imput_collab(idc, annee, mois):
    """
    Permet de voir les imputations d'un collaborateur.

    Parameters
    - ---------
    idc
        id du collaborateur
    annee
        annee sélectionnée
    mois
        mois sélectionné
    Returns
    - ------
    render_template
    """
    collab = db.session.query(Collab).get(idc)
    assos = collab.boncomms
    boncomms = []
    for i in range(len(assos)):  # On sépare les congés du reste
        boncomm = assos[i].boncomm
        if boncomm.nbCongesTot == 0 and assos[i].joursAllouesBC != 0 and boncomm.etat == "":
            boncomms.append(boncomm)
        elif boncomm.nbCongesTot != 0:
            conges = boncomm
    columns = columnMois(mois,
                         annee)  # On calcule les numéros de semaines et nombres de jours dispo pour le mois en cours
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    data_boncomms = []
    calcJoursDispo = True
    for i in range(len(boncomms)):
        imput = []
        for column in columns:
            numSemaine = column[0]
            date_access = []
            jourImpute = 0
            for date in dates:
                if date.numSemaine() == numSemaine:
                    date_access.append(date)
            for jour in date_access:  # Que les jours de la semaine en cours de la boucle "for column"
                if calcJoursDispo:  # On calcule une seule fois les jours dispo dans la semaine par rapport aux
                    # congés posés
                    jour_conges = db.session.query(Imputation).filter(
                        Imputation.acti_id == conges.id_acti,
                        Imputation.collab_id == idc,
                        Imputation.date_id == jour.id_date, Imputation.type == "client").all()[0].joursAllouesTache
                    if jour_conges != 0:
                        column[1] -= jour_conges  # On enlève un jour de dispo si un congés est posé cette semaine
                imputation = db.session.query(Imputation).filter(
                    Imputation.acti_id == boncomms[i].id_acti,
                    Imputation.collab_id == idc,
                    Imputation.date_id == jour.id_date
                ).all()
                if imputation[0].joursAllouesTache != 0:
                    jourImpute += imputation[
                        0].joursAllouesTache  # En fonction du nb d'imputation avec le nombre de jours alloués != 0,
                    # on calcule le nb de jours imputés sur la semaine
            imput.append([numSemaine, float(jourImpute)])
        calcJoursDispo = False
        assoCollabBC = db.session.query(AssociationBoncommCollab).filter(
            AssociationBoncommCollab.collab_id == idc,
            AssociationBoncommCollab.boncomm_id == boncomms[i].id_acti).all()
        imputations = db.session.query(Imputation).filter(Imputation.acti_id == boncomms[i].id_acti,
                                                          Imputation.collab_id == idc,
                                                          Imputation.joursAllouesTache != 0,
                                                          Imputation.type == "client").all()
        dejaConso = 0
        for imputation in imputations:
            dejaConso += imputation.joursAllouesTache
        joursAlloues = assoCollabBC[0].joursAllouesBC
        data_boncomms.append([boncomms[i], imput, float(joursAlloues), float(joursAlloues) - float(dejaConso)])

    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collaborateur in collaborateurs:
        data_navbar.append([collaborateur.abreviation(), collaborateur])
    dateNow = str(datetime.now())
    mois_courant = int(dateNow[5:7])
    annee_courant = int(dateNow[:4])
    moisStr = stringMois(mois)
    return render_template('imputcollab.html', boncomms=data_boncomms, collab=collab, columns=columns,
                           annee=annee, mois=mois, moisStr=moisStr, data_navbar=data_navbar,
                           mois_courant=mois_courant,
                           annee_courant=annee_courant)


@app.route('/see_imput_global')
def see_imput_global():
    """
    Permet de voir les imputations globales des activités.

    Parameters
    - ---------

    Returns
    - ------
    render_template
    """
    collabs = db.session.query(Collab).filter(Collab.access != 3).all()
    boncomms = []
    # Bons de commande qui ne sont pas finis.
    bons = db.session.query(Boncomm).filter(Boncomm.nbJoursFormation == 0, Boncomm.nbCongesTot == 0,
                                            Boncomm.nbJoursAutre == 0, Boncomm.etat == "").all()
    bonsGDP = []
    for bon in bons:  # On sépare les parts de GdP
        if bon.activite[0:4] == "CP -":
            bonsGDP.append(bon)
            bons.remove(bon)
    data_bon = []
    data_bonGDP = []
    for i in range(len(bons)):
        boncomms.append([i, bons[i], bonsGDP[i]])
        data_ligne = []
        data_ligneGDP = []
        for collab in collabs:
            # Calcul pour les bons hors Gdp
            asso = db.session.query(AssociationBoncommCollab).filter(
                AssociationBoncommCollab.boncomm_id == bons[i].id_acti,
                AssociationBoncommCollab.collab_id == collab.id_collab).all()
            if asso != []:
                joursAllouesCollab = asso[0].joursAllouesBC
                imputations = db.session.query(Imputation).filter(Imputation.acti_id == bons[i].id_acti,
                                                                  Imputation.collab_id == collab.id_collab,
                                                                  Imputation.joursAllouesTache != 0,
                                                                  Imputation.type == "client").all()
                joursConso = 0
                for imputation in imputations:
                    joursConso += imputation.joursAllouesTache  # jours consommés par le collab sur le bon
                raf = joursAllouesCollab - joursConso
                data_ligne.append([joursAllouesCollab, joursConso, raf])
            else:
                data_ligne.append(["", "", ""])  # Ligne vide si le collab n'impute pas sur cette activité

            # Calcul pour les bons de Gdp
            assoGDP = db.session.query(AssociationBoncommCollab).filter(
                AssociationBoncommCollab.boncomm_id == bonsGDP[i].id_acti,
                AssociationBoncommCollab.collab_id == collab.id_collab).all()
            if assoGDP != []:
                joursAllouesCollab = assoGDP[0].joursAllouesBC
                imputsGDP = db.session.query(Imputation).filter(Imputation.acti_id == bonsGDP[i].id_acti,
                                                                Imputation.collab_id == collab.id_collab,
                                                                Imputation.joursAllouesTache != 0,
                                                                Imputation.type == "client").all()
                joursConso = 0
                for imputGDP in imputsGDP:
                    joursConso += imputGDP.joursAllouesTache
                raf = joursAllouesCollab - joursConso
                data_ligneGDP.append([joursAllouesCollab, joursConso, raf])
            else:
                data_ligneGDP.append(["", "", ""])  # Ligne vide si le collab n'impute pas sur cette activité
        data_bon.append(data_ligne)
        data_bonGDP.append(data_ligneGDP)
    valeursBoncomms = []
    valeursBoncommsGDP = []
    for j in range(len(boncomms)):  # On calcule pour chaque activité les valeurs nécessaires dans le tableau : raf,
        # conso, etc...
        valeurs = valeursGlobales(boncomms[j][1])
        valeursGDP = valeursGlobales(boncomms[j][2])
        valeursBoncomms.append(valeurs)
        valeursBoncommsGDP.append(valeursGDP)
    nbCollab = len(collabs)
    collaborateurs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    data_navbar = []
    for collab in collaborateurs:
        data_navbar.append([collab.abreviation(), collab])
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    return render_template('imputglobal.html', collabs=collabs, boncomms=boncomms, nbCollab=nbCollab,
                           data_bonGDP=data_bonGDP, data_bon=data_bon, valeursBoncomms=valeursBoncomms,
                           valeursBoncommsGDP=valeursBoncommsGDP, data_navbar=data_navbar, mois=mois, annee=annee)
