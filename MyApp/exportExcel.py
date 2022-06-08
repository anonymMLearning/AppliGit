import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from MyApp.models import *
from datetime import datetime
from flask import Flask, render_template, request


def export_excel():
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    das = request.form['das']
    workbook = xlsxwriter.Workbook(
        r'C:\Users\a' + das + '\Downloads\ImputationsMS4-' + str(mois) + '-' + str(annee) + '.xlsx')
    bcm = workbook.add_worksheet('BCM')
    impGlob = workbook.add_worksheet('Imp globales')
    activitesMois = workbook.add_worksheet('Activités en cours')
    absences = workbook.add_worksheet('Absences')
    bcm.set_tab_color('#305496')
    impGlob.set_tab_color('#305496')
    activitesMois.set_tab_color('#305496')
    absences.set_tab_color('#305496')

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

    """ ----------------------------------------- Feuille BCM ------------------------------------------------------ """
    activites = db.session.query(Boncomm).filter(Boncomm.nbCongesTot == 0, Boncomm.caAtos == 0,
                                                 Boncomm.prodGdpOuFd != "Fd").all()
    bonsNonTri = db.session.query(Boncomm).filter(Boncomm.nbCongesTot == 0, Boncomm.nbJoursFormation == 0,
                                                  Boncomm.nbJoursAutre == 0, Boncomm.prodGdpOuFd != "Fd").all()
    bonsTri = []  # Liste de listes contenant le bon de Prod et celui de Gdp
    bonTot = []
    for bon in bonsNonTri:  # On va mettre les part Prod et Gdp ensemble pour calculer les valeurs totales sur le bon
        if bon.activite[0:4] != "CP -":
            bonTot.append(bon)
        elif bon.activite[0:4] == "CP -":
            bonTot.append(bon)
            bonsTri.append(bonTot)
            bonTot = []

    dateNow = str(datetime.now())
    moisStr = stringMois(str(int(dateNow[5:7])))
    annee = int(dateNow[:4])
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    bcm.set_column_pixels('A:A', 10)
    bcm.set_row_pixels(0, 10)
    bcm.set_column_pixels('D:D', 300)
    bcm.set_column_pixels('F:F', 72)
    bcm.set_column_pixels('G:G', 85)
    bcm.set_column_pixels('I:I', 80)
    bcm.set_column_pixels('J:J', 80)
    bcm.set_column_pixels('K:K', 45)
    bcm.set_column_pixels('L:L', 300)

    """ ---------- Création des lignes ---------- """

    """----- Titre feuille -----"""
    bcm.write('B2', 'Ensemble des activités depuis le début du projet', format_titre)

    "----- En-têtes -----"
    bcm.write('B4', 'Numéro', format_entete)
    bcm.write('C4', 'Poste', format_entete)
    bcm.write('D4', 'Activité', format_entete)
    bcm.write('E4', 'Année', format_entete)
    bcm.write('F4', 'CA Atos', format_entete)
    bcm.write('G4', 'Jours alloués', format_entete)
    bcm.write('H4', 'Délais', format_entete)
    bcm.write('I4', 'Montant HT', format_entete)
    bcm.write('J4', 'Part EGIS', format_entete)
    bcm.write('K4', 'Etat', format_entete)
    bcm.write('L4', 'Commentaire', format_entete)

    """----- Activités : formation et autres activité -----"""
    row = 6;
    for activite in activites:
        if activite.etat != "TE":
            bcm.write('B' + str(row), activite.num, format_activite)
            bcm.write('C' + str(row), activite.poste, format_activite)
            bcm.write('D' + str(row), activite.activite, format_activite)
            bcm.write('E' + str(row), activite.anneeTarif, format_activite)
            bcm.write('F' + str(row), '', format_activite)
            bcm.write('G' + str(row), activite.jourThq, format_activite)
            bcm.write('H' + str(row), '', format_activite)
            bcm.write('I' + str(row), '', format_activite)
            bcm.write('J' + str(row), '', format_activite)
            bcm.write('K' + str(row), activite.etat, format_activite)
            bcm.write('L' + str(row), activite.com, format_activite)
            row += 1
        else:
            bcm.write('B' + str(row), activite.num, format_fin)
            bcm.write('C' + str(row), activite.poste, format_fin)
            bcm.write('D' + str(row), activite.activite, format_fin)
            bcm.write('E' + str(row), activite.anneeTarif, format_fin)
            bcm.write('F' + str(row), '', format_fin)
            bcm.write('G' + str(row), activite.jourThq, format_fin)
            bcm.write('H' + str(row), '', format_fin)
            bcm.write('I' + str(row), '', format_fin)
            bcm.write('J' + str(row), '', format_fin)
            bcm.write('K' + str(row), activite.etat, format_fin)
            bcm.write('L' + str(row), activite.com, format_fin)
            row += 1

    """----- Bons de commande -----"""
    for bon in bonsTri:
        if bon[0].etat != "TE":
            bcm.write('B' + str(row), bon[0].num, format_bon)
            bcm.write('C' + str(row), bon[0].poste, format_bon)
            bcm.write('D' + str(row), bon[0].activite, format_bon)
            bcm.write('E' + str(row), bon[0].anneeTarif, format_bon)
            bcm.write('F' + str(row), bon[0].caAtos, format_bon)
            bcm.write('G' + str(row), bon[0].jourThq + bon[1].jourThq, format_bon)  # Jours total du bon (Prod + GDP)
            bcm.write('H' + str(row), bon[0].delais, format_bon)
            bcm.write('I' + str(row), bon[0].montantHT, format_bon)
            bcm.write('J' + str(row), bon[0].partEGIS, format_bon)
            bcm.write('K' + str(row), bon[0].etat, format_bon)
            bcm.write('L' + str(row), bon[0].com, format_bon)
            row += 1
        else:
            bcm.write('B' + str(row), bon[0].num, format_fin)
            bcm.write('C' + str(row), bon[0].poste, format_fin)
            bcm.write('D' + str(row), bon[0].activite, format_fin)
            bcm.write('E' + str(row), bon[0].anneeTarif, format_fin)
            bcm.write('F' + str(row), bon[0].caAtos, format_fin)
            bcm.write('G' + str(row), bon[0].jourThq + bon[1].jourThq, format_fin)  # Jours total du bon (Prod + GDP)
            bcm.write('H' + str(row), bon[0].delais, format_fin)
            bcm.write('I' + str(row), bon[0].montantHT, format_fin)
            bcm.write('J' + str(row), bon[0].partEGIS, format_fin)
            bcm.write('K' + str(row), bon[0].etat, format_fin)
            bcm.write('L' + str(row), bon[0].com, format_fin)
            row += 1
    """----- Ligne 1 : total -----"""
    bcm.write('B5', '', format_entete)
    bcm.write('C5', '', format_entete)
    bcm.write('D5', '', format_entete)
    bcm.write('E5', '', format_entete)
    bcm.write_formula('F5', '=SUM(F6:F' + str(row - 1) + ')', format_entete)
    bcm.write_formula('G5', '=SUM(G6:G' + str(row - 1) + ')', format_entete)
    bcm.write('H5', '', format_entete)
    bcm.write_formula('I5', '=SUM(I6:I' + str(row - 1) + ')', format_entete)
    bcm.write_formula('J5', '=SUM(J6:J' + str(row - 1) + ')', format_entete)
    bcm.write('K5', '', format_entete)
    bcm.write('L5', '', format_entete)

    """ ------------------------------------------------------------------------------------------------------------ """

    """ ------------------------------------- Feuille Imp globales ------------------------------------------------- """

    collabs = db.session.query(Collab).filter(Collab.access != 3).all()

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    impGlob.set_column_pixels('A:A', 10)
    impGlob.set_row_pixels(0, 10)
    impGlob.set_column_pixels('E:E', 300)
    impGlob.set_column_pixels('B:B', 80)
    impGlob.set_column_pixels('C:C', 80)
    impGlob.set_column_pixels('D:D', 80)
    impGlob.set_column_pixels('F:F', 95)
    impGlob.set_column_pixels('G:G', 95)
    impGlob.set_column_pixels('I:I', 45)
    impGlob.set_column_pixels('H:H', 95)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    impGlob.write('B2', 'Imputations globales', format_titre)

    "----- En-têtes -----"
    impGlob.write('B4', 'Projet', format_entete)
    impGlob.write('C4', 'BCM', format_entete)
    impGlob.write('D4', 'Poste', format_entete)
    impGlob.write('E4', 'Activité', format_entete)
    impGlob.write('F4', 'Avancement', format_entete)
    impGlob.write('G4', 'Jours alloués', format_entete)
    impGlob.write('H4', 'Consommés', format_entete)
    impGlob.write('I4', 'RAF', format_entete)
    col = 9
    for collab in collabs:
        impGlob.write(xl_col_to_name(col) + '4', 'Alloués', format_entete)
        impGlob.write(xl_col_to_name(col + 1) + '4', 'Conso', format_entete)
        impGlob.write(xl_col_to_name(col + 2) + '4', 'RAF', format_entete)
        impGlob.write(xl_col_to_name(col) + '3', '', format_entete)
        impGlob.write(xl_col_to_name(col + 1) + '3', collab.nom, format_entete)
        impGlob.write(xl_col_to_name(col + 2) + '3', '', format_entete)
        col += 3

    """----- Bons de commande -----"""
    row = 5
    for bon in bonsTri:
        valeurs = valeursGlobales(bon[0])
        valeursGdp = valeursGlobales(bon[1])
        avancementTot = int((valeurs[4] + valeursGdp[4]) / (bon[0].jourThq + bon[1].jourThq) * 100)
        # Ligne Prod + Gdp
        impGlob.write('B' + str(row), bon[0].projet, format_activite)
        impGlob.write('C' + str(row), bon[0].num, format_activite)
        impGlob.write('D' + str(row), bon[0].poste, format_activite)
        impGlob.write('E' + str(row), 'commande - ' + bon[0].activite, format_activite)
        if 100 > avancementTot >= 0:
            impGlob.write('F' + str(row), str(avancementTot) + ' %', format_activite)
        elif avancementTot == 100:
            impGlob.write('F' + str(row), str(avancementTot) + ' %', format_vert)
        elif avancementTot > 100:
            impGlob.write('F' + str(row), str(avancementTot) + ' %', format_rouge)
        impGlob.write('G' + str(row), bon[0].jourThq + bon[1].jourThq, format_activite)
        impGlob.write('H' + str(row), valeurs[4] + valeursGdp[4], format_activite)
        impGlob.write('I' + str(row), valeurs[3] + valeursGdp[3], format_activite)
        # Ligne Prod
        impGlob.write('B' + str(row + 1), bon[0].projet, format_bon)
        impGlob.write('C' + str(row + 1), bon[0].num, format_bon)
        impGlob.write('D' + str(row + 1), bon[0].poste, format_bon)
        impGlob.write('E' + str(row + 1), bon[0].activite, format_bon)
        if 100 > valeurs[2] >= 0:
            impGlob.write('F' + str(row + 1), str(valeurs[2]) + ' %', format_bon)
        elif valeurs[2] == 100:
            impGlob.write('F' + str(row + 1), str(valeurs[2]) + ' %', format_vert)
        elif valeurs[2] > 100:
            impGlob.write('F' + str(row + 1), str(valeurs[2]) + ' %', format_rouge)
        impGlob.write('G' + str(row + 1), bon[0].jourThq, format_bon)
        impGlob.write('H' + str(row + 1), valeurs[4], format_bon)
        impGlob.write('I' + str(row + 1), valeurs[3], format_bon)
        # Ligne Gdp
        impGlob.write('B' + str(row + 2), bon[0].projet, format_bon)
        impGlob.write('C' + str(row + 2), bon[0].num, format_bon)
        impGlob.write('D' + str(row + 2), bon[0].poste, format_bon)
        impGlob.write('E' + str(row + 2), 'CP - ' + bon[0].activite, format_bon)
        if 100 > valeursGdp[2] >= 0:
            impGlob.write('F' + str(row + 2), str(valeursGdp[2]) + ' %', format_bon)
        elif valeursGdp[2] == 100:
            impGlob.write('F' + str(row + 2), str(valeursGdp[2]) + ' %', format_vert)
        elif valeursGdp[2] > 100:
            impGlob.write('F' + str(row + 2), str(valeursGdp[2]) + ' %', format_rouge)
        impGlob.write('G' + str(row + 2), bon[1].jourThq, format_bon)
        impGlob.write('H' + str(row + 2), valeursGdp[4], format_bon)
        impGlob.write('I' + str(row + 2), valeursGdp[3], format_bon)
        col = 9
        for collab in collabs:
            # Pour la partie Prod
            asso = db.session.query(AssociationBoncommCollab).filter(
                AssociationBoncommCollab.boncomm_id == bon[0].id_acti,
                AssociationBoncommCollab.collab_id == collab.id_collab).all()
            if asso != []:
                joursAllouesCollab = asso[0].joursAllouesBC
                imputations = db.session.query(Imputation).filter(Imputation.acti_id == bon[0].id_acti,
                                                                  Imputation.collab_id == collab.id_collab,
                                                                  Imputation.joursAllouesTache != 0).all()
                joursConso = 0
                for imputation in imputations:
                    joursConso += imputation.joursAllouesTache
                raf = float(joursAllouesCollab) - float(joursConso)
            else:
                joursAllouesCollab = ""
                joursConso = ""
                raf = ""
            # Pour la partie Gdp
            assoGDP = db.session.query(AssociationBoncommCollab).filter(
                AssociationBoncommCollab.boncomm_id == bon[1].id_acti,
                AssociationBoncommCollab.collab_id == collab.id_collab).all()
            if assoGDP != []:
                joursAllouesCollabGDP = assoGDP[0].joursAllouesBC
                imputsGDP = db.session.query(Imputation).filter(Imputation.acti_id == bon[1].id_acti,
                                                                Imputation.collab_id == collab.id_collab,
                                                                Imputation.joursAllouesTache != 0).all()
                joursConsoGDP = 0
                for imputGDP in imputsGDP:
                    joursConsoGDP += imputGDP.joursAllouesTache
                rafGDP = float(joursAllouesCollabGDP) - float(joursConsoGDP)
            else:
                joursAllouesCollabGDP = ""
                joursConsoGDP = ""
                rafGDP = ""
            impGlob.write(xl_col_to_name(col) + str(row), "", format_activite)
            impGlob.write(xl_col_to_name(col + 1) + str(row), "", format_activite)
            impGlob.write(xl_col_to_name(col + 2) + str(row), "", format_activite)
            impGlob.write(xl_col_to_name(col) + str(row + 1), joursAllouesCollab, format_bon)
            impGlob.write(xl_col_to_name(col + 1) + str(row + 1), joursConso, format_bon)
            impGlob.write(xl_col_to_name(col + 2) + str(row + 1), raf, format_bon)
            impGlob.write(xl_col_to_name(col) + str(row + 2), joursAllouesCollabGDP, format_bon)
            impGlob.write(xl_col_to_name(col + 1) + str(row + 2), joursConsoGDP, format_bon)
            impGlob.write(xl_col_to_name(col + 2) + str(row + 2), rafGDP, format_bon)
            col += 3
        row += 3
    """ ------------------------------------------------------------------------------------------------------------ """

    """ ---------------------------------- Feuille Activités en cours ---------------------------------------------- """

    activitesECMois = db.session.query(Boncomm).filter(Boncomm.nbCongesTot == 0, Boncomm.caAtos == 0,
                                                       Boncomm.etat != "TE", Boncomm.prodGdpOuFd != "Fd").all()
    bonsNonTriMois = db.session.query(Boncomm).filter(Boncomm.nbCongesTot == 0, Boncomm.nbJoursFormation == 0,
                                                      Boncomm.nbJoursAutre == 0, Boncomm.etat != "TE",
                                                      Boncomm.prodGdpOuFd != "Fd").all()
    bonsTriMois = []  # Liste de listes contenant le bon de Prod et celui de Gdp
    bonTot = []
    for bon in bonsNonTriMois:  # On va mettre les part Prod et Gdp ensemble pour calculer les valeurs totales sur
        # tout le bon
        if bon.activite[0:4] != "CP -":
            bonTot.append(bon)
        elif bon.activite[0:4] == "CP -":
            bonTot.append(bon)
            bonsTriMois.append(bonTot)
            bonTot = []

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    activitesMois.set_column_pixels('A:A', 10)
    activitesMois.set_row_pixels(0, 10)
    activitesMois.set_column_pixels('D:D', 300)
    activitesMois.set_column_pixels('F:F', 90)
    activitesMois.set_column_pixels('G:G', 120)
    activitesMois.set_column_pixels('H:H', 40)
    activitesMois.set_column_pixels('I:I', 300)

    """ ---------- Création des lignes ---------- """

    """----- Titre feuille -----"""
    activitesMois.write('B2', 'Ensemble des activités en cours ce mois', format_titre)
    activitesMois.write('I2', moisStr + " " + str(annee), format_font_rouge)

    "----- En-têtes -----"
    activitesMois.write('B4', 'Numéro', format_entete)
    activitesMois.write('C4', 'Poste', format_entete)
    activitesMois.write('D4', 'Activité', format_entete)
    activitesMois.write('E4', 'Année', format_entete)
    activitesMois.write('F4', 'Jours alloués', format_entete)
    activitesMois.write('G4', 'Jours consommés', format_entete)
    activitesMois.write('H4', 'RAF', format_entete)
    activitesMois.write('I4', 'Commentaire', format_entete)

    """----- Activités : formation et autres activité -----"""
    row = 6;
    for activite in activitesECMois:
        valeurs = valeursGlobales(activite)
        activitesMois.write('B' + str(row), activite.num, format_activite)
        activitesMois.write('C' + str(row), activite.poste, format_activite)
        activitesMois.write('D' + str(row), activite.activite, format_activite)
        activitesMois.write('E' + str(row), activite.anneeTarif, format_activite)
        activitesMois.write('F' + str(row), activite.jourThq, format_activite)
        activitesMois.write('G' + str(row), valeurs[4], format_activite)
        activitesMois.write('H' + str(row), valeurs[3], format_activite)
        activitesMois.write('I' + str(row), activite.com, format_activite)
        row += 1
    """----- Bons de commande -----"""
    for bon in bonsTriMois:
        valeurs = valeursGlobales(bon[0])
        valeursGdp = valeursGlobales(bon[1])
        activitesMois.write('B' + str(row), bon[0].num, format_bon)
        activitesMois.write('C' + str(row), bon[0].poste, format_bon)
        activitesMois.write('D' + str(row), bon[0].activite, format_bon)
        activitesMois.write('E' + str(row), bon[0].anneeTarif, format_bon)
        activitesMois.write('F' + str(row), bon[0].jourThq + bon[1].jourThq, format_bon)
        activitesMois.write('G' + str(row), valeurs[4] + valeursGdp[4], format_bon)
        activitesMois.write('H' + str(row), valeurs[3] + valeursGdp[3], format_bon)
        activitesMois.write('I' + str(row), bon[0].com, format_bon)
        row += 1

    """----- Ligne 1 : total -----"""
    activitesMois.write('B5', '', format_entete)
    activitesMois.write('C5', '', format_entete)
    activitesMois.write('D5', '', format_entete)
    activitesMois.write('E5', '', format_entete)
    activitesMois.write_formula('F5', '=SUM(F6:F' + str(row - 1) + ')', format_entete)
    activitesMois.write_formula('G5', '=SUM(G6:G' + str(row - 1) + ')', format_entete)
    activitesMois.write_formula('H5', '=SUM(H6:H' + str(row - 1) + ')', format_entete)
    activitesMois.write('I5', '', format_entete)

    """ ------------------------------------------------------------------------------------------------------------ """

    """ --------------------------------------- Feuille Absences --------------------------------------------------- """
    dates = db.session.query(Date).filter(Date.mois == mois, Date.annee == annee).all()
    collabsActifs = db.session.query(Collab).filter(Collab.access != 4, Collab.access != 3).all()

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    absences.set_column_pixels('A:A', 10)
    absences.set_row_pixels(0, 10)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    absences.write('B2', 'Absences - ' + moisStr + ' ' + str(annee), format_titre)
    absences.write('F2', " 1 : journée entière,  0,5 : demi-journée  ", format_font_rouge)

    "----- Création du tableau -----"
    absences.write('C4', 'Total Abs.', format_entete)
    col = 3
    for date in dates:
        dateStr = date.transfoDate()
        absences.write_datetime(xl_col_to_name(col) + '4', dateStr, format_date)
        absences.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 50)
        col += 1
    row = 5
    for collab in collabsActifs:
        absences.write('B' + str(row), collab.nom, format_entete)
        assos = collab.boncomms
        for i in range(len(assos)):  # On récupère les congés
            boncomm = assos[i].boncomm
            if boncomm.nbCongesTot != 0:
                conges = boncomm
        joursPoses = 0
        col = 3
        for date in dates:
            imputJour = db.session.query(Imputation).filter(Imputation.date_id == date.id_date,
                                                            Imputation.acti_id == conges.id_acti,
                                                            Imputation.collab_id == collab.id_collab).all()
            if imputJour[0].joursAllouesTache != 0:
                absences.write(xl_col_to_name(col) + str(row), imputJour[0].joursAllouesTache, format_bon)
            else:
                absences.write(xl_col_to_name(col) + str(row), "", format_bon)
            joursPoses += imputJour[0].joursAllouesTache
            col += 1
        absences.write('C' + str(row), joursPoses, format_entete)
        row += 1
    """------------------------------------------------------------------------------------------------------------- """

    """ --------------------------------------- Feuille Collabs ---------------------------------------------------- """
    columns = columnMois(mois, annee)
    for collab in collabsActifs:
        feuilleCollab = workbook.add_worksheet(collab.abreviation())
        feuilleCollab.set_tab_color('#305496')

        """ ---------- Format et tailles des cellules ---------- """
        """----- Taille lignes et colonnes -----"""
        feuilleCollab.set_column_pixels('A:A', 10)
        feuilleCollab.set_column_pixels('B:B', 300)
        feuilleCollab.set_column_pixels('C:C', 115)
        feuilleCollab.set_column_pixels('I:I', 90)
        feuilleCollab.set_column_pixels('J:J', 95)
        feuilleCollab.set_row_pixels(0, 10)

        """ ---------- Création des lignes ---------- """
        """----- Titre feuille -----"""
        feuilleCollab.write('B2', 'Imputations de ' + collab.nom + ", " + moisStr + ' ' + str(annee), format_titre)
        joursMois = nbJoursMoisSansWeekEnd(mois, annee)
        feuilleCollab.write('I2', "Nb de jours dispo dans le mois : " + str(joursMois), format_font_rouge)

        "----- En-têtes -----"
        feuilleCollab.write('B5', 'Activité', format_entete)
        feuilleCollab.write('C4', 'N° Semaine', format_entete)
        feuilleCollab.write('C5', 'Jours disponibles', format_entete)
        col = 3
        for column in columns:
            feuilleCollab.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 50)
            feuilleCollab.write(xl_col_to_name(col) + '4', column[0], format_activite)
            feuilleCollab.write(xl_col_to_name(col) + '5', column[1], format_activite)
            col += 1
        feuilleCollab.write(xl_col_to_name(col) + '5', 'Jours alloués', format_entete)
        feuilleCollab.write(xl_col_to_name(col + 1) + '5', 'RAF', format_entete)

        """----- Bons de commande -----"""
        assos = collab.boncomms
        row = 6
        for i in range(len(assos)):
            boncomm = assos[i].boncomm
            if boncomm.nbCongesTot == 0 and assos[i].joursAllouesBC != 0 and boncomm.etat != "TE":
                feuilleCollab.write('B' + str(row), boncomm.activite, format_activite)
                feuilleCollab.write('C' + str(row), '-', format_bon)
                col = 3
                dejaConso = 0
                for column in columns:

                    numSemaine = column[0]
                    date_access = []
                    jourImpute = 0
                    for date in dates:
                        if date.numSemaine() == numSemaine:
                            date_access.append(date)
                    for jour in date_access:
                        imputation = db.session.query(Imputation).filter(Imputation.date_id == jour.id_date,
                                                                         Imputation.acti_id == boncomm.id_acti,
                                                                         Imputation.collab_id == collab.id_collab).all()[
                            0]
                        jourImpute += imputation.joursAllouesTache
                        dejaConso += imputation.joursAllouesTache
                    feuilleCollab.write(xl_col_to_name(col) + str(row), jourImpute, format_bon)
                    col += 1
                feuilleCollab.write(xl_col_to_name(col) + str(row), assos[i].joursAllouesBC, format_activite)
                feuilleCollab.write(xl_col_to_name(col + 1) + str(row), assos[i].joursAllouesBC - dejaConso,
                                    format_activite)
                row += 1

    """------------------------------------------------------------------------------------------------------------- """

    workbook.close()
    return None
