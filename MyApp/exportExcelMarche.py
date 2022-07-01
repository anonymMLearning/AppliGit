import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from MyApp.models import *
from datetime import datetime
from flask import Flask, request


def export_excel_marcheMS4():
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    das = request.form['das']
    workbook = xlsxwriter.Workbook(
        r'C:\Users\a' + das + '\Downloads\MarchéMS4-' + str(mois) + '-' + str(annee) + '.xlsx')
    chronoBC = workbook.add_worksheet('chrono des BC')
    chronoBC.set_tab_color('#305496')
    chronoFD = workbook.add_worksheet('chrono des FD')
    chronoFD.set_tab_color('#305496')
    pdc = workbook.add_worksheet('PdC')
    pdc.set_tab_color('#305496')
    cra = workbook.add_worksheet('CRA Marché')
    cra.set_tab_color('#305496')
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

    """ -------------------------------------- Feuille chronoBC ---------------------------------------------------- """
    bons = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Prod").all()
    uos = db.session.query(UO).all()
    dateNow = str(datetime.now())
    moisStr = stringMois(str(int(dateNow[5:7])))
    annee = int(dateNow[:4])

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    chronoBC.set_column_pixels('A:A', 10)
    chronoBC.set_row_pixels(0, 10)
    chronoBC.set_column_pixels('D:D', 300)
    chronoBC.set_column_pixels('F:F', 72)
    chronoBC.set_column_pixels('G:G', 85)
    chronoBC.set_column_pixels('I:I', 80)
    chronoBC.set_column_pixels('J:J', 80)
    chronoBC.set_column_pixels('K:K', 80)
    chronoBC.set_column_pixels('L:L', 80)
    chronoBC.set_column_pixels('M:M', 80)

    """ ---------- Création des lignes ---------- """

    """----- Titre feuille -----"""
    chronoBC.write('B2', 'Chrono des bons de commande', format_titre)
    chronoBC.write('H2', moisStr + " " + str(annee), format_font_rouge)

    "----- En-têtes -----"
    chronoBC.write('B4', 'Projet', format_entete)
    chronoBC.write('C4', 'BC', format_entete)
    chronoBC.write('D4', 'Activité', format_entete)
    chronoBC.write('E4', 'Poste', format_entete)
    chronoBC.write('F4', 'Notif', format_entete)
    chronoBC.write('G4', 'Part ATOS', format_entete)
    chronoBC.write('H4', 'Part EGIS', format_entete)
    chronoBC.write('I4', 'Total', format_entete)
    chronoBC.write('J4', 'Date notif', format_entete)
    chronoBC.write('K4', 'Date début', format_entete)
    chronoBC.write('L4', 'Délais', format_entete)
    chronoBC.write('M4', 'Date fin', format_entete)
    chronoBC.write('N4', 'Fact', format_entete)
    chronoBC.write('P4', 'Total', format_bon)
    col = 16
    for uo in uos:
        chronoBC.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 60)
        chronoBC.write(xl_col_to_name(col) + '4', uo.num, format_entete)
        col += 1

    """----- Bons de commande -----"""
    row = 5
    for bon in bons:
        assos = bon.uos
        chronoBC.write('B' + str(row), bon.projet, format_bon)
        chronoBC.write('C' + str(row), bon.num, format_bon)
        chronoBC.write('D' + str(row), bon.activite, format_bon)
        chronoBC.write('E' + str(row), bon.poste, format_bon)
        chronoBC.write('F' + str(row), bon.notification, format_bon)
        chronoBC.write('G' + str(row), bon.caAtos, format_bon)
        chronoBC.write('H' + str(row), bon.partEGIS, format_bon)
        chronoBC.write('I' + str(row), bon.montantHT, format_bon)
        chronoBC.write('J' + str(row), bon.dateNotif, format_bon)
        chronoBC.write('K' + str(row), bon.dateDebut, format_bon)
        chronoBC.write('L' + str(row), bon.delais, format_bon)
        chronoBC.write('M' + str(row), bon.dateFinOp, format_bon)
        chronoBC.write('N' + str(row), bon.facturation, format_bon)
        col = 16
        total = 0
        for asso in assos:
            total += asso.facteur * asso.uo.prix
            chronoBC.write(xl_col_to_name(col) + str(row), asso.facteur, format_bon)
            col += 1
        if total == bon.montantHT:
            chronoBC.write('P' + str(row), total, format_activite)
        else:
            chronoBC.write('P' + str(row), total, format_rouge)
        row += 1
    """--------------------------------------------------------------------------------------------------------------"""
    """ -------------------------------------- Feuille chronoFD ---------------------------------------------------- """
    bons = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Fd", Boncomm.apm =="").all()
    uosFD = db.session.query(UO).filter(UO.type == "Fd").all()
    dateNow = str(datetime.now())
    moisStr = stringMois(str(int(dateNow[5:7])))
    annee = int(dateNow[:4])

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    chronoFD.set_column_pixels('A:A', 10)
    chronoFD.set_row_pixels(0, 10)
    chronoFD.set_column_pixels('D:D', 300)
    chronoFD.set_column_pixels('F:F', 72)
    chronoFD.set_column_pixels('G:G', 85)
    chronoFD.set_column_pixels('I:I', 80)
    chronoFD.set_column_pixels('J:J', 80)
    chronoFD.set_column_pixels('K:K', 80)
    chronoFD.set_column_pixels('L:L', 80)
    chronoFD.set_column_pixels('M:M', 80)

    """ ---------- Création des lignes ---------- """

    """----- Titre feuille -----"""
    chronoFD.write('B2', 'Chrono des frais de déplacement', format_titre)
    chronoFD.write('H2', moisStr + " " + str(annee), format_font_rouge)

    "----- En-têtes -----"
    chronoFD.write('B4', 'Projet', format_entete)
    chronoFD.write('C4', 'BC', format_entete)
    chronoFD.write('D4', 'Activité', format_entete)
    chronoFD.write('E4', 'Poste', format_entete)
    chronoFD.write('F4', 'Notif', format_entete)
    chronoFD.write('G4', 'Part ATOS', format_entete)
    chronoFD.write('H4', 'Part EGIS', format_entete)
    chronoFD.write('I4', 'Total', format_entete)
    chronoFD.write('J4', 'Date notif', format_entete)
    chronoFD.write('K4', 'Date début', format_entete)
    chronoFD.write('L4', 'Délais', format_entete)
    chronoFD.write('M4', 'Date fin', format_entete)
    chronoFD.write('N4', 'Fact', format_entete)
    chronoFD.write('P4', 'Total', format_bon)
    col = 16
    for uo in uosFD:
        chronoFD.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 60)
        chronoFD.write(xl_col_to_name(col) + '4', uo.num, format_entete)
        col += 1

    """----- Bons de commande -----"""
    row = 5
    for bon in bons:
        assos = bon.uos
        chronoFD.write('B' + str(row), bon.projet, format_bon)
        chronoFD.write('C' + str(row), bon.num, format_bon)
        chronoFD.write('D' + str(row), bon.activite, format_bon)
        chronoFD.write('E' + str(row), bon.poste, format_bon)
        chronoFD.write('F' + str(row), bon.notification, format_bon)
        chronoFD.write('G' + str(row), bon.caAtos, format_bon)
        chronoFD.write('H' + str(row), bon.partEGIS, format_bon)
        chronoFD.write('I' + str(row), bon.montantHT, format_bon)
        chronoFD.write('J' + str(row), bon.dateNotif, format_bon)
        chronoFD.write('K' + str(row), bon.dateDebut, format_bon)
        chronoFD.write('L' + str(row), bon.delais, format_bon)
        chronoFD.write('M' + str(row), bon.dateFinOp, format_bon)
        chronoFD.write('N' + str(row), bon.facturation, format_bon)
        col = 16
        total = 0
        for asso in assos:
            if asso.uo.type == "Fd":
                total += asso.facteur * asso.uo.prix
                chronoFD.write(xl_col_to_name(col) + str(row), asso.facteur, format_bon)
                col += 1
        if total == bon.montantHT:
            chronoFD.write('P' + str(row), total, format_activite)
        else:
            chronoFD.write('P' + str(row), total, format_rouge)
        row += 1
    """--------------------------------------------------------------------------------------------------------------"""
    """ -------------------------------------- Feuille PdC ---------------------------------------------------- """
    moisDebut, anneeDebut = request.form['moisD'], request.form['anneeD']
    moisFin, anneeFin = request.form['moisF'], request.form['anneeF']
    if anneeDebut == anneeFin:
        moisToShow = [[int(moisDebut) + i, anneeDebut] for i in range(int(moisFin) - int(moisDebut) + 1)]
    else:
        moisToShow = [[int(moisDebut) + i, anneeDebut] for i in range(12 - int(moisDebut) + 1)]
        for i in range(int(anneeFin) - int(anneeDebut) - 1):
            for j in range(12):
                moisToShow.append([j + 1, int(anneeDebut) + i + 1])
        for j in range(int(moisFin)):
            moisToShow.append([j + 1, anneeFin])
    budgetTotJours = 0
    nbMois = len(moisToShow)
    dataTotMois = [[0.0, 0.0, 0.0] for i in range(nbMois)]
    boncomms = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Prod").all()
    projets = []  # Contiendra tous les différents projets en cours
    for boncomm in boncomms:
        projet = boncomm.projet
        if projet not in projets:
            projets.append(projet)
    data = []
    for projet in projets:
        if projet == "APP":
            collabs = collabsProjet(projet)
            bonsProjet = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Prod", Boncomm.projet == projet).all()
            budgetTotAtos = 0
            budgetTotEgis = 0
            for bon in bonsProjet:
                budgetTotAtos += bon.caAtos
                budgetTotEgis += bon.partEGIS
                budgetTotJours += bon.caAtos + bon.partEGIS
            dataProjetAtos = [budgetTotAtos, projet + " Atos"]
            dataProjetEgis = [budgetTotEgis, projet + " EGIS"]

            for collab in collabs:
                if collab.entreprise == "Atos":
                    dataCollab = [collab, []]
                    conso = 0
                    joursAlloues = 0
                    assos = collab.boncomms
                    for asso in assos:
                        boncomm = asso.boncomm
                        if boncomm.projet == projet:
                            joursAlloues += asso.joursAllouesBC
                            for i in range(nbMois):
                                mois = moisToShow[i]
                                consoMois = 0
                                dates = db.session.query(Date).filter(Date.mois == mois[0], Date.annee == mois[1]).all()
                                for date in dates:
                                    imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                                              Imputation.collab_id == collab.id_collab,
                                                                              Imputation.acti_id == boncomm.id_acti, ).all()
                                    consoMois += imp[0].joursAllouesTache
                                conso += consoMois
                                dataTotMois[i][0] += float(consoMois)
                                dataCollab[1].append(float(consoMois))
                elif collab.entreprise == "EGIS":
                    dataCollab = [collab, []]
                    conso = 0
                    joursAlloues = 0
                    assos = collab.boncomms
                    for asso in assos:
                        boncomm = asso.boncomm
                        if boncomm.projet == projet and boncomm.prodGdpOuFd == "Prod":
                            joursAlloues += asso.joursAllouesBC
                            for i in range(nbMois):
                                mois = moisToShow[i]
                                consoMois = 0
                                dates = db.session.query(Date).filter(Date.mois == mois[0], Date.annee == mois[1]).all()
                                for date in dates:
                                    imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                                              Imputation.collab_id == collab.id_collab,
                                                                              Imputation.acti_id == boncomm.id_acti, ).all()
                                    consoMois += imp[0].joursAllouesTache
                                conso += consoMois
                                dataTotMois[i][0] += float(consoMois)
                                dataCollab[1].append(float(consoMois))
                if joursAlloues != 0:
                    raf = joursAlloues - conso
                    dataCollab.append(joursAlloues)
                    dataCollab.append(raf)
                    if collab.entreprise == "Atos":
                        dataProjetAtos.append(dataCollab)
                    elif collab.entreprise == "EGIS":
                        dataProjetEgis.append(dataCollab)
            data.append(dataProjetAtos)
            data.append(dataProjetEgis)

        else:
            collabs = collabsProjet(projet)
            bonsProjet = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Prod", Boncomm.projet == projet).all()
            budgetTot = 0
            for bon in bonsProjet:
                budgetTot += bon.caAtos
                budgetTotJours += bon.caAtos
            dataProjet = [budgetTot, projet]

            for collab in collabs:
                dataCollab = [collab, [0 for i in range(nbMois)]]
                conso = 0
                joursAlloues = 0
                assos = collab.boncomms
                for asso in assos:
                    boncomm = asso.boncomm
                    if boncomm.projet == projet and boncomm.prodGdpOuFd == "Prod":
                        joursAlloues += asso.joursAllouesBC
                        for i in range(nbMois):
                            mois = moisToShow[i]
                            consoMois = 0
                            dates = db.session.query(Date).filter(Date.mois == mois[0], Date.annee == mois[1]).all()
                            for date in dates:
                                imp = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                                          Imputation.collab_id == collab.id_collab,
                                                                          Imputation.acti_id == boncomm.id_acti, ).all()
                                consoMois += imp[0].joursAllouesTache
                            conso += consoMois
                            dataTotMois[i][0] += float(consoMois)
                            dataCollab[1][i] += float(consoMois)
                if joursAlloues != 0:
                    raf = joursAlloues - conso
                    dataCollab.append(joursAlloues)
                    dataCollab.append(raf)
                    dataProjet.append(dataCollab)
            data.append(dataProjet)
    budgetTotJours = budgetTotJours / 500
    if budgetTotJours != 0:
        dataTotMois[0][1] = round(100 * dataTotMois[0][0] / budgetTotJours, 1)
    else:
        dataTotMois[0][1] = 0
    dataTotMois[0][2] = round(dataTotMois[0][0] / 18, 2)
    for i in range(nbMois - 1):
        dataTotMois[i + 1][2] = round(dataTotMois[i + 1][0] / 18, 2)
        if budgetTotJours != 0:
            dataTotMois[i + 1][1] = round((dataTotMois[i + 1][0] / budgetTotJours) * 100 + dataTotMois[i][1], 1)
        else:
            dataTotMois[i + 1][1] = 0
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    pdc.set_column_pixels('A:A', 10)
    pdc.set_row_pixels(0, 10)
    pdc.set_column_pixels('D:D', 130)
    pdc.set_column_pixels('E:E', 90)
    pdc.set_column_pixels('F:F', 72)
    pdc.set_column_pixels('G:G', 85)
    pdc.set_column_pixels('I:I', 150)
    pdc.set_column_pixels('J:J', 80)
    pdc.set_column_pixels('K:K', 80)
    pdc.set_column_pixels('L:L', 80)
    pdc.set_column_pixels('M:M', 80)

    """ ---------- Création des lignes ---------- """

    """----- Titre feuille -----"""
    pdc.write('B2', 'Plan de charge', format_titre)
    pdc.write('I2', str(moisDebut) + '/' + str(anneeDebut) + ' - ' + str(moisFin) + '/' + str(anneeFin),
              format_font_rouge)

    "----- En-têtes -----"
    pdc.write('C4', 'Budget HT', format_entete)
    pdc.write('D4', 'Nom', format_entete)
    pdc.write('E4', 'Prénom', format_entete)
    pdc.write('F4', 'Entreprise', format_entete)
    pdc.write('G4', 'Budget jour', format_entete)
    pdc.write('H4', 'RAF', format_entete)
    col = 9
    for mois in moisToShow:
        pdc.write(xl_col_to_name(col) + '4', str(mois[0]) + "/" + str(mois[1]), format_date)
        col += 1
    """----- Projet -----"""
    row = 5
    for projet in data:
        pdc.write('B' + str(row), projet[1], format_entete)
        pdc.write('C' + str(row), projet[0], format_bon)
        pdc.write('I' + str(row), "", format_activite)
        for collab in projet[2:]:
            if collab != projet[2]:
                pdc.write('C' + str(row), "", format_bon)
            pdc.write('I' + str(row), "", format_activite)
            pdc.write('D' + str(row), collab[0].nom, format_bon)
            pdc.write('E' + str(row), collab[0].prenom, format_bon)
            pdc.write('F' + str(row), collab[0].entreprise, format_bon)
            pdc.write('G' + str(row), collab[2], format_bon)
            pdc.write('H' + str(row), collab[3], format_bon)
            col = 9
            for i in range(len(moisToShow)):
                pdc.write(xl_col_to_name(col) + str(row), collab[1][i], format_bon)
                col += 1
            row += 1
        if collab != projet[-1]:
            row += 1

    """----- Tableaux avancement -----"""
    row += 2
    pdc.write('I' + str(row), "Conso du mois", format_entete)
    pdc.write('I' + str(row + 1), "Avancement", format_entete)
    pdc.write('I' + str(row + 2), "Prod OTP sur le mois", format_entete)

    col = 9
    for i in range(len(moisToShow)):
        pdc.write(xl_col_to_name(col) + str(row), dataTotMois[i][0], format_bon)
        pdc.write(xl_col_to_name(col) + str(row + 1), dataTotMois[i][1], format_bon)
        pdc.write(xl_col_to_name(col) + str(row + 2), dataTotMois[i][2], format_bon)
        col += 1

    data = [dataTotMois[i][2] for i in range(len(dataTotMois))]
    graph = workbook.add_chart({'type': 'line'})
    graph.add_series({'values': '=PdC!$J$15:$' + xl_col_to_name(col) + '$15'})
    pdc.insert_chart('C' + str(row), graph)

    """--------------------------------------------------------------------------------------------------------------"""
    """------------------------------------------- Feuille CRA Marché -----------------------------------------------"""
    moisDebut, anneeDebut = request.form['moisD'], request.form['anneeD']
    moisFin, anneeFin = request.form['moisF'], request.form['anneeF']
    if anneeDebut == anneeFin:
        dates = db.session.query(Date).filter(Date.annee == anneeDebut, Date.mois <= moisFin, Date.mois >= moisDebut)
    else:
        dates = [db.session.query(Date).filter(Date.annee == anneeDebut, Date.mois >= moisDebut)]
        for i in range(int(anneeFin) - int(anneeDebut) - 1):
            dates.append(db.session.query(Date).filter(Date.annee == anneeDebut + i + 1))
        dates.append(db.session.query(Date).filter(Date.annee == anneeFin, Date.mois <= moisFin))
    boncomms = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Prod").all()
    projets = []  # Contiendra tous les différents projets en cours
    for boncomm in boncomms:
        projet = boncomm.projet
        if projet not in projets:
            projets.append(projet)

    dataBoncomms = [["CAUTRA"]]
    for projet in projets:
        if projet == "ATM1" or projet == "ATM2" or projet == "ATM1-2":
            dataBonProjet = dataBoncomms[0]
        else:
            if projet == "APP":
                dataBonProjet = ["APPROCHES"]
            elif projet == "TRANS":
                dataBonProjet = ["TRANSERVE"]
            else:
                dataBonProjet = [projet]
        # On va récupérer le nombre de jours total imputés sur ce projet :
        joursImput = 0
        bonsProjet = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Prod", Boncomm.projet == projet).all()
        for i in range(len(bonsProjet)):
            bon = bonsProjet[i]
            dataBonProjet.append([bon, valeursGlobales(bon)[2]])
            assoCollabs = bon.collabs
            for asso in assoCollabs:
                collab = asso.collab
                if anneeDebut != anneeFin:
                    for annee in dates:
                        for jour in annee:
                            imput = db.session.query(Imputation).filter(Imputation.acti_id == bon.id_acti,
                                                                        Imputation.collab_id == collab.id_collab,
                                                                        Imputation.date_id == jour.id_date).all()[0]
                            joursImput += imput.joursAllouesTache
                elif anneeDebut == anneeFin:
                    for jour in dates:
                        imput = db.session.query(Imputation).filter(Imputation.acti_id == bon.id_acti,
                                                                    Imputation.collab_id == collab.id_collab,
                                                                    Imputation.date_id == jour.id_date).all()[0]
                        joursImput += imput.joursAllouesTache
        dataBonProjet[1].append(joursImput)
        for i in range(len(dataBonProjet) - 2):  # elt 0 est la str du projet
            dataBonProjet[i + 2].append(dataBonProjet[i + 1][2] - dataBonProjet[i + 1][0].jourThq)
        if projet != "ATM1" and projet != "ATM2" and projet != "ATM1-2":
            dataBoncomms.append(dataBonProjet)
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    cra.set_column_pixels('A:A', 10)
    cra.set_row_pixels(0, 10)
    cra.set_column_pixels('D:D', 350)
    cra.set_column_pixels('E:E', 80)
    cra.set_column_pixels('F:F', 115)
    cra.set_column_pixels('G:G', 90)
    cra.set_column_pixels('H:H', 90)
    cra.set_column_pixels('I:I', 150)
    cra.set_column_pixels('J:J', 150)
    cra.set_column_pixels('K:K', 80)
    cra.set_column_pixels('L:L', 80)
    cra.set_column_pixels('M:M', 80)

    """ ---------- Création des lignes ---------- """

    """----- Titre feuille -----"""
    cra.write('B2', 'CRA Marché', format_titre)
    cra.write('F2', moisStr + " " + str(annee), format_font_rouge)

    "----- En-têtes -----"
    cra.write('B4', 'BC', format_entete)
    cra.write('C4', 'Poste', format_entete)
    cra.write('D4', 'Libellé du poste', format_entete)
    cra.write('E4', 'Date début', format_entete)
    cra.write('F4', 'Date fin contract.', format_entete)
    cra.write('G4', 'Date fin op.', format_entete)
    cra.write('H4', 'Avancement', format_entete)
    cra.write('I4', 'Jours alloués au bon', format_entete)
    cra.write('J4', 'Jours conso. tot. projet', format_entete)

    """----- Projet -----"""
    row = 5
    for projet in dataBoncomms:
        cra.write('E' + str(row), projet[0], format_activite)
        cra.write('B' + str(row), "", format_activite)
        cra.write('C' + str(row), "", format_activite)
        cra.write('D' + str(row), "", format_activite)
        cra.write('F' + str(row), "", format_activite)
        cra.write('G' + str(row), "", format_activite)
        cra.write('H' + str(row), "", format_activite)
        cra.write('I' + str(row), "", format_activite)
        cra.write('J' + str(row), "", format_activite)
        row += 1
        for bon in projet[1:]:
            cra.write('B' + str(row), bon[0].num, format_bon)
            cra.write('C' + str(row), bon[0].poste, format_bon)
            cra.write('D' + str(row), bon[0].activite, format_bon)
            cra.write('E' + str(row), bon[0].dateDebut, format_bon)
            cra.write('F' + str(row), bon[0].dateFinPrev, format_bon)
            cra.write('G' + str(row), bon[0].dateFinOp, format_bon)
            cra.write('H' + str(row), bon[1], format_bon)
            cra.write('I' + str(row), bon[0].jourThq, format_bon)
            cra.write('J' + str(row), bon[2], format_bon)
            row += 1

    """--------------------------------------------------------------------------------------------------------------"""
    workbook.close()
    return None
