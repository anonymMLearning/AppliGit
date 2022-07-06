import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from MyApp.models import *
from datetime import datetime
from flask import Flask, request


def export_excel_prod_annuelle():
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    das = request.form['das']
    anneeToShow = request.form['annee']

    workbook = xlsxwriter.Workbook(
        r'C:\Users\a' + das + '\Downloads\Production Année ' + str(annee) + '.xlsx')
    sheetScr = workbook.add_worksheet('SCR')
    sheetScr.set_tab_color('#305496')
    prodAnReel = workbook.add_worksheet('Prod. annuelle réelle')
    prodAnReel.set_tab_color('#305496')
    prodAnValide = workbook.add_worksheet('Prod. annuelle validée')
    prodAnValide.set_tab_color('#305496')

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
    """---------------------------------------------- Feuille SCR ---------------------------------------------------"""
    anneeDebut = 2021
    anneesToShow = []
    for i in range(int(anneeToShow) - int(anneeDebut) + 1):
        anneesToShow.append(int(anneeDebut) + i)
    nbAnnees = len(anneesToShow)
    scrs = db.session.query(SCR).all()
    collabs = db.session.query(Collab).all()
    # Données globales sur l'année :
    joursTot, coutTot = [0 for i in range(nbAnnees)], [0 for i in range(nbAnnees)]
    scrMoyenCalc, scrMoyenArrondi, scrMoyenRetenu = [0 for i in range(nbAnnees)], [0 for i in range(nbAnnees)], []
    for i in range(nbAnnees):
        scrMoyenRetenu.append(db.session.query(Date).filter(Date.annee == int(anneeDebut) + i).all()[0].scrMoyRetenu)

    # Données des collaborateurs pour le 2ème tableau de la page :
    dataCollabsTableau2 = []
    for collab in collabs:
        gcm = db.session.query(Gcm).get(collab.gcm_id)
        data = [collab, collab.abreviation(), gcm, ["" for i in range(nbAnnees)]]
        for i in range(nbAnnees):
            annee = int(anneeDebut) + i
            assos = db.session.query(AssoCollabSCR).filter(AssoCollabSCR.collab_id == collab.id_collab,
                                                           AssoCollabSCR.annee == annee).all()
            if assos:
                # On va prendre le SCR en cours pour les différents calculs, dans le cas de 2 SCR sur une même année
                posSCR = 0
                diff = 12  # Initialisation. L'écart entre les mois ne peut pas être plus grand
                for j in range(len(assos)):
                    if assos[j].moisDebut != "":
                        if int(dateNow[5:7]) >= assos[j].moisDebut:  # A l'inverse, le moisD n'est pas encore arrivé
                            if diff >= int(dateNow[5:7]) - assos[j].moisDebut:
                                diff = int(dateNow[5:7]) - assos[j].moisDebut
                                posSCR = j
                joursTot[i] += assos[posSCR].scr.ponderation
                coutTot[i] += assos[posSCR].scr.cout * assos[posSCR].scr.ponderation
                data[3][i] = assos[posSCR].scr
        dataCollabsTableau2.append(data)
    for i in range(nbAnnees):
        if joursTot[i] != 0:
            if joursTot[i] != 0:
                scrMoyenCalc[i] = round(coutTot[i] / joursTot[i], 2)
                scrMoyenArrondi[i] = round(scrMoyenCalc[i])
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    sheetScr.set_column_pixels('A:A', 10)
    sheetScr.set_row_pixels(0, 10)
    sheetScr.set_column_pixels('B:B', 80)
    sheetScr.set_column_pixels('C:C', 80)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    sheetScr.write('B2', 'SCR collaborateurs MS4', format_titre)
    "----- En-têtes -----"
    col = 2
    for i in range(nbAnnees):
        sheetScr.merge_range(3, col, 3, col + 2, anneesToShow[i], format_entete)
        sheetScr.write(xl_col_to_name(col) + '5', 'GCM', format_activite)
        sheetScr.write(xl_col_to_name(col + 1) + '5', 'Coût', format_activite)
        sheetScr.set_column_pixels(xl_col_to_name(col + 2) + ':' + xl_col_to_name(col + 2), 90)
        sheetScr.write(xl_col_to_name(col + 2) + '5', 'Pondération', format_activite)
        sheetScr.set_column_pixels(xl_col_to_name(col + 3) + ':' + xl_col_to_name(col + 3), 5)
        sheetScr.write(xl_col_to_name(col + 3) + '5', '', format_entete)
        col += 4

    row = 6
    for collab in dataCollabsTableau2:
        sheetScr.write('B' + str(row), collab[1], format_entete)
        col = 2
        for i in range(nbAnnees):
            sheetScr.write(xl_col_to_name(col) + str(row), collab[2].code, format_bon)
            sheetScr.write(xl_col_to_name(col + 1) + str(row), collab[3][i].cout, format_bon)
            sheetScr.write(xl_col_to_name(col + 2) + str(row), collab[3][i].ponderation, format_bon)
            sheetScr.write(xl_col_to_name(col + 3) + str(row), '', format_entete)
            col += 4
        row += 1

    sheetScr.write('B' + str(row), '', format_entete)
    col = 2
    sheetScr.set_row_pixels(row - 1, 5)
    for i in range(nbAnnees):
        sheetScr.write(xl_col_to_name(col) + str(row), '', format_entete)
        sheetScr.write(xl_col_to_name(col + 1) + str(row), '', format_entete)
        sheetScr.write(xl_col_to_name(col + 2) + str(row), '', format_entete)
        sheetScr.write(xl_col_to_name(col + 3) + str(row), '', format_entete)
        col += 4
    row += 1

    sheetScr.write('B' + str(row), '', format_entete)
    col = 2
    for i in range(nbAnnees):
        sheetScr.write(xl_col_to_name(col) + str(row), 'Total ', format_activite)
        sheetScr.write(xl_col_to_name(col + 1) + str(row), coutTot[i], format_bon)
        sheetScr.write(xl_col_to_name(col + 2) + str(row), joursTot[i], format_bon)
        sheetScr.write(xl_col_to_name(col + 3) + str(row), '', format_entete)
        col += 4
    row += 1

    sheetScr.write('B' + str(row), 'SCR Moyen', format_entete)
    col = 2
    for i in range(nbAnnees):
        sheetScr.write(xl_col_to_name(col) + str(row), 'Calculé', format_activite)
        sheetScr.write(xl_col_to_name(col + 1) + str(row), 'Arrondi', format_activite)
        sheetScr.write(xl_col_to_name(col + 2) + str(row), 'Retenu', format_activite)
        sheetScr.write(xl_col_to_name(col + 3) + str(row), '', format_entete)
        col += 4
    row += 1

    sheetScr.write('B' + str(row), '', format_entete)
    col = 2
    for i in range(nbAnnees):
        sheetScr.write(xl_col_to_name(col) + str(row), scrMoyenCalc[i], format_bon)
        sheetScr.write(xl_col_to_name(col + 1) + str(row), scrMoyenArrondi[i], format_bon)
        sheetScr.write(xl_col_to_name(col + 2) + str(row), scrMoyenRetenu[i], format_bon)
        sheetScr.write(xl_col_to_name(col + 3) + str(row), '', format_entete)
        col += 4
    row += 1

    sheetScr.write('B' + str(row), '', format_entete)
    col = 2
    sheetScr.set_row_pixels(row - 1, 5)
    for i in range(nbAnnees):
        sheetScr.write(xl_col_to_name(col) + str(row), '', format_entete)
        sheetScr.write(xl_col_to_name(col + 1) + str(row), '', format_entete)
        sheetScr.write(xl_col_to_name(col + 2) + str(row), '', format_entete)
        sheetScr.write(xl_col_to_name(col + 3) + str(row), '', format_entete)
        col += 4
    row += 1
    """---------------------------------------------- Feuille Prod annuelle -----------------------------------------"""
    """ ---------- Récupération des données ---------- """
    prodInitValide = db.session.query(Prod).filter(Prod.annee == 2021, Prod.type == "valide", Prod.mois == 2).all()[0]
    prodInitReel = db.session.query(Prod).filter(Prod.annee == 2021, Prod.type == "reel", Prod.mois == 2).all()[0]
    prodsValidees = db.session.query(Prod).filter(Prod.annee == anneeToShow, Prod.type == "valide").all()
    prodsReelles = db.session.query(Prod).filter(Prod.annee == anneeToShow, Prod.type == "reel").all()
    dataDate = db.session.query(Date).filter(Date.annee == anneeToShow, Date.jour == 1).all()
    dataProdValide, dataProdReel = [], []
    for i in range(12):
        if int(anneeToShow) == 2021 and i == 0:
            dataValide, dataReel = [prodsValidees[i], 0, 0, 0, 0, 0], [prodsReelles[i], 0, 0, 0, 0, 0]
        else:
            dataValide, dataReel = [prodsValidees[i]], [prodsReelles[i]]

            # Budget :
            if int(anneeToShow) == 2021 and (i == 0 or i == 1):
                budgetValide = 0
                budgetReel = 0
            else:
                if prodsValidees[i].jourMoisDP != 0:
                    budgetValide = dataDate[i].equipe * dataDate[i].tjm * prodsValidees[i].jourMoisTeam + dataDate[
                        i].tjm * prodsValidees[i].jourMoisDP
                else:
                    budgetValide = 0
                if int(anneeToShow) == 2021 and i == 2:
                    budgetReel = 25000
                else:
                    if prodsReelles[i].jourMoisDP != 0:
                        budgetReel = dataDate[i].equipe * dataDate[i].tjm * prodsReelles[i].jourMoisTeam + dataDate[
                            i].tjm * \
                                     prodsReelles[i].jourMoisDP
                    else:
                        budgetReel = 0
            dataValide.append(budgetValide)
            dataReel.append(budgetReel)

            # Coût total :
            coutTotValide = prodsValidees[i].coutDP + prodsValidees[i].coutTeam
            coutTotReel = prodsReelles[i].coutDP + prodsReelles[i].coutTeam
            dataValide.append(coutTotValide)
            dataReel.append(coutTotReel)

            # Amortissement :
            """ Amortissement """
            if int(anneeToShow) == 2021 and (i == 0 or i == 1):
                amortValide = 0
                amortReel = 0
            else:
                if prodsValidees[i].amort != 0:
                    amortValide = round((prodInitValide.coutDP + prodInitValide.coutTeam) / prodsValidees[i].amort, 2)
                else:
                    amortValide = 0
                if prodsReelles[i].amort != 0:
                    amortReel = round((prodInitReel.coutDP + prodInitReel.coutTeam) / prodsReelles[i].amort, 2)
                else:
                    amortReel = 0
            dataValide.append(amortValide)
            dataReel.append(amortReel)
            """ Reste à amortir """  # Amortissement mensuel tjs le même
            if int(anneeToShow) == 2021:
                if i == 0:  # Mois de janvier
                    rAAValide = 0  # rAA : reste à amortir
                    rAAReel = 0
                elif i == 1:  # Mois de février
                    rAAReel = 0
                    rAAValide = 0
                else:
                    rAAValide = round(prodInitValide.coutDP + prodInitValide.coutTeam - amortValide * (i - 1), 2)
                    rAAReel = round(prodInitReel.coutDP + prodInitReel.coutTeam - amortReel * (i - 1), 2)
            # Pour les autres années
            else:
                rAAValide = round(prodInitValide.coutDP + prodInitValide.coutTeam - amortValide * (
                        10 + 12 * (int(anneeToShow) - 2022) + i + 1), 2)
                rAAReel = round(prodInitReel.coutDP + prodInitReel.coutTeam - amortReel * (
                        10 + 12 * (int(anneeToShow) - 2022) + i + 1), 2)
                # 10 : Tous les mois de 2021
                # 12 * (anneeToShow - 2021 + 1) : nombre d'années complète entre 2021 et anneeToShow
                # i - 1 : Nombre de mois passés sur l'année en cours
            dataValide.append(rAAValide)
            dataReel.append(rAAReel)

            # Marge:
            margeValide = round(budgetValide - coutTotValide - amortValide, 2)
            margeReel = round(budgetReel - coutTotReel - amortReel, 2)
            dataValide.append(margeValide)
            dataReel.append(margeReel)

            # Pourcentage marge :
            if budgetValide != 0:
                margePourcentValide = round(100 * (budgetValide - (coutTotValide + amortValide)) / budgetValide, 2)
            else:
                margePourcentValide = 0
            if budgetReel != 0:
                margePourcentReel = round(100 * (budgetReel - (coutTotReel + amortReel)) / budgetReel, 2)
            else:
                margePourcentReel = 0
            dataValide.append(margePourcentValide)
            dataReel.append(margePourcentReel)
        dataProdValide.append(dataValide)
        dataProdReel.append(dataReel)
    collabs = db.session.query(Collab).all()
    """ ---------- Tableau réel ---------- """
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    prodAnReel.set_column_pixels('A:A', 10)
    prodAnReel.set_row_pixels(0, 10)
    prodAnReel.set_column_pixels('B:B', 90)
    prodAnReel.set_column_pixels('C:C', 150)
    prodAnReel.set_column_pixels('D:D', 90)
    prodAnReel.set_column_pixels('E:E', 90)
    prodAnReel.set_column_pixels('F:F', 90)
    prodAnReel.set_column_pixels('G:G', 90)
    prodAnReel.set_column_pixels('H:H', 90)
    prodAnReel.set_column_pixels('I:I', 90)
    prodAnReel.set_column_pixels('J:J', 90)
    prodAnReel.set_column_pixels('K:K', 90)
    prodAnReel.set_column_pixels('L:L', 90)
    prodAnReel.set_column_pixels('M:M', 90)
    prodAnReel.set_column_pixels('N:N', 90)
    prodAnReel.set_column_pixels('O:O', 90)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    prodAnReel.write('B2', 'Production annuelle réelle', format_titre)
    "----- En-têtes -----"
    prodAnReel.merge_range(3, 3, 3, 14, str(dataDate[0].annee), format_entete)
    row = 5
    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Tableau réel', format_entete)
    col += 1
    for date in dataDate:
        prodAnReel.write(xl_col_to_name(col) + str(row), stringMois(str(date.mois)), format_entete)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Équipe', format_entete)
    col += 1
    for date in dataDate:
        prodAnReel.write(xl_col_to_name(col) + str(row), str(date.equipe), format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'TJM', format_entete)
    col += 1
    for date in dataDate:
        prodAnReel.write(xl_col_to_name(col) + str(row), str(date.tjm), format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.set_row_pixels(row - 1, 5)
    prodAnReel.write(xl_col_to_name(col) + str(row), '', format_entete)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), '', format_entete)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Budget', format_activite)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][1], format_activite)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Coût DP', format_activite)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][0].coutDP, format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Coût Team', format_activite)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][0].coutTeam, format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Coût total', format_activite)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][2], format_activite)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Amortissement', format_activite)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][3], format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'RAA', format_activite)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][4], format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Coût tot. + février 2021', format_entete)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][3] + dataProdValide[i][2], format_activite)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Marge', format_entete)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), dataProdValide[i][5], format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.write(xl_col_to_name(col) + str(row), 'Marge en %', format_entete)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), str(dataProdValide[i][6]) + ' %', format_bon)
        col += 1
    row += 1

    col = 2
    prodAnReel.set_row_pixels(row - 1, 5)
    prodAnReel.write(xl_col_to_name(col) + str(row), '', format_entete)
    col += 1
    for i in range(12):
        prodAnReel.write(xl_col_to_name(col) + str(row), '', format_entete)
        col += 1
    row += 1

    """ ---------- Tableau validé ---------- """
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    prodAnValide.set_column_pixels('A:A', 10)
    prodAnValide.set_row_pixels(0, 10)
    prodAnValide.set_column_pixels('B:B', 90)
    prodAnValide.set_column_pixels('C:C', 150)
    prodAnValide.set_column_pixels('D:D', 90)
    prodAnValide.set_column_pixels('E:E', 90)
    prodAnValide.set_column_pixels('F:F', 90)
    prodAnValide.set_column_pixels('G:G', 90)
    prodAnValide.set_column_pixels('H:H', 90)
    prodAnValide.set_column_pixels('I:I', 90)
    prodAnValide.set_column_pixels('J:J', 90)
    prodAnValide.set_column_pixels('K:K', 90)
    prodAnValide.set_column_pixels('L:L', 90)
    prodAnValide.set_column_pixels('M:M', 90)
    prodAnValide.set_column_pixels('N:N', 90)
    prodAnValide.set_column_pixels('O:O', 90)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    prodAnValide.write('B2', 'Production annuelle validée', format_titre)
    "----- En-têtes -----"
    prodAnValide.merge_range(3, 3, 3, 14, str(dataDate[0].annee), format_entete)
    row = 5
    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Tableau validé', format_entete)
    col += 1
    for date in dataDate:
        prodAnValide.write(xl_col_to_name(col) + str(row), stringMois(str(date.mois)), format_entete)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Équipe', format_entete)
    col += 1
    for date in dataDate:
        prodAnValide.write(xl_col_to_name(col) + str(row), str(date.equipe), format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'TJM', format_entete)
    col += 1
    for date in dataDate:
        prodAnValide.write(xl_col_to_name(col) + str(row), str(date.tjm), format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.set_row_pixels(row - 1, 5)
    prodAnValide.write(xl_col_to_name(col) + str(row), '', format_entete)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), '', format_entete)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Budget', format_activite)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][1], format_activite)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Coût DP', format_activite)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][0].coutDP, format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Coût Team', format_activite)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][0].coutTeam, format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Coût total', format_activite)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][2], format_activite)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Amortissement', format_activite)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][3], format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'RAA', format_activite)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][4], format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Coût tot. + février 2021', format_entete)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][3] + dataProdReel[i][2], format_activite)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Marge', format_entete)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), dataProdReel[i][5], format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.write(xl_col_to_name(col) + str(row), 'Marge en %', format_entete)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), str(dataProdReel[i][6]) + ' %', format_bon)
        col += 1
    row += 1

    col = 2
    prodAnValide.set_row_pixels(row - 1, 5)
    prodAnValide.write(xl_col_to_name(col) + str(row), '', format_entete)
    col += 1
    for i in range(12):
        prodAnValide.write(xl_col_to_name(col) + str(row), '', format_entete)
        col += 1
    row += 1
    """---------------------------------------------------------------------------------------------------------------"""
    workbook.close()
    return None
