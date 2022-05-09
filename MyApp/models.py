from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, Column

from MyApp.views import app

import datetime
from jours_feries_france import JoursFeries

# Create database connection object
db = SQLAlchemy(app)


class AssociationBoncommCollab(db.Model):
    """
            Réprésente l'association entre un collab et une activité.

            ...

            Attributs
            ----------
            collab_id : int
                id du collaborateur, clé primaire.
            boncomm_id : int
                id de l'activité, clé primaire.
            joursAllouesBC : float
                nombre de jours alloués au collab pour cette activité .
            collab :
                lien d'association au collaborateur.
            boncomm :
                lien d'association à l'activité.
    """
    boncomm_id = db.Column('boncomm_id', db.Integer, db.ForeignKey('boncomm.id_acti'), primary_key=True)
    collab_id = db.Column('collab_id', db.Integer, db.ForeignKey('collab.id_collab'), primary_key=True)
    joursAllouesBC = db.Column(db.Float, nullable=False)
    collab = db.relationship("Collab", back_populates="boncomms")
    boncomm = db.relationship("Boncomm", back_populates="collabs")


class AssoCollabFonction(db.Model):
    """
            Réprésente l'association entre une fonction et un collaborateur.

            ...

            Attributs
            ----------
            collab_id : int
                id du collaborateur, clé primaire.
            fonction_id : int
                id de la fonction, clé primaire.
            affectation : float
                pourcentage, représentant la part du temps de travail du collaborateur sur cette fonction.
            collab :
                lien d'association au collaborateur.
            fonction :
                lien d'association à la fonction.
    """
    collab_id = db.Column('collab_id', db.Integer, db.ForeignKey('collab.id_collab'), primary_key=True)
    fonction_id = db.Column('fonction_id', db.Integer, db.ForeignKey('fonction.id_fonction'), primary_key=True)
    affectation = db.Column(db.Float, nullable=False)
    collab = db.relationship("Collab", back_populates="fonctions")
    fonction = db.relationship("Fonction", back_populates="collabs")


class AssoUoBoncomm(db.Model):
    """
        Réprésente l'association entre une UO et un bon de commande.

        ...

        Attributs
        ----------
        uo_id : int
            id de l'UO, clé primaire.
        boncomm_id : int
            id du bon de commande, clé primaire.
        facteur : int
            facteur multiplicatif de l'UO dans le BC.
        uo :
            lien d'association à l'uo.
        boncomm :
            lien d'association à la fonction.
    """
    uo_id = db.Column('uo_id', db.Integer, db.ForeignKey('UO.id_uo'), primary_key=True)
    boncomm_id = db.Column('boncomm_id', db.Integer, db.ForeignKey('boncomm.id_acti'), primary_key=True)
    facteur = db.Column(db.Integer, nullable=False)
    uo = db.relationship("UO", back_populates="boncomms")
    boncomm = db.relationship("Boncomm", back_populates="uos")


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
            entreprise : str
                entreprise du collaborateur.
            imputations : list d'Imputation
               ensemble des imputations associées au collaborateur, venant de l'association entre la classe Collab et Imputation.
            boncomms : list de Boncomm
                ensemble des bons de commande associés au collaborateur, venant de l'association plusieurs-à-plusieurs entre Collab et Boncomm.

            Méthodes
            -------
            __init__(self, nom, prenom, access, entreprise)
                constructeur de la classe

            abreviation(self)
                permet d'avoir l'abréviation du nom et prénom du collaborateur
            """
    id_collab = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(30), nullable=False)
    prenom = db.Column(db.String(30), nullable=False)
    access = db.Column(db.Integer, nullable=False)
    entreprise = db.Column(db.String(30), nullable=False)
    imputations = db.relationship('Imputation', backref='collab', uselist=False)
    boncomms = db.relationship('AssociationBoncommCollab', back_populates="collab")
    fonctions = db.relationship('AssoCollabFonction', back_populates="collab")

    def __init__(self, nom, prenom, access, entreprise):
        self.nom = nom
        self.prenom = prenom
        self.access = access
        self.entreprise = entreprise

    def abreviation(self):
        prenom = self.prenom[0]
        nomDebut = self.nom[0]
        nomFin = self.nom[-1]
        abrev = (prenom + nomDebut + nomFin).upper()
        return abrev


class Fonction(db.Model):
    """
        Réprésente une fonction que peut remplir un collaborateur.

        ...

        Attributs
        ----------
        id_fonction : int
            id de la fonction, clé primaire.
        nom : str
            nom de la fonction.
        tjm : float
            tjm de la fonction.
        collabs : list de Collab
            ensemble des colaborateurs assurant cette fonction, venant de l'association plusieurs-à-plusieurs entre Collab et Fonction.

        Méthodes
        -------
        __init__(self, nom, tjm)
            constructeur de la classe
    """
    id_fonction = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    tjm = db.Column(db.Float, nullable=False)
    collabs = db.relationship('AssoCollabFonction', back_populates="fonction")

    def __init__(self, nom, tjm):
        self.nom = nom
        self.tjm = tjm


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
            get_jours(self)
                méthode pour récupérer nombre de jours alloués a la tache pour ce collab, cette activité à cette date.
                (équivalent à .joursAllouesTache)
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
            etat : str
                état, terminé ou en cours, du bon de commande.
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
            poste : str
                poste du bon de commande.
            projet : str
                projet du bon de commande.
            tjm : float
                taux journalier moyen appliqué à ce commande.
            imputations : list d'Imputation
                ensemble des imputations associées au bon de commande, venant de l'association entre la classe Imputation et Boncomm.
            collabs : list de Collab
                ensemble des collaborateurs qui imputent sur ce bon de commande, venant de l'association plusieurs_à_plusieurs entre Boncomm et Collab.
            uos : list d'UO
                ensemble des UOs liées à ce BC, venant de l'association plusieurs_à_plusieurs entre Boncomm et UO.

            Méthodes
            -------
            __init__(self, activite, com, anneeTarif, caAtos, jourThq, delais, montantHT, partEGIS, num, poste, projet, tjm)
               constructeur de la classe
            """
    id_acti = db.Column(db.Integer, primary_key=True, autoincrement=True)
    activite = db.Column(db.String(20))
    etat = db.Column(db.String(100))
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
    notification = db.Column(db.String(30))
    facturation = db.Column(db.String(30))
    prodGdpOuFd = db.Column(db.String(30))
    dateDebut = db.Column(db.String(30))
    dateFinPrev = db.Column(db.String(30))
    dateNotif = db.Column(db.String(30))
    dateFinOp = db.Column(db.String(30))
    horsProjet = db.Column(db.String(10))
    nbJoursFormation = db.Column(db.Float)
    nbCongesTot = db.Column(db.Float)
    nbCongesPose = db.Column(db.Float)
    nbJoursAutre = db.Column(db.Float)
    imputations = db.relationship('Imputation', backref='boncomm', uselist=False)
    collabs = db.relationship('AssociationBoncommCollab', back_populates="boncomm")
    uos = db.relationship('AssoUoBoncomm', back_populates="boncomm")

    def __init__(self, activite, etat, com, anneeTarif, caAtos, jourThq, delais, montantHT, partEGIS, num, poste,
                 projet, tjm, notification, facturation, prodGdpOuFd, dateDebut, dateFinPrev, dateNotif, dateFinOp,
                 horsProjet, nbJoursFormation, nbCongesTot, nbCongesPose, nbJoursAutre):
        self.activite = activite
        self.etat = etat
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
        self.notification = notification
        self.facturation = facturation
        self.prodGdpOuFd = prodGdpOuFd
        self.dateDebut = dateDebut
        self.dateFinPrev = dateFinPrev
        self.dateNotif = dateNotif
        self.dateFinOp = dateFinOp
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
            pourcentAn : float
                pourcentage sur l'année pour calculs des prix UO et TJM.
            imputations : list d'Imputation
                ensemble des imputations associées a la date, venant de l'association entre la classe Date et Imputation.

            Méthodes
            -------
            __init__(self, jour, mois, annee, pourcentAn)
                constructeur de la classe.
            transfoDate(self)
                transforme la date au format jj-mm-aaa.
            numSemaine(self)
                renvoie le numéro de la semaine associé à ce jour.
            estFerie(self)
                indique par un booléen en sortie si le jour est férié ou non.
            jourSemaine(self)
                indique à quel jour de la semaine la date correspond.
            """
    id_date = db.Column(db.Integer, primary_key=True)
    jour = db.Column(db.Integer, nullable=False)
    mois = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    pourcentAn = db.Column(db.Float, nullable=False)
    imputations = db.relationship('Imputation', backref='date', uselist=False)

    def __init__(self, jour, mois, annee, pourcentAn):
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.pourcentAn = pourcentAn

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

    def jourSemaine(self):
        return self.transfoDate().weekday()


class UO(db.Model):
    """
            Réprésente une UO.

            ...

            Attributs
            ----------
            id_uo : int
                id de l'uo, clé primaire.
            charges : float
                charges de l'uo.
            num : str
                numéro de l'uo.
            description : str
                description de l'uo.
            prix : float
                prix de base de l'uo sur l'année de sa création.
            boncomms : list
                liste de bon de commande venant de l'association AssoUoBoncomm.

            Méthodes
            -------
            __init__(self, charges, num, description, prix)
                constructeur de la classe.
            """
    id_uo = db.Column(db.Integer, primary_key=True)
    charges = db.Column(db.Float, nullable=False)
    num = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    boncomms = db.relationship('AssoUoBoncomm', back_populates="uo")

    def __init__(self, charges, num, description, prix):
        self.charges = charges
        self.num = num
        self.description = description
        self.prix = prix


"""
    Méthode pour calculer, pour le mois voulu, le nombre de jours disponibles par semaine, sans prendre en compte le 
    samedi et le dimanche.
"""


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


"""
    Méthode pour calculer, pour le mois voulu, le nombre de jours disponibles par semaine, en prenant en compte le 
    samedi et le dimanche.
"""


def columnMoisWeekEnd(mois, annee):
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    columns = []
    numSem = dates[0].numSemaine()
    joursDispo = 0
    for date in dates:
        if date.numSemaine() == numSem:
            joursDispo += 1
        else:
            columns.append([numSem, joursDispo])
            numSem = date.numSemaine()
            joursDispo = 1
    columns.append([numSem, joursDispo])
    return columns


"""
    Méthode pour calculer l'ensemble des valeurs nécessaires pour la création des tables résumant l'avancement des 
    activités.
"""


def valeursGlobales(boncomm):
    joursConsommes = 0
    assoCollabs = boncomm.collabs
    collabs = []
    for asso in assoCollabs:
        collabs.append(asso.collab)
    consoCollabs = []
    for collab in collabs:
        imputations = db.session.query(Imputation).filter(Imputation.acti_id == boncomm.id_acti,
                                                          Imputation.collab_id == collab.id_collab,
                                                          Imputation.joursAllouesTache != 0).all()
        joursConsommesCollab = 0
        for imputation in imputations:
            joursConsommesCollab += imputation.joursAllouesTache
        consoCollabs.append(joursConsommesCollab)
        joursConsommes += joursConsommesCollab
    raf = boncomm.jourThq - joursConsommes
    avancement = int(joursConsommes / boncomm.jourThq * 100)
    ecart = boncomm.jourThq - (raf + joursConsommes)
    if joursConsommes == boncomm.jourThq:
        etat = "TE"
    elif joursConsommes < boncomm.jourThq:
        etat = ""
    else:
        etat = "HB"
    return [consoCollabs, etat, avancement, raf, joursConsommes, ecart]


"""
    Méthode pour renvoyer le nombre de jours total dans le mois.
"""


def nbJoursMois(mois, annee):
    if mois == 1 or mois == 3 or mois == 5 or mois == 7 or mois == 8 or mois == 10 or mois == 12:
        return 31
    elif mois == 2:
        if (annee - 2020) % 4 == 0:
            return 29
        else:
            return 28
    else:
        return 30


"""
    Méthode pour renvoyer le nombre de jours total dans le mois sans compter les week-ends.
"""


def nbJoursMoisSansWeekEnd(mois, annee):
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    nb = 0
    for date in dates:
        date_format = date.transfoDate().weekday()
        if date_format != 5 and date_format != 6:
            nb += 1
    return nb


"""
    Méthode pour renvoyer sous forme de str le mois voulu.
"""


def stringMois(mois):
    if mois == "1":
        return "Janvier"
    elif mois == "2":
        return "Février"
    elif mois == "3":
        return "Mars"
    elif mois == "4":
        return "Avril"
    elif mois == "5":
        return "Mai"
    elif mois == "6":
        return "Juin"
    elif mois == "7":
        return "Juillet"
    elif mois == "8":
        return "Août"
    elif mois == "9":
        return "Septembre"
    elif mois == "10":
        return "Octobre"
    elif mois == "11":
        return "Novembre"
    elif mois == "12":
        return "Décembre"
    else:
        return ""


def prixUoAn(uo, annee):  # Applique le pourcentgae de l'année au prix de l'année précédente, fonction récursive
    if annee == 2022:
        return uo.prix
    prixPrec = prixUoAn(uo, annee - 1)
    pourcentAn = db.session.query(Date).filter(Date.annee == annee).all()[0].pourcentAn
    return round(prixPrec * (1 + (pourcentAn / 100)), 2)


def tjmCollab(collab):
    tjm = 0
    fonctions = db.session.query(Fonction).all()
    assoFonctions = collab.fonctions  # listes de mêmes longueurs
    for i in range(len(fonctions)):
        affectation = assoFonctions[i].affectation
        tjm += (affectation / 100) * fonctions[i].tjm
    return tjm


def prixTjmCollab(collab, annee):
    tjm2022 = tjmCollab(collab)
    if annee == 2022:
        return tjm2022
    tjmPrec = prixTjmCollab(collab, annee - 1)
    pourcentAn = db.session.query(Date).filter(Date.annee == annee).all()[0].pourcentAn
    return round(tjmPrec * (1 + (pourcentAn / 100)), 2)


def calculerTotUo(boncomm):
    assoUos = boncomm.uos
    total = 0
    for assoUo in assoUos:
        uo = assoUo.uo
        facteur = assoUo.facteur
        total += float(facteur) * uo.prix
    return total


def collabsProjet(projet):
    collabs = []
    bons = db.session.query(Boncomm).filter(Boncomm.projet == projet, Boncomm.prodGdpOuFd != "Fd").all()
    for bon in bons:
        assos = bon.collabs
        for asso in assos:
            if asso.collab not in collabs:
                collabs.append(asso.collab)
    return collabs


def moisVisibles(mois ,annee):

    if mois == 12:
        moisSuivant = 1
        anneeSuivante = annee + 1
    else:
        moisSuivant = mois + 1
        anneeSuivante = annee
    moisVisibles = [[moisSuivant, anneeSuivante], [mois, annee]]  # Mois que l'on montrera dans le tableau
    for i in range(8):
        if mois == 1:
            mois = 12
            annee = annee - 1
            moisVisibles.append([mois, annee])
        else:
            mois = mois - 1
            moisVisibles.append([mois, annee])
    moisVisibles.reverse()
    return moisVisibles


db.create_all()
