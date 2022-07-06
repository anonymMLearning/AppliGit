import xlsxwriter
from xlsxwriter.utility import xl_col_to_name

from MyApp.models import *
from datetime import datetime
from flask import Flask, request


def export_excel_deplacement():
    dateNow = str(datetime.now())
    mois = int(dateNow[5:7])
    annee = int(dateNow[:4])
    das = request.form['das']

    workbook = xlsxwriter.Workbook(
        r'C:\Users\a' + das + '\Downloads\Suivi Déplacements MS4 ' + '.xlsx')
    chronoAPM = workbook.add_worksheet('chronoAPM')
    chronoAPM.set_tab_color('#305496')
    soldeAtos = workbook.add_worksheet('Solde realise Atos')
    soldeAtos.set_tab_color('#305496')
    soldeEgis = workbook.add_worksheet('Solde realise EGIS')
    soldeEgis.set_tab_color('#305496')

    """----- Format des titres -----"""
    format_titre = workbook.add_format()
    format_titre.set_font_color('#305496')
    format_titre.set_font_size(18)
    format_titre.set_italic()
    format_titre.set_underline()

    """----- Format séparations -----"""
    format_sep = workbook.add_format()
    format_sep.set_bg_color('#6c757d')
    format_sep.set_italic()
    format_sep.set_underline()

    """----- Format écritures rouges -----"""
    format_font_rouge = workbook.add_format()
    format_font_rouge.set_font_color('red')
    format_font_rouge.set_font_size(18)

    """----- Format cases en-têtes -----"""
    format_entete = workbook.add_format()
    format_entete.set_font_color('white')
    format_entete.set_bold()
    format_entete.set_bg_color('#305496')
    format_entete.set_align('vcenter')
    format_entete.set_align('center')
    format_entete.set_border()
    format_entete.set_text_wrap()

    """----- Format UO -----"""
    format_uo = workbook.add_format()
    format_uo.set_font_color('white')
    format_uo.set_bold()
    format_uo.set_bg_color('#305496')
    format_uo.set_align('vcenter')
    format_uo.set_align('center')
    format_uo.set_rotation(90)
    format_uo.set_border()

    """----- Format des formations et autres activités -----"""
    format_activite = workbook.add_format()
    format_activite.set_bg_color('#8EA9DB')
    format_activite.set_align('center')
    format_activite.set_align('vcenter')
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
    """------------------------------------------- Feuille Chrono APM -----------------------------------------------"""
    fds = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Fd", Boncomm.apm != "").all()  # Que les apm
    # Servira pour trier dans l'ordre les asso aux Fds, contient différents type de ndf :
    ndfRef = db.session.query(NoteDeFrais).filter(NoteDeFrais.acti_id == 0).all()
    uos = db.session.query(UO).filter(UO.type == "Fd").all()
    dataToShow = []
    for j in range(len(fds)):
        dataAssosUo = db.session.query(AssoUoBoncomm).filter(AssoUoBoncomm.boncomm_id == fds[j].id_acti).all()
        assosUo = []
        for asso in dataAssosUo:
            if asso.uo.type == "Fd":  # Que les UO de déplacement
                assosUo.append(asso)
        notesDeFrais = db.session.query(NoteDeFrais).filter(NoteDeFrais.acti_id == fds[j].id_acti).all()
        if len(notesDeFrais) == 0:
            dataNDF = ["" for i in range(len(ndfRef))]
        else:
            dataNDF = []
            for note in ndfRef:  # On va classer les NDF dans l'ordre pour correspondre à l'affichage
                i = 0
                nb = len(dataNDF)
                while i < len(ndfRef) and i < len(notesDeFrais):
                    if notesDeFrais[i].type == note.type:
                        dataNDF.append(notesDeFrais[i].depense)
                        i = len(ndfRef)  # Pour sortir de la boucle while
                    else:
                        i += 1
                if nb == len(dataNDF):
                    dataNDF.append("")  # Si on arrive ici, c'est qu'il n'y a pas de cette note associée à ce BC
        assoCollab = db.session.query(AssociationBoncommCollab).filter(
            AssociationBoncommCollab.boncomm_id == fds[j].id_acti).all()[0]  # Un seul intervenant par FD
        dataToAdd = [fds[j], assoCollab.collab, assoCollab.collab.abreviation(), assosUo, dataNDF]

        totUo, totNdf = 0, 0
        for asso in assosUo:
            totUo += asso.facteur * asso.uo.prix
        for ndf in notesDeFrais:
            totNdf += ndf.depense
        dataToAdd.append(totNdf)
        dataToAdd.append(totUo)

        if j == 0:
            dataToAdd.append(round((totUo - totNdf) + fds[j].margeLib, 2))
        else:
            dataToAdd.append(round((totUo - totNdf) + dataToShow[j - 1][7] + fds[j].margeLib, 2))

        dataToShow.append(dataToAdd)
    collabs = db.session.query(Collab).all()
    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    chronoAPM.set_column_pixels('A:A', 10)
    chronoAPM.set_row_pixels(0, 10)
    chronoAPM.set_row_pixels(3, 100)
    chronoAPM.set_column_pixels('B:B', 80)
    chronoAPM.set_column_pixels('C:C', 80)
    chronoAPM.set_column_pixels('F:F', 200)
    chronoAPM.set_column_pixels('G:G', 80)
    chronoAPM.set_column_pixels('H:H', 80)
    chronoAPM.set_column_pixels('L:L', 5)
    chronoAPM.set_column_pixels('I:I', 90)
    chronoAPM.set_column_pixels('K:K', 90)
    chronoAPM.set_column_pixels('Q:Q', 80)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    chronoAPM.write('B2', 'Chrono des APM', format_titre)
    "----- En-têtes -----"
    chronoAPM.merge_range(3, 2, 5, 2, 'N°APM', format_entete)
    chronoAPM.merge_range(3, 3, 5, 3, 'N°BC', format_entete)
    chronoAPM.merge_range(3, 4, 5, 4, 'Poste', format_entete)
    chronoAPM.merge_range(3, 5, 5, 5, 'Objet', format_entete)
    chronoAPM.merge_range(3, 6, 5, 6, 'Date début mission', format_entete)
    chronoAPM.merge_range(3, 7, 5, 7, 'Date fin mission', format_entete)
    chronoAPM.merge_range(3, 8, 5, 8, 'Lieu', format_entete)
    chronoAPM.merge_range(3, 9, 5, 9, 'Société', format_entete)
    chronoAPM.merge_range(3, 10, 5, 10, 'Intervant', format_entete)
    chronoAPM.merge_range(3, 11, 5, 11, '', format_sep)

    col = 12
    for uo in uos:
        chronoAPM.write(xl_col_to_name(col) + '4', uo.description, format_uo)
        chronoAPM.write(xl_col_to_name(col) + '5', uo.num, format_activite)
        chronoAPM.write(xl_col_to_name(col) + '6', uo.prix, format_activite)
        col += 1
    chronoAPM.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
    chronoAPM.merge_range(3, col, 5, col, '', format_sep)
    col += 1

    chronoAPM.merge_range(3, col, 5, col, 'Client', format_entete)
    col += 1
    chronoAPM.merge_range(3, col, 5, col, 'Date signature', format_entete)
    col += 1
    chronoAPM.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
    chronoAPM.merge_range(3, col, 5, col, '', format_sep)
    col += 1

    chronoAPM.merge_range(3, col, 3, col + len(ndfRef) - 1, 'NdF Collab.', format_entete)
    for ndf in ndfRef:
        chronoAPM.write(xl_col_to_name(col) + '5', ndf.type, format_activite)
        chronoAPM.write(xl_col_to_name(col) + '6',
                        '=SUM(' + xl_col_to_name(col) + '7:' + xl_col_to_name(col) + str(7 + len(fds)) + ')',
                        format_activite)
        col += 1
    chronoAPM.set_column_pixels(xl_col_to_name(col - 1) + ':' + xl_col_to_name(col - 1), 90)
    chronoAPM.set_column_pixels(xl_col_to_name(col) + ':' + xl_col_to_name(col), 5)
    chronoAPM.merge_range(3, col, 5, col, '', format_sep)
    col += 1

    chronoAPM.merge_range(3, col, 5, col, 'Total NdF', format_uo)
    col += 1
    chronoAPM.merge_range(3, col, 5, col, 'Total UO', format_uo)
    col += 1
    chronoAPM.merge_range(3, col, 4, col + 2, 'Ecart NdF', format_entete)
    chronoAPM.write(xl_col_to_name(col) + '6', 'Dép.', format_activite)
    chronoAPM.write(xl_col_to_name(col + 1) + '6', 'Marge lib.', format_activite)
    chronoAPM.set_column_pixels(xl_col_to_name(col + 1) + ':' + xl_col_to_name(col + 1), 80)
    chronoAPM.write(xl_col_to_name(col + 2) + '6', 'Cumul', format_activite)

    """----- Remplissage des données -----"""
    row = 7
    for fd in dataToShow:
        col = 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].num) + str(fd[0].poste) + str(fd[1].entreprise),
                        format_activite)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].apm), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].num), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].poste), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].activite), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].dateDebut), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].dateFinOp), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].lieu), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[1].entreprise), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[2]), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), '', format_sep)
        col += 1
        for asso in fd[3]:
            chronoAPM.write(xl_col_to_name(col) + str(row), asso.facteur, format_bon)
            col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), '', format_sep)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].client), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].dateSign), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), '', format_sep)
        col += 1
        for ndf in fd[4]:
            chronoAPM.write(xl_col_to_name(col) + str(row), ndf, format_bon)
            col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), '', format_sep)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[5]), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[6]), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[6] - fd[5]), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[0].margeLib), format_bon)
        col += 1
        chronoAPM.write(xl_col_to_name(col) + str(row), str(fd[7]), format_bon)
        col += 1
        row += 1

    """--------------------------------------------------------------------------------------------------------------"""
    """------------------------------------------- Feuille Solde Atos -----------------------------------------------"""
    fds = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Fd", Boncomm.apm == "").all()
    fdAtos = triFd("Atos", fds)
    uosFd = db.session.query(UO).filter(UO.type == "Fd").all()
    nbUosFd = len(uosFd)
    dataFdAtos = []
    dataTotUo = []
    for i in range(nbUosFd):
        dataTotUo.append([0, 0, 0, 0])
    for fd in fdAtos:
        dataToAdd = [fd]
        apms = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Fd", Boncomm.apm != "",
                                                Boncomm.num == fd.num).all()  # Tous les apms liés à ce FD
        dataToAdd.append(apms[0].collabs[0].collab.entreprise)  # Entreprise lié à ce FD
        dataToAdd.append('20' + str(apms[0].num[-2:]))  # Année du FD
        dataToAdd.append(apms[0].client)  # Client lié à ce FD
        # collabs[0] car un seul collab lié à un FD
        dataUo = []
        for j in range(nbUosFd):
            uo = uosFd[j]
            data = []
            facteurFd = db.session.query(AssoUoBoncomm).filter(AssoUoBoncomm.uo_id == uo.id_uo,
                                                               AssoUoBoncomm.boncomm_id == fd.id_acti).all()[0].facteur
            data.append(facteurFd)
            dataTotUo[j][0] += facteurFd
            facteurAffecte = 0
            for apm in apms:
                facteurAffecte += db.session.query(AssoUoBoncomm).filter(
                    AssoUoBoncomm.uo_id == uo.id_uo, AssoUoBoncomm.boncomm_id == apm.id_acti).all()[0].facteur
            data.append(facteurAffecte)
            dataTotUo[j][1] += facteurAffecte
            data.append(facteurFd - facteurAffecte)
            dataTotUo[j][2] += (facteurFd - facteurAffecte)
            dataUo.append(data)
        dataToAdd.append(dataUo)
        dataFdAtos.append(dataToAdd)
    for j in range(nbUosFd):
        dataTotUo[j][3] = dataTotUo[j][0] * uosFd[j].prix

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    soldeAtos.set_column_pixels('A:A', 10)
    soldeAtos.set_column_pixels('B:B', 90)
    soldeAtos.set_column_pixels('H:H', 90)
    soldeAtos.set_row_pixels(0, 10)
    soldeAtos.set_row_pixels(5, 30)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    soldeAtos.write('B2', 'Solde réalisé Atos', format_titre)
    "----- En-têtes -----"
    soldeAtos.write('C6', 'Lot', format_entete)
    soldeAtos.write('D6', 'N°BC', format_entete)
    soldeAtos.write('E6', 'Poste', format_entete)
    soldeAtos.write('F6', 'Client', format_entete)
    soldeAtos.write('G6', 'Libellé', format_entete)
    soldeAtos.write('H6', 'Échéance', format_entete)
    soldeAtos.write('I6', 'État', format_entete)
    soldeAtos.set_column_pixels('J:J', 5)
    soldeAtos.write('J6', '', format_sep)
    col = 10
    for uo in uosFd:
        soldeAtos.merge_range(3, col, 3, col + 2, uo.description, format_entete)
        soldeAtos.merge_range(4, col, 4, col + 2, uo.prix, format_entete)
        soldeAtos.write(xl_col_to_name(col) + '6', 'BC', format_activite)
        soldeAtos.write(xl_col_to_name(col + 1) + '6', 'Affecté', format_activite)
        soldeAtos.write(xl_col_to_name(col + 2) + '6', 'Dispo', format_activite)
        soldeAtos.set_column_pixels(xl_col_to_name(col + 3) + ':' + xl_col_to_name(col + 3), 5)
        soldeAtos.write(xl_col_to_name(col + 3) + '6', '', format_sep)
        col += 4

    row = 7
    for fd in dataFdAtos:
        col = 1
        soldeAtos.write(xl_col_to_name(col) + str(row), str(fd[0].num) + str(fd[0].poste) + str(fd[1]), format_activite)
        soldeAtos.write(xl_col_to_name(col + 1) + str(row), fd[2], format_bon)
        soldeAtos.write(xl_col_to_name(col + 2) + str(row), fd[0].num, format_bon)
        soldeAtos.write(xl_col_to_name(col + 3) + str(row), fd[0].poste, format_bon)
        soldeAtos.write(xl_col_to_name(col + 4) + str(row), fd[3], format_bon)
        soldeAtos.write(xl_col_to_name(col + 5) + str(row), fd[0].activite, format_bon)
        soldeAtos.write(xl_col_to_name(col + 6) + str(row), fd[0].dateFinOp, format_bon)
        soldeAtos.write(xl_col_to_name(col + 7) + str(row), fd[0].etat, format_bon)
        soldeAtos.write(xl_col_to_name(col + 8) + str(row), '', format_sep)
        col = 10
        for i in range(nbUosFd):
            soldeAtos.write(xl_col_to_name(col) + str(row), fd[4][i][0], format_bon)
            soldeAtos.write(xl_col_to_name(col + 1) + str(row), fd[4][i][1], format_bon)
            soldeAtos.write(xl_col_to_name(col + 2) + str(row), fd[4][i][2], format_bon)
            soldeAtos.write(xl_col_to_name(col + 3) + str(row), '', format_sep)
            col += 4
        row += 1

    soldeAtos.write('I' + str(row), 'Total', format_entete)
    soldeAtos.write('I' + str(row + 1), 'Total UO revenus', format_entete)
    soldeAtos.write('J' + str(row), '', format_sep)
    soldeAtos.write('J' + str(row + 1), '', format_sep)
    col = 10
    for j in range(nbUosFd):
        soldeAtos.write(xl_col_to_name(col) + str(row), dataTotUo[j][0], format_bon)
        soldeAtos.write(xl_col_to_name(col + 1) + str(row), dataTotUo[j][1], format_bon)
        soldeAtos.write(xl_col_to_name(col + 2) + str(row), dataTotUo[j][2], format_bon)
        soldeAtos.write(xl_col_to_name(col + 3) + str(row), '', format_sep)
        soldeAtos.write(xl_col_to_name(col) + str(row + 1), dataTotUo[j][3], format_bon)
        soldeAtos.write(xl_col_to_name(col + 1) + str(row + 1), '-', format_bon)
        soldeAtos.write(xl_col_to_name(col + 2) + str(row + 1), '-', format_bon)
        soldeAtos.write(xl_col_to_name(col + 3) + str(row + 1), '', format_sep)
        col += 4
    """--------------------------------------------------------------------------------------------------------------"""

    """------------------------------------------- Feuille Solde Egis -----------------------------------------------"""
    fds = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Fd", Boncomm.apm == "").all()
    fdEgis = triFd("EGIS", fds)
    uosFd = db.session.query(UO).filter(UO.type == "Fd").all()
    nbUosFd = len(uosFd)
    dataFdEgis = []
    dataTotUo = []
    for i in range(nbUosFd):
        dataTotUo.append([0, 0, 0, 0])
    for fd in fdEgis:
        dataToAdd = [fd]
        apms = db.session.query(Boncomm).filter(Boncomm.prodGdpOuFd == "Fd", Boncomm.apm != "",
                                                Boncomm.num == fd.num).all()  # Tous les apms liés à ce FD
        dataToAdd.append(apms[0].collabs[0].collab.entreprise)  # Entreprise lié à ce FD
        dataToAdd.append('20' + str(apms[0].num[-2:]))  # Année du FD
        dataToAdd.append(apms[0].client)  # Client lié à ce FD
        # collabs[0] car un seul collab lié à un FD
        dataUo = []
        for j in range(nbUosFd):
            uo = uosFd[j]
            data = []
            facteurFd = db.session.query(AssoUoBoncomm).filter(AssoUoBoncomm.uo_id == uo.id_uo,
                                                               AssoUoBoncomm.boncomm_id == fd.id_acti).all()[0].facteur
            data.append(facteurFd)
            dataTotUo[j][0] += facteurFd
            facteurAffecte = 0
            for apm in apms:
                facteurAffecte += db.session.query(AssoUoBoncomm).filter(
                    AssoUoBoncomm.uo_id == uo.id_uo, AssoUoBoncomm.boncomm_id == apm.id_acti).all()[0].facteur
            data.append(facteurAffecte)
            dataTotUo[j][1] += facteurAffecte
            data.append(facteurFd - facteurAffecte)
            dataTotUo[j][2] += (facteurFd - facteurAffecte)
            dataUo.append(data)
        dataToAdd.append(dataUo)
        dataFdEgis.append(dataToAdd)
    for j in range(nbUosFd):
        dataTotUo[j][3] = dataTotUo[j][0] * uosFd[j].prix

    """ ---------- Format et tailles des cellules ---------- """
    """----- Taille lignes et colonnes -----"""
    soldeEgis.set_column_pixels('A:A', 10)
    soldeEgis.set_column_pixels('B:B', 90)
    soldeEgis.set_column_pixels('H:H', 90)
    soldeEgis.set_row_pixels(0, 10)
    soldeEgis.set_row_pixels(5, 30)

    """ ---------- Création des lignes ---------- """
    """----- Titre feuille -----"""
    soldeEgis.write('B2', 'Solde réalisé Egis', format_titre)
    "----- En-têtes -----"
    soldeEgis.write('C6', 'Lot', format_entete)
    soldeEgis.write('D6', 'N°BC', format_entete)
    soldeEgis.write('E6', 'Poste', format_entete)
    soldeEgis.write('F6', 'Client', format_entete)
    soldeEgis.write('G6', 'Libellé', format_entete)
    soldeEgis.write('H6', 'Échéance', format_entete)
    soldeEgis.write('I6', 'État', format_entete)
    soldeEgis.set_column_pixels('J:J', 5)
    soldeEgis.write('J6', '', format_sep)
    col = 10
    for uo in uosFd:
        soldeEgis.merge_range(3, col, 3, col + 2, uo.description, format_entete)
        soldeEgis.merge_range(4, col, 4, col + 2, uo.prix, format_entete)
        soldeEgis.write(xl_col_to_name(col) + '6', 'BC', format_activite)
        soldeEgis.write(xl_col_to_name(col + 1) + '6', 'Affecté', format_activite)
        soldeEgis.write(xl_col_to_name(col + 2) + '6', 'Dispo', format_activite)
        soldeEgis.set_column_pixels(xl_col_to_name(col + 3) + ':' + xl_col_to_name(col + 3), 5)
        soldeEgis.write(xl_col_to_name(col + 3) + '6', '', format_sep)
        col += 4

    row = 7
    for fd in dataFdEgis:
        col = 1
        soldeEgis.write(xl_col_to_name(col) + str(row), str(fd[0].num) + str(fd[0].poste) + str(fd[1]), format_activite)
        soldeEgis.write(xl_col_to_name(col + 1) + str(row), fd[2], format_bon)
        soldeEgis.write(xl_col_to_name(col + 2) + str(row), fd[0].num, format_bon)
        soldeEgis.write(xl_col_to_name(col + 3) + str(row), fd[0].poste, format_bon)
        soldeEgis.write(xl_col_to_name(col + 4) + str(row), fd[3], format_bon)
        soldeEgis.write(xl_col_to_name(col + 5) + str(row), fd[0].activite, format_bon)
        soldeEgis.write(xl_col_to_name(col + 6) + str(row), fd[0].dateFinOp, format_bon)
        soldeEgis.write(xl_col_to_name(col + 7) + str(row), fd[0].etat, format_bon)
        soldeEgis.write(xl_col_to_name(col + 8) + str(row), '', format_sep)
        col = 10
        for i in range(nbUosFd):
            soldeEgis.write(xl_col_to_name(col) + str(row), fd[4][i][0], format_bon)
            soldeEgis.write(xl_col_to_name(col + 1) + str(row), fd[4][i][1], format_bon)
            soldeEgis.write(xl_col_to_name(col + 2) + str(row), fd[4][i][2], format_bon)
            soldeEgis.write(xl_col_to_name(col + 3) + str(row), '', format_sep)
            col += 4
        row += 1

    soldeEgis.write('I' + str(row), 'Total', format_entete)
    soldeEgis.write('I' + str(row + 1), 'Total UO revenus', format_entete)
    soldeEgis.write('J' + str(row), '', format_sep)
    soldeEgis.write('J' + str(row + 1), '', format_sep)
    col = 10
    for j in range(nbUosFd):
        soldeEgis.write(xl_col_to_name(col) + str(row), dataTotUo[j][0], format_bon)
        soldeEgis.write(xl_col_to_name(col + 1) + str(row), dataTotUo[j][1], format_bon)
        soldeEgis.write(xl_col_to_name(col + 2) + str(row), dataTotUo[j][2], format_bon)
        soldeEgis.write(xl_col_to_name(col + 3) + str(row), '', format_sep)
        soldeEgis.write(xl_col_to_name(col) + str(row + 1), dataTotUo[j][3], format_bon)
        soldeEgis.write(xl_col_to_name(col + 1) + str(row + 1), '-', format_bon)
        soldeEgis.write(xl_col_to_name(col + 2) + str(row + 1), '-', format_bon)
        soldeEgis.write(xl_col_to_name(col + 3) + str(row + 1), '', format_sep)
        col += 4
    """--------------------------------------------------------------------------------------------------------------"""

    workbook.close()
    return None
