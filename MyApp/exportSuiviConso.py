import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from MyApp.models import *
from datetime import datetime
from flask import Flask, request


def export_excel_SSQSuiviConso():
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    das = request.form['das']
    moisDebut, anneeDebut = request.form['moisD'], request.form['anneeD']
    moisFin, anneeFin = request.form['moisF'], request.form['anneeF']
    if int(anneeDebut) == int(anneeFin):
        workbook = xlsxwriter.Workbook(
            r'C:\Users\a' + das + '\Downloads\AtosSSQSuiviConso-' + str(anneeDebut) + '.xlsx')
    else:
        workbook = xlsxwriter.Workbook(
            r'C:\Users\a' + '857591' + '\Downloads\AtosSSQSuiviConso-' + str(anneeDebut) + '/' + str(
                anneeFin) + '.xlsx')
    suiviConso = workbook.add_worksheet('SSQ Suivi Conso')
    suiviConso.set_tab_color('#305496')

    """----- Format des titres -----"""
    format_titre = workbook.add_format()
    format_titre.set_font_color('#305496')
    format_titre.set_font_size(18)
    format_titre.set_italic()
    format_titre.set_underline()

    """----- Format écritures rouges -----"""
    format_font_rouge = workbook.add_format()
    format_font_rouge.set_font_color('red')
    format_font_rouge.set_font_size(18)

    """----- Format cases en-têtes -----"""
    format_entete = workbook.add_format()
    format_entete.set_font_color('white')
    format_entete.set_bold()
    format_entete.set_bg_color('#305496')
    format_entete.set_align('center')
    format_entete.set_border()

    """----- Format des formations et autres activités -----"""
    format_activite = workbook.add_format()
    format_activite.set_bg_color('#8EA9DB')
    format_activite.set_align('center')
    format_activite.set_border()

    """----- Format des bons de commande -----"""
    format_bon = workbook.add_format()
    format_bon.set_bg_color('#D9E1F2')
    format_bon.set_align('center')
    format_bon.set_border()

    """----- Format des activités finies -----"""
    format_fin = workbook.add_format()
    format_fin.set_bg_color('gray')
    format_fin.set_align('center')
    format_fin.set_border()

    """----- Format vert -----"""
    format_vert = workbook.add_format()
    format_vert.set_bg_color('#548235')
    format_vert.set_bold()
    format_vert.set_align('center')
    format_vert.set_border()

    """----- Format rouge -----"""
    format_rouge = workbook.add_format()
    format_rouge.set_bg_color('#FF2525')
    format_entete.set_font_color('white')
    format_rouge.set_bold()
    format_rouge.set_align('center')
    format_rouge.set_border()

    """----- Format des dates -----"""
    format_date = workbook.add_format({'num_format': 'd-mmm'})
    format_date.set_font_color('white')
    format_date.set_bold()
    format_date.set_bg_color('#305496')
    format_date.set_align('center')
    format_date.set_border()
    """--------------------------------------------------------------------------------------------------------------"""
    """------------------------------------------ Feuille SSQ Suivi Conso -------------------------------------------"""
    """ ---------- Récupération des données ---------- """
    monteeDoc = db.session.query(Boncomm).filter(Boncomm.activite == "Montée Doc. Autonomie").all()[0]
    bonsGdp = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Gdp").all()
    horsProjet = db.session.query(Boncomm).filter(Boncomm.horsProjet == "Oui").all()
    # On va séparer les formations sur supervision des autres :
    formationsNonTri = db.session.query(Boncomm).filter(Boncomm.nbJoursFormation != 0,
                                                        Boncomm.horsProjet == "Non").all()
    formationsSUPV = []
    formations = []
    for formation in formationsNonTri:
        if formation.activite[0:4] == "SUPV":
            formationsSUPV.append(formation)
        else:
            formations.append(formation)
    nbFormations = len(formations)

    # Idem que pour le plan de charge, mais on construit la liste des mois qu'il faudra afficher
    if anneeDebut == anneeFin:
        dataMois = [str(int(moisDebut) + i) + '/' + anneeDebut for i in range(int(moisFin) - int(moisDebut) + 1)]
    else:
        dataMois = [str(int(moisDebut) + i) + '/' + anneeDebut for i in range(12 - int(moisDebut) + 1)]
        for i in range(int(anneeFin) - int(anneeDebut) - 1):
            for j in range(12):
                dataMois.append(str(j + 1) + '/' + str(int(anneeDebut) + i))
        for j in range(int(moisFin)):
            dataMois.append(str(j + 1) + '/' + anneeFin)
    columns = []  # Contiendra les num de semaine et le nb de jours dispo par semaine
    nbTotSemaine = 0
    for mois in dataMois:
        if len(mois) == 6:  # Mois à un chiffre
            columns.append([mois[0], mois[2:], columnMois(mois[0], mois[2:])])
            nbTotSemaine += len(columns[-1][2])
        else:
            columns.append([mois[0:2], mois[3:], columnMois(mois[0:2], mois[3:])])

    # Création des différentes parties du tableau :

    collabs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()
    nbCollabs = len(collabs)
    dataCollabs = [collab.abreviation() for collab in collabs]
    dataMs4Form = []
    dataMs4Prod = []
    dataFormations = [[] for formation in formations]
    dataMonteeDoc = []
    dataAbsences = [[], []]
    dataGdp = []
    for mois in columns:
        dataGdp.append([0 for i in range(len(mois[2]))])
    for collab in collabs:
        dataMs4FormCollab, dataMs4ProdCollab, dataMonteeDocCollab, dataAbsencesCongesCollab, dataAbsencesHPCollab = [], [], [], [], []
        for mois in columns:
            dataMs4FormCollab.append([0 for i in range(len(mois[2]))])
            dataMs4ProdCollab.append([0 for i in range(len(mois[2]))])
            dataMonteeDocCollab.append([0 for i in range(len(mois[2]))])
            dataAbsencesCongesCollab.append([0 for i in range(len(mois[2]))])
            dataAbsencesHPCollab.append([0 for i in range(len(mois[2]))])
        dataMs4Form.append(dataMs4FormCollab)
        dataMs4Prod.append(dataMs4ProdCollab)
        for j in range(len(formations)):
            dataFormationsCollab = []
            for mois in columns:
                dataFormationsCollab.append([0 for i in range(len(mois[2]))])
            dataFormations[j].append(dataFormationsCollab)
        dataMonteeDoc.append(dataMonteeDocCollab)
        dataAbsences[0].append(dataAbsencesCongesCollab)
        dataAbsences[1].append(dataAbsencesHPCollab)
    # Remplissage des données pour chaque semaine :
    for k in range(len(collabs)):
        collab = collabs[k]
        for i in range(len(columns)):  # Pour chaque mois à afficher
            mois = columns[i][0]
            annee = columns[i][1]
            dates = db.session.query(Date).filter(Date.annee == annee, Date.mois == mois).all()
            for j in range(len(columns[i][2])):  # Nombre de semaines dans le mois
                column = columns[i][2][j]  # C'est une semaine
                numSemaine = column[0]
                datesAccess = []  # Contiendra les jours de la semaine
                for date in dates:
                    if date.numSemaine() == numSemaine:
                        datesAccess.append(date)
                for date in datesAccess:
                    # Formations SUPV :
                    for formation in formationsSUPV:
                        imput = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                    Imputation.acti_id == formation.id_acti,
                                                                    Imputation.date_id == date.id_date,
                                                                    Imputation.type == "atos").all()

                        if imput:  # Liste non vide
                            # 0 : Formations SUPV | k : collab n°k | i : mois n°i | j : semaine n°j
                            dataMs4Form[k][i][j] += imput[0].joursAllouesTache

                    # Prod MS4 :
                    assos = collab.boncomms
                    for asso in assos:
                        boncomm = asso.boncomm
                        if boncomm.prodGdpOuFd == "Prod":

                            imput = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                        Imputation.acti_id == boncomm.id_acti,
                                                                        Imputation.date_id == date.id_date,
                                                                        Imputation.type == "atos").all()

                            if imput:  # Liste non vide
                                # 1 : Prod MS4 | k : collab n°k | i : mois n°i | j : semaine n°j
                                dataMs4Prod[k][i][j] += imput[0].joursAllouesTache

                    # Formations :
                    for n in range(len(formations)):
                        imput = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                    Imputation.acti_id == formations[n].id_acti,
                                                                    Imputation.date_id == date.id_date,
                                                                    Imputation.type == "atos").all()
                        if imput:  # Liste non vide
                            # n : formation n°n |  k : collab n°k | i : mois n°i | j : semaine n°j
                            dataFormations[n][k][i][j] += imput[0].joursAllouesTache

                    # Montée Doc :
                    imput = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                Imputation.acti_id == monteeDoc.id_acti,
                                                                Imputation.date_id == date.id_date,
                                                                Imputation.type == "atos").all()
                    if imput:  # Liste non vide
                        # k : collab n°k | i : mois n°i | j : semaine n°j
                        dataMonteeDoc[k][i][j] += imput[0].joursAllouesTache

                    # Gdp :
                    if collab.nom == "Vieira":
                        for bon in bonsGdp:
                            imput = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                        Imputation.acti_id == bon.id_acti,
                                                                        Imputation.date_id == date.id_date,
                                                                        Imputation.type == "atos").all()
                            if imput:  # Liste non vide
                                # i : mois n°i | j : semaine n°j
                                dataGdp[i][j] += imput[0].joursAllouesTache

                    # Congés :
                    assos = collab.boncomms
                    for asso in assos:
                        if asso.boncomm.nbCongesTot != 0:
                            conges = asso.boncomm
                    imput = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                Imputation.acti_id == conges.id_acti,
                                                                Imputation.date_id == date.id_date,
                                                                Imputation.type == "atos").all()
                    if imput:  # Liste non vide
                        # 0 : congés | k : collab n°k | i : mois n°i | j : semaine n°j
                        dataAbsences[0][k][i][j] += imput[0].joursAllouesTache

                    # Hors Projet
                    for bon in horsProjet:
                        imput = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                    Imputation.acti_id == bon.id_acti,
                                                                    Imputation.date_id == date.id_date,
                                                                    Imputation.type == "atos").all()
                        if imput:  # Liste non vide
                            # 1 : HP | k : collab n°k | i : mois n°i | j : semaine n°j
                            dataAbsences[1][k][i][j] += imput[0].joursAllouesTache
    collabs = db.session.query(Collab).filter(Collab.access == 3).all()
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    suiviConso.set_column_pixels('A:A', 10)
    suiviConso.set_row_pixels(0, 10)
    suiviConso.set_column_pixels('B:B', 170)
    suiviConso.set_column_pixels('C:C', 80)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    if anneeDebut == anneeFin:
        suiviConso.write('B2', 'Atos SSQ Suivi Conso ' + str(anneeDebut), format_titre)
    else:
        suiviConso.write('B2', 'Atos SSQ Suivi Conso ' + str(anneeDebut) + '- ' + str(anneeFin), format_titre)
    "----- En-têtes -----"
    suiviConso.write('C6', 'Jours dispo', format_entete)
    col = 3
    for j in range(len(dataMois)):
        mois = dataMois[j]
        suiviConso.write(xl_col_to_name(col) + '4', str(mois), format_entete)
        suiviConso.write(xl_col_to_name(col) + '5', 'S' + str(columns[j][2][0][0]), format_entete)
        suiviConso.write(xl_col_to_name(col) + '6', str(columns[j][2][0][1]), format_activite)
        col += 1
        for i in range(1, len(columns[j][2])):
            suiviConso.write(xl_col_to_name(col) + '5', 'S' + str(columns[j][2][i][0]), format_entete)
            suiviConso.write(xl_col_to_name(col) + '6', str(columns[j][2][i][1]), format_activite)
            suiviConso.write(xl_col_to_name(col) + '4', "", format_entete)
            col += 1
        suiviConso.write(xl_col_to_name(col) + str(4), "", format_entete)
        suiviConso.write(xl_col_to_name(col) + str(5), "", format_entete)
        suiviConso.write(xl_col_to_name(col) + str(6), "", format_entete)
        suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
        col += 1
    nbCol = col
    "----- Activités -----"
    row = 7
    """ MS - Prod """
    suiviConso.write('B' + str(row), "MS - Prod", format_entete)
    for j in range(2, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row),
                         "=SUM(" + xl_col_to_name(j) + str(row + 1) + ":" + xl_col_to_name(j) + str(
                             row + nbCollabs * 2 + 1) + ")", format_entete)
    row += 1

    # Formations sur supervision :
    for i in range(nbCollabs):
        suiviConso.write('B' + str(row), "Form. sur supervision", format_activite)
        suiviConso.write('C' + str(row), dataCollabs[i], format_activite)
        col = 3
        for mois in dataMs4Form[i]:
            for sem in mois:
                suiviConso.write(xl_col_to_name(col) + str(row), sem, format_bon)
                col += 1
            suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
            suiviConso.write(xl_col_to_name(col) + str(row), "", format_entete)
            col += 1
        row += 1

    suiviConso.set_row_pixels(row - 1, 5)
    for j in range(1, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row), "", format_entete)
    row += 1
    # Prod sur bon de commande :
    for i in range(nbCollabs):
        suiviConso.write('B' + str(row), "Prod. sur BC", format_activite)
        suiviConso.write('C' + str(row), dataCollabs[i], format_activite)
        col = 3
        for mois in dataMs4Form[i]:
            for sem in mois:
                suiviConso.write(xl_col_to_name(col) + str(row), sem, format_bon)
                col += 1
            suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
            suiviConso.write(xl_col_to_name(col) + str(row), "", format_entete)
            col += 1
        row += 1

    """ Formations """
    suiviConso.write('B' + str(row), "Formations", format_entete)
    for j in range(2, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row),
                         "=SUM(" + xl_col_to_name(j) + str(row + 1) + ":" + xl_col_to_name(j) + str(
                             row + nbCollabs * nbFormations + 1) + ")", format_entete)
    row += 1

    # Formations :
    for k in range(nbFormations):
        for i in range(nbCollabs):
            suiviConso.write('B' + str(row), formations[k].activite, format_activite)
            suiviConso.write('C' + str(row), dataCollabs[i], format_activite)
            col = 3
            for mois in dataFormations[k][i]:
                for sem in mois:
                    suiviConso.write(xl_col_to_name(col) + str(row), sem, format_bon)
                    col += 1
                suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
                suiviConso.write(xl_col_to_name(col) + str(row), "", format_entete)
                col += 1
            row += 1
        if k != nbFormations - 1:
            suiviConso.set_row_pixels(row - 1, 5)
            for j in range(1, nbCol):
                suiviConso.write(xl_col_to_name(j) + str(row), "", format_entete)
            row += 1

    """ Montée Doc. """
    suiviConso.write('B' + str(row), "Montée Doc. Autonomie", format_entete)
    for j in range(2, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row),
                         "=SUM(" + xl_col_to_name(j) + str(row + 1) + ":" + xl_col_to_name(j) + str(
                             row + nbCollabs) + ")", format_entete)
    row += 1

    for i in range(nbCollabs):
        suiviConso.write('B' + str(row), "Montée Doc.", format_activite)
        suiviConso.write('C' + str(row), dataCollabs[i], format_activite)
        col = 3
        for mois in dataMonteeDoc[i]:
            for sem in mois:
                suiviConso.write(xl_col_to_name(col) + str(row), sem, format_bon)
                col += 1
            suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
            suiviConso.write(xl_col_to_name(col) + str(row), "", format_entete)
            col += 1
        row += 1

    """ prépa - GdP """
    suiviConso.write('B' + str(row), "prépa - GdP", format_entete)
    for j in range(2, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row),
                         "=SUM(" + xl_col_to_name(j) + str(row + 1) + ":" + xl_col_to_name(j) + str(
                             row + 1) + ")", format_entete)
    row += 1

    suiviConso.write('B' + str(row), "prépa - GdP", format_activite)
    suiviConso.write('C' + str(row), "AVA", format_activite)
    col = 3
    for mois in dataGdp:
        for sem in mois:
            suiviConso.write(xl_col_to_name(col) + str(row), sem, format_bon)
            col += 1
        suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
        suiviConso.write(xl_col_to_name(col) + str(row), "", format_entete)
        col += 1
    row += 1

    """ Absences """
    suiviConso.write('B' + str(row), "Absences", format_entete)
    for j in range(2, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row),
                         "=SUM(" + xl_col_to_name(j) + str(row + 1) + ":" + xl_col_to_name(j) + str(
                             row + nbCollabs * 2 + 1) + ")", format_entete)
    row += 1

    # Congés :
    for i in range(nbCollabs):
        suiviConso.write('B' + str(row), "Congés", format_activite)
        suiviConso.write('C' + str(row), dataCollabs[i], format_activite)
        col = 3
        for mois in dataAbsences[0][i]:
            for sem in mois:
                suiviConso.write(xl_col_to_name(col) + str(row), sem, format_bon)
                col += 1
            suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
            suiviConso.write(xl_col_to_name(col) + str(row), "", format_entete)
            col += 1
        row += 1

    suiviConso.set_row_pixels(row - 1, 5)
    for j in range(1, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row), "", format_entete)
    row += 1

    # Hors-Projet :
    for i in range(nbCollabs):
        suiviConso.write('B' + str(row), "Hors-Projet", format_activite)
        suiviConso.write('C' + str(row), dataCollabs[i], format_activite)
        col = 3
        for mois in dataAbsences[1][i]:
            for sem in mois:
                suiviConso.write(xl_col_to_name(col) + str(row), sem, format_bon)
                col += 1
            suiviConso.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
            suiviConso.write(xl_col_to_name(col) + str(row), "", format_entete)
            col += 1
        row += 1
    suiviConso.set_row_pixels(row - 1, 5)
    for j in range(1, nbCol):
        suiviConso.write(xl_col_to_name(j) + str(row), "", format_entete)
    row += 1

    """--------------------------------------------------------------------------------------------------------------"""
    workbook.close()
    return None
