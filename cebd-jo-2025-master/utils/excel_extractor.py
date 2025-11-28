import sqlite3
import pandas
from sqlite3 import IntegrityError

# Fonction permettant de lire le fichier Excel des JO et d'insérer les données dans la base


def read_excel_file_V0(data: sqlite3.Connection, file):

    # Pays
    print("pays")
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
    print("discipline")
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
    print("sportifs")
    # Lecture de l'onglet du fichier excel LesEpreuves, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into LesSportifs values ({},'{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # LesEpreuves
    print("epreuve")
    # Lecture de l'onglet LesEpreuves du fichier excel, en interprétant toutes les colonnes comme des string
    # pour construire uniformement la requête
    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:

            if row['dateEp'] != 'null':
                query = "insert into LesEpreuves values ({},'{}','{}','{}','{}',{},'{}')".format(
                    row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'], row['dateEp'])
            else:
                query = "insert into LesEpreuves values ({},'{}','{}','{}','{}',{},NULL)".format(
                    row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    # Equipe
    print("equipe")
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')
    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into Equipe values ({})".format(
                row['numEq'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Enroler
    print("enroler")
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into Enroler values ({},{})".format(
                row['numSp'], row['numEq'])
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Participe
    print("participe")
    # Lecture de l'onglet du fichier excel LesSportifsEQ, en interprétant toutes les colonnes comme des strings
    # pour construire uniformement la requête
    df_inscriptions = pandas.read_excel(
        file, sheet_name='LesInscriptions', dtype=str)
    df_inscriptions = df_inscriptions.where(
        pandas.notnull(df_inscriptions), 'null')

    cursor = data.cursor()
    for ix, row in df_inscriptions.iterrows():
        try:
            if int(row['numIn']) < 1000:
                cursor.execute("""
                SELECT numSp
                FROM Enroler
                WHERE numEq = ?;
                """, [row['numIn']])
                tab_inscri = {str(i[0]).strip() for i in cursor.fetchall()}
                # print(tab_inscri)
                for i in tab_inscri:
                    cursor.execute("insert or ignore into Participe values ({},{})".format(
                        int(i), row['numEp']))
                # print("if")
            else:
                # print("else1")
                query = "insert or ignore into Participe values ({},{})".format(
                    row['numIn'], row['numEp'])
                # print("else2")
            # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            # print(query)
                cursor.execute(query)
                # print("else3")
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

    tab_solo = {str(i[0]).strip() for i in cursor.fetchall()}
    # On affiche la requête pour comprendre la construction. A enlever une fois compris.

    for ix, row in df_resultats.iterrows():
        try:

            if row['numEp'] in tab_solo:
                query = "insert or ignore into Resultat values ('{}','{}','{}','{}',NULL,NULL,NULL)".format(
                    row['numEp'], row['gold'], row['silver'], row['bronze'])
                # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            else:
                query = "insert or ignore into Resultat values ('{}',NULL,NULL,NULL,'{}','{}','{}')".format(
                    row['numEp'], row['gold'], row['silver'], row['bronze'])
                # On affiche la requête pour comprendre la construction. A enlever une fois compris.
            cursor.execute(query)
        except IntegrityError as err:
            print(err)
