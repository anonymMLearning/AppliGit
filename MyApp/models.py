from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, Column

from MyApp.views import app

import datetime

from jours_feries_france import JoursFeries

# Create database connection object
db = SQLAlchemy(app)

"""assoBoncommCollab = db.Table('assoBoncommCollab',
                             db.Column('boncomm_id', db.Integer, db.ForeignKey('collab.id_collab'), primary_key=True),
                             db.Column('collab_id', db.Integer, db.ForeignKey('boncomm.id_acti'), primary_key=True)
                             )
"""


class AssociationBoncommCollab(db.Model):
    boncomm_id = db.Column('boncomm_id', db.Integer, db.ForeignKey('boncomm.id_acti'), primary_key=True)
    collab_id = db.Column('collab_id', db.Integer, db.ForeignKey('collab.id_collab'), primary_key=True)
    joursAllouesBC = db.Column(db.Integer, nullable=False)
    collab = db.relationship("Collab", back_populates="boncomms")
    boncomm = db.relationship("Boncomm", back_populates="collabs")


class Collab(db.Model):
    """
            Réprésente un collaborateur de l'équipe.

            ...

            Attributs
            ----------
            id_collab : int
                id du collaborateur, clé primaire.
            nom : str
                nom du collaborateur.
            prenom : str
                prénom du collaborateur.
            access : int
                niveau d'accès du collaborateur.
            imputations : list d'Imputation
               ensemble des imputations associées au collaborateur, venant de l'association entre la classe Collab et Imputation.
            boncomms : list de Boncomm
                ensemble des bons de commande associés au collaborateur, venant de l'association plusieurs-à-plusieurs entre Collab et Boncomm.

            Méthodes
            -------
            __init__(self, nom, prenom, access)
                constructeur de la classe
            """
    id_collab = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    access = db.Column(db.Integer, nullable=False)
    imputations = db.relationship('Imputation', backref='collab', uselist=False)
    boncomms = db.relationship('AssociationBoncommCollab', back_populates="collab")

    def __init__(self, nom, prenom, access):
        self.nom = nom
        self.prenom = prenom
        self.access = access


class Imputation(db.Model):
    """
            Réprésente une Imputation sur une date et un bon de commande par un collaborateur.

            ...

            Attributs
            ----------
            id_imp : int
                id de l'imputation, clé primaire.
            acti_id : int
                id de l'activité liée, clé étrangère de la table Boncomm.
            collab_id : int
                id du collaborateur liée, clé étrangère de la table Collab.
            date_id : int
                id de la date liée, clé étrangère de la table Date.
            joursAllouesTache : float
                nombre de jours alloués sur cette activité pour cette date, par ce collaborateur.

            Méthodes
            -------
            __init__(self, acti_id, collab_id, date_id, joursAllouesTache)
                constructeur de la classe
            """

    id_imp = db.Column(db.Integer, primary_key=True)
    acti_id = db.Column(db.Integer, db.ForeignKey('boncomm.id_acti'), nullable=False)
    collab_id = db.Column(db.Integer, db.ForeignKey('collab.id_collab'), nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id_date'), nullable=False)
    joursAllouesTache = db.Column(db.Float, nullable=False)

    def __init__(self, acti_id, collab_id, date_id, joursAllouesTache):
        self.acti_id = acti_id
        self.collab_id = collab_id
        self.date_id = date_id
        self.joursAllouesTache = joursAllouesTache

    def get_jours(self):
        imp = db.session.query(Imputation).filter(Imputation.acti_id == self.acti_id,
                                                  Imputation.collab_id == self.collab_id,
                                                  Imputation.date_id == self.date_id).all()
        jours = imp[0].joursAllouesTache
        return jours


class Boncomm(db.Model):
    """
            Réprésente un bon de commande.

            ...

            Attributs
            ----------
            id_acti : int
                id du bon de commande, clé primaire.
            activite : str
                description du bon de commande.
            com : str
                Commentaire, si nécessaire, sur le bon de commande.
            anneeTarif : float
                année tarifaire du bon de commande.
            caAtos : float
                chiffre d'affaire du bon de commande.
            delais : float
                délais de réalisation du bon de commande.
            montantHT : float
                montant Hors Taxes du bon de commande.
            partEGIS : float
                part d'EGIS sur le chiffre d'affaire du bon de commande.
            num : str
                numéro du bon de commande.
            num : poste
                poste du bon de commande.
            projet : str
                projet du bon de commande.
            tjm : float
                taux journalier moyen appliqué à ce commande.
            imputations : list d'Imputation
                ensemble des imputations associées au bon de commande, venant de l'association entre la classe Imputation et Boncomm.
            collabs ; list de Collab
                ensemble des collaborateurs qui imputent sur ce bon de commande, venant de l'association plusieurs_à_plusieurs entre Boncomm et Collab.

            Méthodes
            -------
            __init__(self, activite, com, anneeTarif, caAtos, jourThq, delais, montantHT, partEGIS, num, poste, projet, tjm)
               constructeur de la classe
            """
    id_acti = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activite = db.Column(db.String(100))
    com = db.Column(db.String(100))
    anneeTarif = db.Column(db.Integer)
    caAtos = db.Column(db.Float)
    jourThq = db.Column(db.Float)
    delais = db.Column(db.Float)
    montantHT = db.Column(db.Float)
    partEGIS = db.Column(db.Float)
    num = db.Column(db.String(30))
    poste = db.Column(db.String(100))
    projet = db.Column(db.String(30))
    tjm = db.Column(db.Float)
    horsProjet = db.Column(db.String(10))
    nbJoursFormation = db.Column(db.Float)
    nbCongesTot = db.Column(db.Float)
    nbCongesPose = db.Column(db.Float)
    nbJoursAutre = db.Column(db.Float)
    imputations = db.relationship('Imputation', backref='boncomm', uselist=False)
    collabs = db.relationship('AssociationBoncommCollab', back_populates="boncomm")

    def __init__(self, activite, com, anneeTarif, caAtos, jourThq, delais, montantHT, partEGIS, num, poste,
                 projet, tjm, horsProjet, nbJoursFormation, nbCongesTot, nbCongesPose, nbJoursAutre):
        self.activite = activite
        self.com = com
        self.anneeTarif = anneeTarif
        self.caAtos = caAtos
        self.jourThq = jourThq
        self.delais = delais
        self.montantHT = montantHT
        self.partEGIS = partEGIS
        self.num = num
        self.poste = poste
        self.projet = projet
        self.tjm = tjm
        self.horsProjet = horsProjet
        self.nbJoursFormation = nbJoursFormation
        self.nbCongesTot = nbCongesTot
        self.nbCongesPose = nbCongesPose
        self.nbJoursAutre = nbJoursAutre


class Date(db.Model):
    """
            Réprésente une date.

            ...

            Attributs
            ----------
            id_date : int
                id de la date, clé primaire.
            jour : int
                jour de la date.
            mois : int
                mois de la date.
            annee : int
                annee de la date.
            imputations : list d'Imputation
                ensemble des imputations associées a la date, venant de l'association entre la classe Date et Imputation.

            Méthodes
            -------
            __init__(self, jour, mois, annee)
                constructeur de la classe.
            transfoDate(self)
                transforme la date au format jj-mm-aaa.
            numSemaine(self)
                renvoie le numéro de la semaine associé à ce jour.
            estFerie(self)
                indique par un booléen en sortie si le jour est férié ou non.
            """
    id_date = db.Column(db.Integer, primary_key=True)
    jour = db.Column(db.Integer, nullable=False)
    mois = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    imputations = db.relationship('Imputation', backref='date', uselist=False)

    def __init__(self, jour, mois, annee):
        self.jour = jour
        self.mois = mois
        self.annee = annee

    def transfoDate(self):
        date = datetime.date(self.annee, self.mois, self.jour)
        return date

    def numSemaine(self):
        date = self.transfoDate()
        return date.isocalendar()[1]

    def estFerie(self):
        date = self.transfoDate()
        res = JoursFeries.for_year(self.annee)
        keys = res.keys()
        for key in keys:
            if res.get(key) == date:
                return True
        return False


def columnMois(mois, annee):
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    columns = []
    numSem = dates[0].numSemaine()
    joursDispo = 0
    for date in dates:
        date_format = date.transfoDate().weekday()
        if date.numSemaine() == numSem:
            if date_format != 5 and date_format != 6:
                if not date.estFerie():
                    joursDispo += 1
        else:
            columns.append([numSem, joursDispo])
            numSem = date.numSemaine()
            joursDispo = 0
            if date_format != 5 and date_format != 6:
                if not date.estFerie():
                    joursDispo += 1
    columns.append([numSem, joursDispo])
    return columns


def valeursGlobales(boncomm):
    joursConsommes = 0
    assoCollabs = boncomm.collabs
    collabs = []
    for asso in assoCollabs:
        collabs.append(asso.collab)
    consoCollabs = []
    for collab in collabs:
        joursConsommesCollab = 0
        imputations = db.session.query(Imputation).filter(Imputation.acti_id == boncomm.id_acti,
                                                          Imputation.collab_id == collab.id_collab,
                                                          Imputation.joursAllouesTache == 1).all()
        joursConsommesCollab += len(imputations)
        consoCollabs.append(joursConsommesCollab)
        joursConsommes += joursConsommesCollab
    raf = boncomm.jourThq - joursConsommes
    avancement = joursConsommes / boncomm.jourThq * 100
    ecart = boncomm.jourThq - (raf + joursConsommes)
    etat = ""
    if joursConsommes == boncomm.jourThq:
        etat = "TE"
    elif joursConsommes < boncomm.jourThq:
        etat = ""
    else:
        etat = "HB"
    return [consoCollabs, etat, avancement, raf, joursConsommes, ecart]


db.create_all()
