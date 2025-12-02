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
            if row['numEq'] == 'null':
                pass
            else:
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
            if row['numEq'] == 'null':
                pass
            else:
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

    print("fin insertion classque")
    # test trigger categorie_ep_sp
    print("test categorie_ep_sp")
    try :
        cursor.execute("""INSERT INTO Participe VALUES(1016, 3)""")
        cursor.execute("""INSERT INTO Participe VALUES(1017, 4)""")
        cursor.execute("""INSERT INTO Participe VALUES(1016, 1)""")
        cursor.execute("""INSERT INTO Participe VALUES(1017, 2)""")

        cursor.execute("SELECT * FROM Participe WHERE numSp = 1016")
        rows = cursor.fetchall()
        print("Participe numSp=1016:")
        for i in rows:
            print(i)

        cursor.execute("SELECT * FROM Participe WHERE numSp = 1017")
        rows = cursor.fetchall()
        print("Participe numSp=1017:")
        for i in rows:
            print(i)

    except IntegrityError as err:
            print("TRIGGER : categorie_ep_sp")

    # test trigger pays_eq
    print("test pays_eq")
    try :
        cursor.execute("""INSERT INTO Enroler VALUES(1003, 30)""")
        cursor.execute("SELECT * FROM Enroler WHERE numSp = 1003")
        rows = cursor.fetchall()
        print("Enroler numSp=1003:")
        for i in rows:
            print(i)

    except IntegrityError as err:
            print("TRIGGER : pays_eq")
    # test trigger date_sp_ep
    print("test  date_sp_ep")
    try :
        cursor.execute(
            """INSERT INTO LesSportifs VALUES(1500, 'Jean','Patrick','France','masculin','2026-01-01')""")
        cursor.execute("SELECT * FROM LesSportifs WHERE numSp = 1500")
        rows = cursor.fetchall()
        print("Sportif numSp=1500:")
        for i in rows:
            print(i)

        cursor.execute("""INSERT INTO Participe VALUES(1500, 1)""")
        cursor.execute("SELECT * FROM Participe WHERE numSp = 1500")
        rows = cursor.fetchall()
       # print("Participe numSp=1500:")
        for i in rows:
            print(i)
    except IntegrityError as err:
            print("TRIGGER : date_sp_ep")

    #test trigger NbPersParEquipe
    print("test NbPersParEquipe")
    try : 
        print("loutre 1")
        cursor.execute("""INSERT INTO Equipe VALUES(95)""")
        cursor.execute("""INSERT INTO Enroler VALUES(1500, 95)""")
        cursor.execute("""INSERT INTO Enroler VALUES(1002, 95)""")
        cursor.execute("SELECT * FROM Enroler WHERE numEq = 95")
        rows = cursor.fetchall()
       # print(" AVANT DELETE Enroler numEp = 95:")
        for i in rows:
            print(i)
        cursor.execute("""DELETE FROM Enroler WHERE numSp = 1002""")

        cursor.execute("SELECT * FROM Enroler WHERE numEq = 95")
        rows = cursor.fetchall()
        print("APRES DELETE Enroler numEp = 95:")
        for i in rows:
            print(i)
    except IntegrityError as err:
            print("TRIGGER : NbPersParEquipe")

    #test trigger NbParticipant
    print("test NbParticipant")
    try : 
        cursor.execute("""INSERT INTO LesEpreuves VALUES(50, 'Batman', 'individuelle', 'Ski alpin', 'mixte', NULL, '2020-04-06 00:00:00')""")
        cursor.execute("""INSERT INTO Participe VALUES(1017, 50)""")
        cursor.execute("""INSERT INTO Participe VALUES(1016, 50)""")
        cursor.execute("SELECT * FROM Participe WHERE numEp = 50")
        rows = cursor.fetchall()
        #print(" AVANT INSERT Participe numEp = 50:")
        for i in rows:
            print(i)
        cursor.execute("""INSERT INTO Resultat VALUES(50, 1017,1016, 1017, NULL, NULL, NULL)""")

        cursor.execute("SELECT * FROM Participe WHERE numEp = 50")
        rows = cursor.fetchall()
       # print("APRES INSERT Participe numEp = 50:")
        for i in rows:
            print(i)
    except IntegrityError as err:
            print("TRIGGER : NbParticipant")