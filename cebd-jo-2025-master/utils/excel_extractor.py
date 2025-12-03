import sqlite3
import pandas
from sqlite3 import IntegrityError

# Fonction permettant de lire le fichier Excel des JO et d'insérer les données dans la base


def read_excel_file_V0(data: sqlite3.Connection, file):

    # Pays
    print("Pays")

    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into Pays values ('{}')".format(
                row['pays'])

            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Discipline
    print("Discipline")

    df_epreuves = pandas.read_excel(
        file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            query = "insert or ignore into Discipline values ('{}')".format(
                row['nomDi'])

            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # LesSportifs
    print("LesSportifs")

    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            query = "insert or ignore into LesSportifs values ({},'{}','{}','{}','{}','{}')".format(
                row['numSp'], row['nomSp'], row['prenomSp'], row['pays'], row['categorieSp'], row['dateNaisSp'])

            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # LesEpreuves
    print("LesEpreuves")

    df_epreuves = pandas.read_excel(file, sheet_name='LesEpreuves', dtype=str)
    df_epreuves = df_epreuves.where(pandas.notnull(df_epreuves), 'null')

    cursor = data.cursor()
    for ix, row in df_epreuves.iterrows():
        try:
            # Gestion des dates NULL
            if row['dateEp'] != 'null':
                query = "insert into LesEpreuves values ({},'{}','{}','{}','{}',{},'{}')".format(
                    row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'], row['dateEp'])
            else:  # row['dateEp'] == 'null'
                query = "insert into LesEpreuves values ({},'{}','{}','{}','{}',{},NULL)".format(
                    row['numEp'], row['nomEp'], row['formeEp'], row['nomDi'], row['categorieEp'], row['nbSportifsEp'])

            cursor.execute(query)
        except IntegrityError as err:
            print(f"{err} : \n{row}")

    # Equipe
    print("Equipe")

    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')
    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            # Gestion des equipes NULL
            if row['numEq'] != 'null':
                query = "insert or ignore into Equipe values ({})".format(
                    row['numEq'])
                cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Enroler
    print("Enroler")

    df_sportifs = pandas.read_excel(
        file, sheet_name='LesSportifsEQ', dtype=str)
    df_sportifs = df_sportifs.where(pandas.notnull(df_sportifs), 'null')

    cursor = data.cursor()
    for ix, row in df_sportifs.iterrows():
        try:
            # Gestion des equipes NULL
            if row['numEq'] != 'null':
                query = "insert or ignore into Enroler values ({},{})".format(
                    row['numSp'], row['numEq'])
                cursor.execute(query)

        except IntegrityError as err:
            print(err)

    # Participe
    print("Participe")

    df_inscriptions = pandas.read_excel(
        file, sheet_name='LesInscriptions', dtype=str)
    df_inscriptions = df_inscriptions.where(
        pandas.notnull(df_inscriptions), 'null')

    cursor = data.cursor()
    for ix, row in df_inscriptions.iterrows():
        try:
            # Verifie si c'est une equipe ou un sportif qui s'inscrit
            # Si c'est une equipe, on inscrit tout les sportifs de l'equipe
            if int(row['numIn']) < 1000:
                cursor.execute("""
                SELECT numSp
                FROM Enroler
                WHERE numEq = ?;
                """, [row['numIn']])
                tab_inscri = {str(i[0]).strip() for i in cursor.fetchall()}
                for i in tab_inscri:
                    cursor.execute("insert or ignore into Participe values ({},{})".format(
                        int(i), row['numEp']))
            else:  # Inscription du sportif
                query = "insert or ignore into Participe values ({},{})".format(
                    row['numIn'], row['numEp'])
                cursor.execute(query)
        except IntegrityError as err:
            print(err)

    # Resultat
    print("Resultat")
    df_resultats = pandas.read_excel(
        file, sheet_name='LesResultats', dtype=str)
    df_resultats = df_resultats.where(pandas.notnull(df_resultats), 'null')

    # Recuperation des epreuves individuelle
    cursor = data.cursor()
    cursor.execute("""
    SELECT numEp
    FROM LesEpreuves
    WHERE formeEp = 'individuelle';
    """)

    tab_solo = {str(i[0]).strip() for i in cursor.fetchall()}

    for ix, row in df_resultats.iterrows():
        try:

            # Si c'est une epreuve individuelle, il n'y a pas de resultat d'equipe
            if row['numEp'] in tab_solo:
                query = "insert or ignore into Resultat values ('{}','{}','{}','{}',NULL,NULL,NULL)".format(
                    row['numEp'], row['gold'], row['silver'], row['bronze'])

            else:  # Si c'est une epreuve par equipe, il n'y a pas de resultat individuelle
                query = "insert or ignore into Resultat values ('{}',NULL,NULL,NULL,'{}','{}','{}')".format(
                    row['numEp'], row['gold'], row['silver'], row['bronze'])
            cursor.execute(query)
        except IntegrityError as err:
            print(err)

    print("Fin insertion du tableau excel")
