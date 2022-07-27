import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from MyApp.models import *
from datetime import datetime
from flask import Flask, request


def export_excel_suivi_booster():
    workbook = xlsxwriter.Workbook('MS4 - SSQ - Suivi Booster.xlsx')
    suiviSSQInit = workbook.add_worksheet('Suivi Conso SSQ Init')
    suiviSSQInit.set_tab_color('#305496')
    suiviSSQ = workbook.add_worksheet('Suivi Conso SSQ')
    suiviSSQ.set_tab_color('#305496')
    boosterConso = workbook.add_worksheet('Booster Consom.')
    boosterConso.set_tab_color('#305496')

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
    format_bon.set_align('vcenter')
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
    """-------------------------------------------- Suivi Conso SSQ init --------------------------------------------"""
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    suiviSSQInit.set_column_pixels('A:A', 10)
    suiviSSQInit.set_row_pixels(0, 10)
    suiviSSQInit.set_column_pixels('B:B', 100)
    suiviSSQInit.set_column_pixels('C:C', 90)
    suiviSSQInit.set_column_pixels('D:D', 70)
    suiviSSQInit.set_column_pixels('E:E', 70)
    suiviSSQInit.set_column_pixels('F:F', 70)
    suiviSSQInit.set_column_pixels('G:G', 70)
    suiviSSQInit.set_column_pixels('H:H', 70)
    suiviSSQInit.set_column_pixels('I:I', 70)
    suiviSSQInit.set_column_pixels('J:J', 90)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    suiviSSQInit.write('B2', 'Suivi Conso. SSQ - Init', format_titre)
    "----- En-têtes -----"
    suiviSSQInit.write('D4', 'AVA', format_entete)
    suiviSSQInit.write('E4', 'CDE', format_entete)
    suiviSSQInit.write('F4', 'FOY', format_entete)
    suiviSSQInit.write('G4', 'CLN', format_entete)
    suiviSSQInit.write('H4', 'CPR', format_entete)
    suiviSSQInit.write('I4', 'GLE', format_entete)
    suiviSSQInit.write('J4', 'Total', format_entete)

    "----- Remplissage données -----"
    """--- Février 2021 ---"""
    row = 5

    suiviSSQInit.write('B' + str(row), 'Février 2021', format_entete)
    suiviSSQInit.write('C' + str(row), 'RAF Update', format_entete)
    suiviSSQInit.write('D' + str(row), '19.5', format_bon)
    suiviSSQInit.write('E' + str(row), '6', format_bon)
    suiviSSQInit.write('F' + str(row), '0.75', format_bon)
    suiviSSQInit.write('G' + str(row), '20', format_bon)
    suiviSSQInit.write('H' + str(row), '20', format_bon)
    suiviSSQInit.write('I' + str(row), '20', format_bon)
    suiviSSQInit.write('J' + str(row), '86.25', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S06', format_activite)
    suiviSSQInit.write('D' + str(row), '5', format_bon)
    suiviSSQInit.write('E' + str(row), '5', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '3', format_bon)
    suiviSSQInit.write('H' + str(row), '5', format_bon)
    suiviSSQInit.write('I' + str(row), '5', format_bon)
    suiviSSQInit.write('J' + str(row), '23', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S07', format_activite)
    suiviSSQInit.write('D' + str(row), '4', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '1', format_bon)
    suiviSSQInit.write('H' + str(row), '5', format_bon)
    suiviSSQInit.write('I' + str(row), '2', format_bon)
    suiviSSQInit.write('J' + str(row), '12', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S08', format_activite)
    suiviSSQInit.write('D' + str(row), '2.5', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '1', format_bon)
    suiviSSQInit.write('H' + str(row), '5', format_bon)
    suiviSSQInit.write('I' + str(row), '5', format_bon)
    suiviSSQInit.write('J' + str(row), '13.5', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'Conso. Totale', format_entete)
    suiviSSQInit.write('D' + str(row), '11.5', format_activite)
    suiviSSQInit.write('E' + str(row), '2', format_activite)
    suiviSSQInit.write('F' + str(row), '0', format_activite)
    suiviSSQInit.write('G' + str(row), '5', format_activite)
    suiviSSQInit.write('H' + str(row), '15', format_activite)
    suiviSSQInit.write('I' + str(row), '12', format_activite)
    suiviSSQInit.write('J' + str(row), '48.5', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'RAF', format_entete)
    suiviSSQInit.write('D' + str(row), '8', format_activite)
    suiviSSQInit.write('E' + str(row), '1', format_activite)
    suiviSSQInit.write('F' + str(row), '0.75', format_activite)
    suiviSSQInit.write('G' + str(row), '15', format_activite)
    suiviSSQInit.write('H' + str(row), '5', format_activite)
    suiviSSQInit.write('I' + str(row), '8', format_activite)
    suiviSSQInit.write('J' + str(row), '37.75', format_entete)
    row += 1

    """--- Mars 2021 ---"""

    suiviSSQInit.write('B' + str(row), 'Mars 2021', format_entete)
    suiviSSQInit.write('C' + str(row), 'RAF Update', format_entete)
    suiviSSQInit.write('D' + str(row), '8', format_bon)
    suiviSSQInit.write('E' + str(row), '1', format_bon)
    suiviSSQInit.write('F' + str(row), '0.75', format_bon)
    suiviSSQInit.write('G' + str(row), '15', format_bon)
    suiviSSQInit.write('H' + str(row), '5', format_bon)
    suiviSSQInit.write('I' + str(row), '8', format_bon)
    suiviSSQInit.write('J' + str(row), '37.75', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S09', format_activite)
    suiviSSQInit.write('D' + str(row), '5', format_bon)
    suiviSSQInit.write('E' + str(row), '1', format_bon)
    suiviSSQInit.write('F' + str(row), '0.75', format_bon)
    suiviSSQInit.write('G' + str(row), '1.5', format_bon)
    suiviSSQInit.write('H' + str(row), '5', format_bon)
    suiviSSQInit.write('I' + str(row), '5', format_bon)
    suiviSSQInit.write('J' + str(row), '18.25', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S10', format_activite)
    suiviSSQInit.write('D' + str(row), '', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '0.5', format_bon)
    suiviSSQInit.write('H' + str(row), '', format_bon)
    suiviSSQInit.write('I' + str(row), '', format_bon)
    suiviSSQInit.write('J' + str(row), '0.5', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S11', format_activite)
    suiviSSQInit.write('D' + str(row), '', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '1.5', format_bon)
    suiviSSQInit.write('H' + str(row), '', format_bon)
    suiviSSQInit.write('I' + str(row), '3', format_bon)
    suiviSSQInit.write('J' + str(row), '4.5', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S12', format_activite)
    suiviSSQInit.write('D' + str(row), '', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '5', format_bon)
    suiviSSQInit.write('H' + str(row), '', format_bon)
    suiviSSQInit.write('I' + str(row), '', format_bon)
    suiviSSQInit.write('J' + str(row), '5', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S13', format_activite)
    suiviSSQInit.write('D' + str(row), '', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '3', format_bon)
    suiviSSQInit.write('H' + str(row), '', format_bon)
    suiviSSQInit.write('I' + str(row), '', format_bon)
    suiviSSQInit.write('J' + str(row), '3', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'Conso. Totale', format_entete)
    suiviSSQInit.write('D' + str(row), '5', format_activite)
    suiviSSQInit.write('E' + str(row), '1', format_activite)
    suiviSSQInit.write('F' + str(row), '0.75', format_activite)
    suiviSSQInit.write('G' + str(row), '11.5', format_activite)
    suiviSSQInit.write('H' + str(row), '5', format_activite)
    suiviSSQInit.write('I' + str(row), '8', format_activite)
    suiviSSQInit.write('J' + str(row), '31.25', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'RAF', format_entete)
    suiviSSQInit.write('D' + str(row), '3', format_activite)
    suiviSSQInit.write('E' + str(row), '0', format_activite)
    suiviSSQInit.write('F' + str(row), '0', format_activite)
    suiviSSQInit.write('G' + str(row), '3.5', format_activite)
    suiviSSQInit.write('H' + str(row), '0', format_activite)
    suiviSSQInit.write('I' + str(row), '0', format_activite)
    suiviSSQInit.write('J' + str(row), '6.5', format_entete)
    row += 1

    """--- Avril 2021 ---"""

    suiviSSQInit.write('B' + str(row), 'Avril 2021', format_entete)
    suiviSSQInit.write('C' + str(row), 'RAF Update', format_entete)
    suiviSSQInit.write('D' + str(row), '3', format_bon)
    suiviSSQInit.write('E' + str(row), '0', format_bon)
    suiviSSQInit.write('F' + str(row), '0', format_bon)
    suiviSSQInit.write('G' + str(row), '3.5', format_bon)
    suiviSSQInit.write('H' + str(row), '0', format_bon)
    suiviSSQInit.write('I' + str(row), '0', format_bon)
    suiviSSQInit.write('J' + str(row), '6.5', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S13', format_activite)
    suiviSSQInit.write('D' + str(row), '', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '2', format_bon)
    suiviSSQInit.write('H' + str(row), '', format_bon)
    suiviSSQInit.write('I' + str(row), '', format_bon)
    suiviSSQInit.write('J' + str(row), '2', format_entete)
    row += 1

    suiviSSQInit.write('C' + str(row), 'S14', format_activite)
    suiviSSQInit.write('D' + str(row), '', format_bon)
    suiviSSQInit.write('E' + str(row), '', format_bon)
    suiviSSQInit.write('F' + str(row), '', format_bon)
    suiviSSQInit.write('G' + str(row), '1.5', format_bon)
    suiviSSQInit.write('H' + str(row), '', format_bon)
    suiviSSQInit.write('I' + str(row), '', format_bon)
    suiviSSQInit.write('J' + str(row), '1.5', format_entete)
    row += 1
    """---------------------------------------------------------------------------------------------------------"""
    """-------------------------------------------- Suivi Conso SSQ --------------------------------------------"""
    """ ---------- Récupération des données ---------- """
    moisDebut, anneeDebut = 2, 2021
    dateNow = str(datetime.now())
    anneeFin, moisFin = int(dateNow[:4]), int(dateNow[5:7])
    if anneeDebut == anneeFin:
        periode = [[moisDebut + i, anneeDebut] for i in range(moisFin - moisDebut + 1)]
    else:
        periode = [[moisDebut + i, anneeDebut] for i in range(12 - moisDebut + 1)]
        for i in range(int(anneeFin) - int(anneeDebut) - 1):
            for j in range(12):
                periode.append([j + 1, anneeDebut + i + 1])
        for i in range(moisFin):
            periode.append([i + 1, anneeFin])
    dataToShow = []  # Contiendra pour chaque mois les données pour construire le tableau
    rafInitTot = 0
    rafsUpdateTot = []
    totConsoTot = []
    rafTot = []
    cumulesMois = []
    collabs = db.session.query(Collab).all()
    for k in range(len(periode)):  # Pour chaque mois à montrer
        mois = periode[k][0]
        annee = periode[k][1]
        semaines = columnMois(mois, annee)
        booster = db.session.query(Booster).filter(Booster.mois == mois, Booster.annee == annee).all()[0]
        """Contiendra une liste avec les RAF Update de chaque collab sur le mois, une liste de listes par semaine du 
        mois avec la conso de chaque collab, une liste pour la conso. totale et une liste pour le RAF du mois : """
        dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
        datesAccess = []  # Jours des différentes semaines pour récupérer les imputations
        consoSemaines = []
        rafsUpdate, raf, consoTot = [], [0 for i in range(len(collabs))], [0 for i in range(len(collabs))]
        for j in range(len(semaines)):
            numSem = semaines[j][0]
            if (mois == 3 or mois == 2) and annee == 2021 and 6 <= numSem <= 9:
                consoSemaines.append([semaines[j], [0 for i in range(len(collabs))], "INIT"])
            elif (mois == 3 or mois == 4) and annee == 2021 and 10 <= numSem <= 14:
                consoSemaines.append([semaines[j], [0 for i in range(len(collabs))], "INIT CLN"])
            else:
                consoSemaines.append([semaines[j], [0 for i in range(len(collabs))], ""])
            datesSemEC = []
            for date in dates:
                if date.numSemaine() == numSem:
                    datesSemEC.append(date)
            datesAccess.append(datesSemEC)
        rafUpdateTot = 0
        totConso = 0
        totRAF = 0
        for i in range(len(collabs)):
            collab = collabs[i]

            assoBooster = db.session.query(AssoCollabBooster).filter(AssoCollabBooster.collab_id == collab.id_collab,
                                                                     AssoCollabBooster.booster_id == booster.id_booster).all()[
                0]
            rafsUpdate.append(assoBooster.rafUpdate)
            rafUpdateTot += assoBooster.rafUpdate
            for j in range(len(semaines)):

                jours = datesAccess[j]  # Jours de la j ème semaine
                for jour in jours:
                    imputs = db.session.query(Imputation).filter(Imputation.collab_id == collab.id_collab,
                                                                 Imputation.date_id == jour.id_date,
                                                                 Imputation.joursAllouesTache != 0,
                                                                 Imputation.type == "client").all()
                    for imput in imputs:
                        boncomm = db.session.query(Boncomm).filter(Boncomm.id_acti == imput.acti_id).all()[0]
                        if boncomm.horsProjet == "Non" or boncomm.horsProjet == "":
                            consoSemaines[j][1][i] += imput.joursAllouesTache
                            consoTot[i] += imput.joursAllouesTache
            totConso += consoTot[i]
            raf[i] = rafsUpdate[i] - consoTot[i]
            totRAF += raf[i]
        rafsUpdateTot.append(rafUpdateTot)
        dataToShow.append([rafsUpdate, consoSemaines, consoTot, raf])
        totConsoTot.append(totConso)
        rafTot.append(totRAF)

        # Calcul du cumulés sur le mois
        if mois == 2 and annee == 2021:
            cumules = [0, 0, 0]
        else:
            conso = totConsoTot[k] + cumulesMois[k - 1][0]
            ajout = rafsUpdateTot[k] - rafTot[k - 1]

            prevuConso = conso + ajout + rafTot[k]
            cumules = [conso, ajout, prevuConso]
        cumulesMois.append(cumules)
    abrevCollabs = []
    for collab in collabs:
        rafInitTot += collab.rafInit
        abrevCollabs.append(collab.abreviation())
    nbMois, nbCollabs = len(periode), len(collabs)
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    suiviSSQ.set_column_pixels('A:A', 10)
    suiviSSQ.set_row_pixels(0, 10)
    suiviSSQ.set_column_pixels('B:B', 100)
    suiviSSQ.set_column_pixels('C:C', 90)
    suiviSSQ.set_column_pixels('D:D', 80)
    suiviSSQ.set_column_pixels('E:E', 70)
    suiviSSQ.set_column_pixels('F:F', 70)
    suiviSSQ.set_column_pixels('G:G', 70)
    suiviSSQ.set_column_pixels('I:I', 70)
    suiviSSQ.set_column_pixels('J:J', 70)
    suiviSSQ.set_column_pixels('L:L', 90)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    suiviSSQ.write('B2', 'Suivi Conso. SSQ', format_titre)
    """----- En-têtes -----"""
    col = 4
    for abrev in abrevCollabs:
        suiviSSQ.write(xl_col_to_name(col) + '4', abrev, format_entete)
        col += 1

    suiviSSQ.write(xl_col_to_name(col) + '4', 'Total', format_entete)
    suiviSSQ.set_column_pixels(xl_col_to_name(col + 1) + ':' + xl_col_to_name(col + 1), 5)
    suiviSSQ.write(xl_col_to_name(col + 1) + '4', '', format_activite)
    suiviSSQ.write(xl_col_to_name(col + 2) + '4', '', format_entete)
    suiviSSQ.write(xl_col_to_name(col + 3) + '4', 'Cumulés', format_entete)
    suiviSSQ.write(xl_col_to_name(col + 4) + '4', '', format_entete)

    """----- Remplissage des données -----"""
    col = 3
    suiviSSQ.write(xl_col_to_name(col) + '5', 'RAF Init', format_entete)
    col += 1
    for collab in collabs:
        suiviSSQ.write(xl_col_to_name(col) + '5', str(collab.rafInit), format_bon)
        col += 1
    suiviSSQ.write(xl_col_to_name(col + 1) + '5', '', format_activite)
    suiviSSQ.write(xl_col_to_name(col) + '5', rafInitTot, format_bon)
    suiviSSQ.write(xl_col_to_name(col + 2) + '5', 'Conso', format_activite)
    suiviSSQ.write(xl_col_to_name(col + 3) + '5', 'Ajout', format_activite)
    suiviSSQ.write(xl_col_to_name(col + 4) + '5', 'Prévus/Conso', format_activite)

    row = 6
    for i in range(nbMois):
        col = 2
        suiviSSQ.write(xl_col_to_name(col) + str(row), str(periode[i][0]) + '/' + str(periode[i][1]), format_entete)
        col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), 'RAF Update', format_entete)
        col += 1
        for j in range(nbCollabs):
            suiviSSQ.write(xl_col_to_name(col) + str(row), dataToShow[i][0][j], format_activite)
            col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), rafsUpdateTot[i], format_entete)
        col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), '', format_activite)
        col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), '', format_bon)
        col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), cumulesMois[i][1], format_bon)
        col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), '', format_bon)
        row += 1
        for semaine in dataToShow[i][1]:
            col = 3
            suiviSSQ.write(xl_col_to_name(col) + str(row), 'S' + str(semaine[0][0]) + ' - ' + str(semaine[0][1]) + 'j',
                           format_activite)
            col += 1
            for j in range(nbCollabs):
                suiviSSQ.write(xl_col_to_name(col) + str(row), semaine[1][j], format_bon)
                col += 1
            suiviSSQ.write(xl_col_to_name(col) + str(row),
                           '=SUM(E' + str(row) + ':' + xl_col_to_name(3 + nbCollabs) + str(row) + ')',
                           format_activite)
            suiviSSQ.write(xl_col_to_name(col + 1) + str(row), '', format_activite)
            suiviSSQ.write(xl_col_to_name(col + 2) + str(row), '', format_bon)
            suiviSSQ.write(xl_col_to_name(col + 3) + str(row), '', format_bon)
            suiviSSQ.write(xl_col_to_name(col + 4) + str(row), '', format_bon)
            row += 1
        col = 3
        suiviSSQ.write(xl_col_to_name(col) + str(row), 'Conso. tot.', format_entete)
        col += 1
        for j in range(nbCollabs):
            suiviSSQ.write(xl_col_to_name(col) + str(row), dataToShow[i][2][j], format_activite)
            col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), totConsoTot[i], format_entete)
        suiviSSQ.write(xl_col_to_name(col + 1) + str(row), '', format_activite)
        suiviSSQ.write(xl_col_to_name(col + 2) + str(row), '', format_bon)
        suiviSSQ.write(xl_col_to_name(col + 3) + str(row), '', format_bon)
        suiviSSQ.write(xl_col_to_name(col + 4) + str(row), '', format_bon)
        row += 1
        col = 3
        suiviSSQ.write(xl_col_to_name(col) + str(row), 'RAF', format_entete)
        col += 1
        for j in range(nbCollabs):
            suiviSSQ.write(xl_col_to_name(col) + str(row), dataToShow[i][3][j], format_activite)
            col += 1
        suiviSSQ.write(xl_col_to_name(col) + str(row), rafTot[i], format_entete)
        suiviSSQ.write(xl_col_to_name(col + 1) + str(row), '', format_activite)
        suiviSSQ.write(xl_col_to_name(col + 2) + str(row), cumulesMois[i][0], format_bon)
        suiviSSQ.write(xl_col_to_name(col + 3) + str(row), '', format_bon)
        suiviSSQ.write(xl_col_to_name(col + 4) + str(row), cumulesMois[i][2], format_bon)
        col += 4
        row += 1
        suiviSSQ.set_row_pixels(row - 1, 5)
        for j in range(col - 2):
            suiviSSQ.write(xl_col_to_name(3 + j) + str(row), '', format_entete)
        row += 1

    """---------------------------------------------------------------------------------------------------------"""
    """--------------------------------------------- Booster conso ---------------------------------------------"""
    """ ---------- Récupération des données ---------- """
    collabs = db.session.query(Collab).all()
    moisDebut, anneeDebut = 9, 2021  # Commence en septembre
    dateNow = str(datetime.now())
    anneeFin, moisFin = int(dateNow[:4]), int(dateNow[5:7])
    if anneeDebut == anneeFin:
        periode = [[moisDebut + i, anneeDebut] for i in range(moisFin - moisDebut + 1)]
    else:
        periode = [[moisDebut + i, anneeDebut] for i in range(12 - moisDebut + 1)]
        for i in range(int(anneeFin) - int(anneeDebut) - 1):
            for j in range(12):
                periode.append([j + 1, anneeDebut + i + 1])
        for i in range(moisFin):
            periode.append([i + 1, anneeFin])

    dataToShowLeft, dataToShowRight = [], []
    nbMois, nbCollab = len(periode), len(collabs)
    for k in range(nbMois):
        mois = periode[k][0]
        annee = periode[k][1]
        dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
        dataRight, dataLeft = [], []
        """ Construction partie droite """
        rafPrecCollab = [0 for i in range(nbCollab + 1)]
        conso = [0 for i in range(nbCollab + 1)]
        raf = [0 for i in range(nbCollab + 1)]  # +1 pour avoir le total de la ligne
        ventilTot = [0 for i in range(nbCollab + 1)]
        rafUpCollab = [0 for i in range(nbCollab + 1)]

        if annee == 2021 and mois == 9:
            for j in range(nbCollab):
                collab = collabs[j]
                booster = db.session.query(Booster).filter(
                    Booster.mois == mois - 1, Booster.annee == annee).all()[0]
                asso = db.session.query(AssoCollabBooster).filter(
                    AssoCollabBooster.collab_id == collab.id_collab,
                    AssoCollabBooster.booster_id == booster.id_booster).all()[0]
                rafPrecCollab[j] = asso.rafUpdate
                rafPrecCollab[-1] += asso.rafUpdate
        else:
            for j in range(nbCollab):
                rafPrecCollab[j] = dataToShowRight[k - 1][4][j]
                rafPrecCollab[-1] = dataToShowRight[k - 1][4][-1]
        dataRight.append(rafPrecCollab)

        booster = db.session.query(Booster).filter(Booster.mois == mois, Booster.annee == annee).all()[0]
        for j in range(nbCollab):
            collab = collabs[j]
            asso = db.session.query(AssoCollabBooster).filter(
                AssoCollabBooster.collab_id == collab.id_collab,
                AssoCollabBooster.booster_id == booster.id_booster).all()[0]
            """ Ventilation """
            ventilTot[j] = asso.ventil
            ventilTot[-1] += asso.ventil

            """ Conso """
            for date in dates:
                imputs = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                             Imputation.collab_id == collab.id_collab,
                                                             Imputation.collab_id == collab.id_collab,
                                                             Imputation.type == "client").all()
                for imput in imputs:
                    boncomm = db.session.query(Boncomm).get(imput.acti_id)
                    if boncomm.horsProjet == "Non":
                        conso[j] += imput.joursAllouesTache
                        conso[-1] += imput.joursAllouesTache

            """ RAF """
            raf[j] = rafPrecCollab[j] - conso[j]

            """ RAF Update """
            rafUpCollab[j] = raf[j] + ventilTot[j]

        raf[-1] = rafPrecCollab[-1] - conso[-1]
        rafUpCollab[-1] = raf[-1] + ventilTot[-1]

        dataRight.append(conso)
        dataRight.append(raf)
        dataRight.append(ventilTot)
        dataRight.append(rafUpCollab)
        dataToShowRight.append(dataRight)
        """ Construction partie gauche """

        rafPrec, rafCalc, rafUp, rafMonte = [], [0, 0, 0], [0, 0, 0], [booster.monteR, booster.monteG,
                                                                       booster.monteR + booster.monteG]

        """ RAF -1 """
        if annee == 2021 and mois == 9:
            rafPrec.append(0)
            rafPrec.append(101.5)
            rafPrec.append(101.5)
        else:
            rafPrec.append(dataToShowLeft[k - 1][4][0])
            rafPrec.append(dataToShowLeft[k - 1][4][1])
            rafPrec.append(dataToShowLeft[k - 1][4][2])
        dataLeft.append(rafPrec)

        """ Ventilation """
        ventilation = [0, ventilTot[-1], ventilTot[-1]]

        """ RAF Calc"""
        rafCalc[0] = rafPrec[0] - ventilation[0]
        rafCalc[1] = rafPrec[1] - ventilation[1]
        rafCalc[2] = rafPrec[2] - ventilation[2]

        """ RAF Update """
        rafUp[0] = rafMonte[0] + rafCalc[0]
        rafUp[1] = rafMonte[1] + rafCalc[1]
        rafUp[2] = rafUp[0] + rafUp[1]

        dataLeft.append(ventilation)
        dataLeft.append(rafCalc)
        dataLeft.append(rafMonte)
        dataLeft.append(rafUp)
        dataLeft.append(booster.com)
        dataToShowLeft.append(dataLeft)

    abrevCollabs = []
    for collab in collabs:
        abrevCollabs.append(collab.abreviation())

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    boosterConso.set_column_pixels('A:A', 10)
    boosterConso.set_row_pixels(0, 10)
    boosterConso.set_column_pixels('B:B', 100)
    boosterConso.set_column_pixels('C:C', 90)
    boosterConso.set_column_pixels('D:D', 80)
    boosterConso.set_column_pixels('E:E', 90)
    boosterConso.set_column_pixels('F:F', 70)
    boosterConso.set_column_pixels('G:G', 250)
    boosterConso.set_column_pixels('I:I', 90)
    boosterConso.set_column_pixels('H:H', 15)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    boosterConso.write('B2', 'Suivi Booster conso', format_titre)
    """----- En-têtes -----"""
    boosterConso.merge_range(3, 3, 3, 4, 'OTP F3.RAF', format_entete)
    boosterConso.write('J5', 'Répartis', format_entete)
    col = 10
    for abrev in abrevCollabs:
        boosterConso.write(xl_col_to_name(col) + '5', abrev, format_entete)
        col += 1

    boosterConso.write('D5', 'Réserve', format_activite)
    boosterConso.write('E5', 'Génériques', format_activite)
    boosterConso.write('F5', 'Total', format_entete)
    boosterConso.write('G5', 'Commentaire', format_entete)
    boosterConso.write('H5', '', format_bon)

    """----- Remplissage des données -----"""

    row = 6
    for k in range(nbMois):
        col = 1
        boosterConso.merge_range(row - 1, 6, row + 3, 6, dataToShowLeft[k][5], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row), str(periode[k][0]) + '/' + str(periode[k][1]), format_entete)
        col += 1
        boosterConso.write(xl_col_to_name(col) + str(row), 'RAF - 1', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 1), 'Ventilation', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 2), 'RAF calc.', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 3), 'RAF Monté', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 4), 'RAF Update', format_entete)
        col += 1
        boosterConso.write(xl_col_to_name(col) + str(row), dataToShowLeft[k][0][0], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 1), dataToShowLeft[k][1][0], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 2), dataToShowLeft[k][2][0], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 3), dataToShowLeft[k][3][0], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 4), dataToShowLeft[k][4][0], format_bon)
        col += 1
        boosterConso.write(xl_col_to_name(col) + str(row), dataToShowLeft[k][0][1], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 1), dataToShowLeft[k][1][1], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 2), dataToShowLeft[k][2][1], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 3), dataToShowLeft[k][3][1], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 4), dataToShowLeft[k][4][1], format_bon)
        col += 1
        boosterConso.write(xl_col_to_name(col) + str(row), dataToShowLeft[k][0][2], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 1), dataToShowLeft[k][1][2], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 2), dataToShowLeft[k][2][2], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 3), dataToShowLeft[k][3][2], format_bon)
        boosterConso.write(xl_col_to_name(col) + str(row + 4), dataToShowLeft[k][4][2], format_bon)
        col += 1
        boosterConso.write('H' + str(row), '', format_bon)
        boosterConso.write('H' + str(row + 1), '', format_bon)
        boosterConso.write('H' + str(row + 2), '', format_bon)
        boosterConso.write('H' + str(row + 3), '', format_bon)
        boosterConso.write('H' + str(row + 4), '', format_bon)
        col += 2
        boosterConso.write(xl_col_to_name(col) + str(row), 'RAF - 1', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 1), 'Conso.', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 2), 'RAF', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 3), 'Ventil.', format_entete)
        boosterConso.write(xl_col_to_name(col) + str(row + 4), 'RAF Update', format_entete)
        boosterConso.write(xl_col_to_name(col + 1) + str(row), dataToShowRight[k][0][-1], format_activite)
        boosterConso.write(xl_col_to_name(col + 1) + str(row + 1), dataToShowRight[k][1][-1], format_activite)
        boosterConso.write(xl_col_to_name(col + 1) + str(row + 2), dataToShowRight[k][2][-1], format_activite)
        boosterConso.write(xl_col_to_name(col + 1) + str(row + 3), dataToShowRight[k][3][-1], format_activite)
        boosterConso.write(xl_col_to_name(col + 1) + str(row + 4), dataToShowRight[k][4][-1], format_activite)
        col += 2
        for j in range(nbCollab):
            boosterConso.write(xl_col_to_name(col) + str(row), dataToShowRight[k][0][j], format_bon)
            boosterConso.write(xl_col_to_name(col) + str(row + 1), dataToShowRight[k][1][j], format_bon)
            boosterConso.write(xl_col_to_name(col) + str(row + 2), dataToShowRight[k][2][j], format_bon)
            boosterConso.write(xl_col_to_name(col) + str(row + 3), dataToShowRight[k][3][j], format_bon)
            boosterConso.write(xl_col_to_name(col) + str(row + 4), dataToShowRight[k][4][j], format_bon)
            col += 1
        row += 5
        boosterConso.set_row_pixels(row - 1, 5)
        for i in range(8 + nbCollabs):
            boosterConso.write(xl_col_to_name(2 + i) + str(row), '', format_entete)
        row += 1

    """--------------------------------------------------------------------------------------------------------------"""
    workbook.close()
    return None
