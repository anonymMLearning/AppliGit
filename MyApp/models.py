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


class AssoGcmFonction(db.Model):
    """
            Réprésente l'association entre une fonction et un GCM.

            ...

            Attributs
            ----------
            gcm_id : int
                id du gcm, clé primaire.
            fonction_id : int
                id de la fonction, clé primaire.
            affectation : float
                pourcentage, représentant la part du temps de travail du collaborateur sur cette fonction.
            gcm :
                lien d'association au gcm.
            fonction :
                lien d'association à la fonction.
    """
    gcm_id = db.Column('gcm_id', db.Integer, db.ForeignKey('gcm.id_gcm'), primary_key=True)
    fonction_id = db.Column('fonction_id', db.Integer, db.ForeignKey('fonction.id_fonction'), primary_key=True)
    affectation = db.Column(db.Float, nullable=False)
    gcm = db.relationship("Gcm", back_populates="fonctions")
    fonction = db.relationship("Fonction", back_populates="gcms")


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


class AssoCollabSCR(db.Model):
    collab_id = db.Column('collab_id', db.Integer, db.ForeignKey('collab.id_collab'), primary_key=True)
    scr_id = db.Column('scr_id', db.Integer, db.ForeignKey('SCR.id_scr'), primary_key=True)
    annee = db.Column(db.Integer, primary_key=True)
    collab = db.relationship("Collab", back_populates="scrs")
    scr = db.relationship("SCR", back_populates="collabs")


class AssoCollabBooster(db.Model):
    collab_id = db.Column('collab_id', db.Integer, db.ForeignKey('collab.id_collab'), primary_key=True)
    booster_id = db.Column('booster_id', db.Integer, db.ForeignKey('booster.id_booster'), primary_key=True)
    annee = db.Column(db.Integer, nullable=False)
    collab = db.relationship("Collab", back_populates="boosters")
    booster = db.relationship("Booster", back_populates="collabs")


class Gcm(db.Model):
    """
        Réprésente un code GCM.

        ...

        Attributs
        ----------
        id_gcm : int
            id du GCM, clé primaire.
        code : str
            code GCM.
        tjm : float
            tjm associé à ce GCM.
        collabs : list
            ensemble des collaborateurs ayant ce code GCM.
        fonctions : list
           ensemble des fonctions associées à ce GCM.

        Méthodes
        -------
        __init__(self, code, tjm)
            constructeur de la classe
    """

    id_gcm = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(30), nullable=False)
    tjm = db.Column(db.Float, nullable=False)
    collabs = db.relationship('Collab', backref='gcm', uselist=False)
    fonctions = db.relationship('AssoGcmFonction', back_populates="gcm")

    def __init__(self, code, tjm):
        self.code = code
        self.tjm = tjm


class Booster(db.Model):
    id_booster = db.Column(db.Integer, primary_key=True)
    mois = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    com = db.Column(db.String(100), nullable=False)
    monteG = db.Column(db.Float, nullable=False)
    monteR = db.Column(db.Float, nullable=False)
    collabs = db.relationship('AssoCollabBooster', back_populates="booster")

    def __init__(self, mois, annee, com, monteG, monteR):
        self.mois = mois
        self.annee = annee
        self.com = com
        self.monteG = monteG
        self.monteR = monteR


class Collab(db.Model):
    """
        Réprésente un collaborateur de l'équipe.
        ...

        Attributs
        ----------
        id_collab: int
        id du collaborateur, clé primaire.
        nom: str
            nom du collaborateur.
        prenom: str
            prénom du collaborateur.
        access: int
            niveau d'accès du collaborateur.
        entreprise: str
            entreprise du collaborateur.
        imputations: list
            ensemble des imputations associées au collaborateur, venant de l'association entre la classe Collab et Imputation.
        boncomms: list
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
    rafInit = db.Column(db.Float, nullable=False)
    gcm_id = db.Column(db.Integer, db.ForeignKey('gcm.id_gcm'), nullable=False)
    imputations = db.relationship('Imputation', backref='collab', uselist=False)
    boncomms = db.relationship('AssociationBoncommCollab', back_populates="collab")
    scrs = db.relationship('AssoCollabSCR', back_populates="collab")
    boosters = db.relationship('AssoCollabBooster', back_populates="collab")

    def __init__(self, nom, prenom, access, entreprise, rafInit):
        self.nom = nom
        self.prenom = prenom
        self.access = access
        self.entreprise = entreprise
        self.rafInit = rafInit

    def abreviation(self):
        prenom = self.prenom[0]
        nomDebut = self.nom[0]
        nomFin = self.nom[-1]
        abrev = (prenom + nomDebut + nomFin).upper()
        return abrev


class Fonction(db.Model):
    id_fonction = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    gcms = db.relationship('AssoGcmFonction', back_populates="fonction")

    def __init__(self, nom):
        self.nom = nom


class SCR(db.Model):
    id_scr = db.Column(db.Integer, primary_key=True)
    cout = db.Column(db.Float, nullable=False)
    ponderation = db.Column(db.Float, nullable=False)
    collabs = db.relationship('AssoCollabSCR', back_populates="scr")

    def __init__(self, cout, ponderation):
        self.cout = cout
        self.ponderation = ponderation


class Imputation(db.Model):
    id_imp = db.Column(db.Integer, primary_key=True)
    acti_id = db.Column(db.Integer, db.ForeignKey('boncomm.id_acti'), nullable=False)
    collab_id = db.Column(db.Integer, db.ForeignKey('collab.id_collab'), nullable=False)
    date_id = db.Column(db.Integer, db.ForeignKey('date.id_date'), nullable=False)
    joursAllouesTache = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)

    def __init__(self, acti_id, collab_id, date_id, joursAllouesTache, type):
        self.acti_id = acti_id
        self.collab_id = collab_id
        self.date_id = date_id
        self.joursAllouesTache = joursAllouesTache
        self.type = type

    def get_jours(self):
        imp = db.session.query(Imputation).filter(Imputation.acti_id == self.acti_id,
                                                  Imputation.collab_id == self.collab_id,
                                                  Imputation.date_id == self.date_id).all()
        jours = imp[0].joursAllouesTache
        return jours


class Boncomm(db.Model):
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
    """ Pour les formations """
    horsProjet = db.Column(db.String(10))
    nbJoursFormation = db.Column(db.Float)
    """ ------------------- """
    """ Pour les congés """
    nbCongesTot = db.Column(db.Float)
    nbCongesPose = db.Column(db.Float)
    """ --------------- """
    """ Pour les autres activités """
    nbJoursAutre = db.Column(db.Float)
    """ ------------------------- """
    """ Pour les frais de déplacement """
    apm = db.Column(db.String(50))
    lieu = db.Column(db.String(50))
    client = db.Column(db.String(50))
    dateSign = db.Column(db.String(50))
    margeLib = db.Column(db.Float)
    """ ----------------------------- """
    imputations = db.relationship('Imputation', backref='boncomm', uselist=False)
    noteDeFrais = db.relationship('NoteDeFrais', backref='boncomm', uselist=False)
    collabs = db.relationship('AssociationBoncommCollab', back_populates="boncomm")
    uos = db.relationship('AssoUoBoncomm', back_populates="boncomm")

    def __init__(self, activite, etat, com, anneeTarif, caAtos, jourThq, delais, montantHT, partEGIS, num, poste,
                 projet, tjm, notification, facturation, prodGdpOuFd, dateDebut, dateFinPrev, dateNotif, dateFinOp,
                 horsProjet, nbJoursFormation, nbCongesTot, nbCongesPose, nbJoursAutre, apm, lieu, client, dateSign,
                 margeLib):
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
        self.apm = apm
        self.lieu = lieu
        self.client = client
        self.dateSign = dateSign
        self.margeLib = margeLib


class Date(db.Model):
    id_date = db.Column(db.Integer, primary_key=True)
    jour = db.Column(db.Integer, nullable=False)
    mois = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    pourcentAn = db.Column(db.Float, nullable=False)
    tjm = db.Column(db.Float, nullable=False)
    equipe = db.Column(db.Float, nullable=False)
    scrMoyRetenu = db.Column(db.Float, nullable=False)
    imputations = db.relationship('Imputation', backref='date', uselist=False)

    def __init__(self, jour, mois, annee, pourcentAn, tjm, equipe, scrMoyRetenu):
        self.jour = jour
        self.mois = mois
        self.annee = annee
        self.pourcentAn = pourcentAn
        self.tjm = tjm
        self.equipe = equipe
        self.scrMoyRetenu = scrMoyRetenu

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
    id_uo = db.Column(db.Integer, primary_key=True)
    charges = db.Column(db.Float, nullable=False)
    num = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    prix = db.Column(db.Float, nullable=False)
    boncomms = db.relationship('AssoUoBoncomm', back_populates="uo")

    def __init__(self, charges, num, description, type, prix):
        self.charges = charges
        self.num = num
        self.type = type
        self.description = description
        self.prix = prix


class Prod(db.Model):
    id_prod = db.Column(db.Integer, primary_key=True)
    mois = db.Column(db.Integer, nullable=False)
    annee = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    amort = db.Column(db.Float, nullable=False)
    coutDP = db.Column(db.Float, nullable=False)
    coutTeam = db.Column(db.Float, nullable=False)
    jourMoisDP = db.Column(db.Float, nullable=False)
    jourMoisTeam = db.Column(db.Float, nullable=False)

    def __init__(self, mois, annee, type, amort, coutDP, coupTeam, jourMoisDP, joursMoisTeam):
        self.mois = mois
        self.annee = annee
        self.type = type
        self.amort = amort
        self.coutDP = coutDP
        self.coupTeam = coupTeam
        self.jourMoisDP = jourMoisDP
        self.joursMoisTeam = joursMoisTeam


class NoteDeFrais(db.Model):
    id_ndf = db.Column(db.Integer, primary_key=True)
    acti_id = db.Column(db.Integer, db.ForeignKey('boncomm.id_acti'), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    depense = db.Column(db.Float, nullable=False)

    def __int__(self, acti_id, type, depense):
        self.acti_id = acti_id
        self.type = type
        self.depense = depense


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


def columnMoisWeekEnd(mois, annee):
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    columns = []
    print(mois, annee)
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
                                                          Imputation.joursAllouesTache != 0,
                                                          Imputation.type == "client").all()
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


def nbJoursMoisSansWeekEnd(mois, annee):
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    nb = 0
    for date in dates:
        date_format = date.transfoDate().weekday()
        if date_format != 5 and date_format != 6:
            nb += 1
    return nb


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


def prixTjmGcm(gcm, annee):
    tjmInit = gcm.tjm
    if annee == 2021:
        return tjmInit
    tjmPrec = prixTjmGcm(gcm, annee - 1)
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


def moisVisibles(mois, annee):
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
