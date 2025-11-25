import sqlite3
import pandas
from sqlite3 import IntegrityError

# Fonction permettant de lire le fichier Excel des JO et d'insérer les données dans la base


def read_excel_file_V0(data: sqlite3.Connection, file):

    # Pays

    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into Pays values ('{}')".format(
                row['pays'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Discipline

    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(
        file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert or ignore into Discipline values ('{}')".format(
                row['nomDi'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # LesSportifs

    # Lecture de l'onglet du fichier excel LesEpreuves, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into LesSportifs values ('{}','{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # LesEpreuves

    # Lecture de l'onglet LesEpreuves du fichier excel, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert or ignore into LesEpreuves values ('{}','{}','{}','{}','{}','{}',".format(
                row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'])

            if row['dateEp'] != 'null':
                query = query + "'{}')".format(row['dateEp'])
            else:
                query = query + "null)"
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    # Participe

    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_inscriptions = pandas.read_excel(
        file, sheet_name='LesInscriptions', dtype=str)
    df_inscriptions = df_inscriptions.where(
        pandas.notnull(df_inscriptions), 'null')

    cursor = data.cursor()
    for ix, row in df_inscriptions.iterrows():
        try:
            query = "insert or ignore into Participe values ('{}','{}')".format(
                row['numIn'], row['numEp'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Equipe

    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')
    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into Equipe values ('{}')".format(
                row['numEq'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Enroler

    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into Enroler values ('{}','{}')".format(
                row['numSp'], row['numEq'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Resultat
    print("resultat")
    df_resultats = pandas.read_excel(
        file, sheet_name='LesResultats', dtype=str)
    df_resultats = df_resultats.where(pandas.notnull(df_resultats), 'null')

    cursor = data.cursor()
    cursor.execute("""
    SELECT numEp
    FROM LesEpreuves
    WHERE formeEp = 'individuelle';
    """)
    # Construire un ensemble de chaînes normalisées pour comparaison fiable avec pandas
    tab_solo = {str(i[0]).strip() for i in cursor.fetchall()}
    print(tab_solo)
    # On affiche la requête pour comprendre la construction. A enlever une fois compris.
    # print(query)
    print(tab_solo)

    for ix, row in df_resultats.iterrows():
        try:

            if row['numEp'] in tab_solo:
                print("try")
                query = "insert or ignore into Resultat values ('{}','{}','{}','{}','{}','{}','{}')".format(
                    row['numEp'], row['gold'], row['silver'], row['bronze'], None, None, None)
                # On affiche la requête pour comprendre la construction. A enlever une fois compris.
                # print(query)
                cursor.execute(query)
            else:
                query = "insert or ignore into Resultat values ('{}','{}','{}','{}','{}','{}','{}')".format(
                    row['numEp'],  None, None, None, row['gold'], row['silver'], row['bronze'])
                # On affiche la requête pour comprendre la construction. A enlever une fois compris.
                # print(query)
                cursor.execute(query)
        except IntegrityError as err:
            print(err)
