import sys
from utils import db
from utils import excel_extractor
from sqlite3 import IntegrityError

# Fonction permettant de créer la base de données


def database_create(data):
    print("\nCréation de la base de données")
    try:
        # On exécute les requêtes du fichier de création
        db.updateDBfile(data, "data/v0_createDB.sql")

        db.updateDBfile(data, "data/triggers.sql", True)
    except Exception as e:
        # En cas d'erreur, on affiche un message
        print("L'erreur suivante s'est produite pendant lors de la création de la base : " + repr(e) + ".")
    else:
        # Si tout s'est bien passé, on affiche le message de succès et on commit
        print("La base de données a été créée avec succès.")
        data.commit()

# Fonction permettant d'insérer les données dans la base


def database_insert(data):
    print("\nInsertion des données dans la base.")
    try:
        # on lit les données dans le fichier Excel
        excel_extractor.read_excel_file_V0(data, "data/LesJO.xlsx")
    except Exception as e:
        # En cas d'erreur, on affiche un message
        print("L'erreur suivante s'est produite lors de l'insertion des données : " +
              repr(e) + ".", file=sys.stderr)
    else:
        # Si tout s'est bien passé, on affiche le message de succès et on commit
        print("Un jeu de test a été inséré dans la base avec succès.")
        data.commit()

# Fonction permettant de supprimer la base de données


def database_delete(data):
    print("\nSuppression de la base de données.")
    try:
        # On exécute les requêtes du fichier de suppression
        db.updateDBfile(data, "data/v0_deleteDB.sql")
    except Exception as e:
        # En cas d'erreur, on affiche un message
        print("Erreur lors de la suppression de la base de données : " + repr(e) + ".")
    else:
        # Si tout s'est bien passé, on affiche le message de succès (le commit est automatique pour un DROP TABLE)
        print("La base de données a été supprimée avec succès.")

# Fonction permettant de teste les triggers et les contrainte on cascade


def database_test(data):
    print("\nLancement des jeux de tests.")
    print("\n---------------------------------\n")

    # Test trigger categorie_ep_sp
    cursor = data.cursor()
    print("Test categorie_ep_sp")
    print("INSERT INTO Participe VALUES(1016, 3)")
    try:
        cursor.execute("""INSERT INTO Participe VALUES(1016, 3)""")
        print("Insertion reussie")

    except IntegrityError as err:
        print("TRIGGER : categorie_ep_sp")

    print("INSERT INTO Participe VALUES(1017, 4)")
    try:

        cursor.execute("""INSERT INTO Participe VALUES(1017, 4)""")
        print("Insertion reussie")

    except IntegrityError as err:
        print("TRIGGER : categorie_ep_sp")

    print("INSERT INTO Participe VALUES(1016, 1)")
    try:

        cursor.execute("""INSERT INTO Participe VALUES(1016, 1)""")
        print("Insertion reussie (voulu epreuve mixte)")

    except IntegrityError as err:
        print("TRIGGER : categorie_ep_sp")

    print("INSERT INTO Participe VALUES(1016, 3)")
    try:
        cursor.execute("""INSERT INTO Participe VALUES(1017, 2)""")
        print("Insertion reussie (voulu epreuve mixte)")

    except IntegrityError as err:
        print("TRIGGER : categorie_ep_sp")

    # Test trigger pays_eq
    print("\n---------------------------------\n")
    print("Test pays_eq")

    print("INSERT INTO Enroler VALUES(1003, 30)")
    try:

        cursor.execute("""INSERT INTO Enroler VALUES(1003, 30)""")
        cursor.execute("SELECT * FROM Enroler WHERE numSp = 1003")
        rows = cursor.fetchall()
        print("Enroler numSp=1003:")
        for i in rows:
            print(i)

    except IntegrityError as err:
        print("TRIGGER : pays_eq")

    # Test trigger date_sp_ep
    print("\n---------------------------------\n")
    print("Test  date_sp_ep")
    print("INSERT INTO LesSportifs VALUES(1500, 'Jean','Patrick','France','masculin','2026-01-01')")
    cursor.execute(
        """INSERT INTO LesSportifs VALUES(1500, 'Jean','Patrick','France','masculin','2026-01-01')""")

    print("INSERT INTO Participe VALUES(1500, 1)")
    try:
        cursor.execute("""INSERT INTO Participe VALUES(1500, 1)""")
        cursor.execute("SELECT * FROM Participe WHERE numSp = 1500")
        rows = cursor.fetchall()
        for i in rows:
            print(i)

    except IntegrityError as err:
        print("TRIGGER : date_sp_ep")

    # Test trigger Nb_Sp_Eq
    print("\n---------------------------------\n")
    print("Test Nb_Sp_Eq")
    print("INSERT INTO Equipe VALUES(95)")
    print("INSERT INTO Enroler VALUES(1500, 95)")
    print("INSERT INTO Enroler VALUES(1002, 95)")

    print("DELETE FROM Enroler WHERE numSp = 1002")
    try:
        cursor.execute("""INSERT INTO Equipe VALUES(95)""")
        cursor.execute("""INSERT INTO Enroler VALUES(1500, 95)""")
        cursor.execute("""INSERT INTO Enroler VALUES(1002, 95)""")

        cursor.execute("""DELETE FROM Enroler WHERE numSp = 1002""")

        cursor.execute("SELECT * FROM Enroler WHERE numEq = 95")
        rows = cursor.fetchall()
        print("APRES DELETE Enroler numEp = 95:")
        for i in rows:
            print(i)
    except IntegrityError as err:
        print("TRIGGER : Nb_Sp_Eq")

    # Test trigger NbParticipant
    print("\n---------------------------------\n")
    print("Test Nb_Participant")
    print(
        """INSERT INTO LesEpreuves VALUES(50, 'Chute acrobatique', 'individuelle', 'Ski alpin', 'mixte', NULL, '2020-04-06 00:00:00')""")
    print("""INSERT INTO Participe VALUES(1017, 50)""")
    print("""INSERT INTO Participe VALUES(1016, 50)""")
    print(
        """INSERT INTO Resultat VALUES(50, 1017,1016, 1017, NULL, NULL, NULL)""")

    try:
        cursor.execute(
            """INSERT INTO LesEpreuves VALUES(50, 'Chute acrobatique', 'individuelle', 'Ski alpin', 'mixte', NULL, '2020-04-06 00:00:00')""")
        cursor.execute("""INSERT INTO Participe VALUES(1017, 50)""")
        cursor.execute("""INSERT INTO Participe VALUES(1016, 50)""")
        cursor.execute(
            """INSERT INTO Resultat VALUES(50, 1017,1016, 1017, NULL, NULL, NULL)""")

        cursor.execute("SELECT * FROM Participe WHERE numEp = 50")
        rows = cursor.fetchall()
        for i in rows:
            print(i)
    except IntegrityError as err:
        print("TRIGGER : Nb_Participant")

    print("\n---------------------------------\n")
    print("Test delete on cascade")
    cursor.execute(
        "SELECT * FROM LesSportifs WHERE pays = 'Japon' AND numSp = 1192")
    rows = cursor.fetchall()
    print(" AVANT DELETE JAPON SPORTIFS ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute("SELECT * FROM Enroler WHERE numSp = 1192")
    rows = cursor.fetchall()
    print(" AVANT DELETE JAPON ENROLER ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute("SELECT * FROM participe WHERE numSp = 1192")
    rows = cursor.fetchall()
    print(" AVANT DELETE JAPON PARTICIPE ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute("""DELETE FROM Pays WHERE pays = 'Japon'""")
    cursor.execute(
        "SELECT * FROM LesSportifs WHERE pays = 'Japon' AND numSp = 1192")
    rows = cursor.fetchall()
    print(" APRES DELETE JAPON SPORTIFS ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute("SELECT * FROM Enroler WHERE numSp = 1192")
    rows = cursor.fetchall()
    print(" APRES DELETE JAPON ENROLER ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute("SELECT * FROM participe WHERE numSp = 1192")
    rows = cursor.fetchall()
    print(" APRES DELETE JAPON PARTICIPE ")
    for i in rows:
        print(i)
    print("\n")

    print("\n---------------------------------\n")

    print("\nTest delete on cascade - Discipline\n")
    cursor.execute(
        "SELECT * FROM Discipline WHERE nomDi = 'Patinage artistique'")
    rows = cursor.fetchall()
    print(" AVANT DELETE Patinage DISCIPLINE ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute(
        "SELECT * FROM LesEpreuves WHERE nomDi = 'Patinage artistique'")
    rows = cursor.fetchall()
    print(" AVANT DELETE Patinage Epreuves ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute(
        "SELECT * FROM Resultat WHERE numEp IN (SELECT numEp FROM LesEpreuves WHERE nomDi = 'Patinage artistique')")
    rows = cursor.fetchall()
    print(" AVANT DELETE Patinage RESULTATE ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute(
        """DELETE FROM Discipline WHERE nomDi = 'Patinage artistique'""")
    cursor.execute(
        "SELECT * FROM Discipline WHERE nomDi = 'Patinage artistique'")
    rows = cursor.fetchall()
    print(" APRES DELETE Patinage DISCIPLINE ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute(
        "SELECT * FROM LesEpreuves WHERE nomDi = 'Patinage artistique'")
    rows = cursor.fetchall()
    print(" APRES DELETE Patinage Epreuves ")
    for i in rows:
        print(i)
    print("\n")
    cursor.execute(
        "SELECT * FROM Resultat WHERE numEp IN (SELECT numEp FROM LesEpreuves WHERE nomDi = 'Patinage artistique')")
    rows = cursor.fetchall()
    print(" APRES DELETE Patinage RESULTATE ")
    for i in rows:
        print(i)
    print("\n")

    data.commit()
