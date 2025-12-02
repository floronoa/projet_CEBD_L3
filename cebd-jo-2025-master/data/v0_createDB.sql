PRAGMA foreign_keys = ON /


CREATE TABLE IF NOT EXISTS Discipline 
(
  nomDi VARCHAR2(25),
  CONSTRAINT Di_PK PRIMARY KEY (nomDi)
)/

CREATE TABLE IF NOT EXISTS Pays 
(
  pays VARCHAR2(20),
  CONSTRAINT Pa_PK PRIMARY KEY (pays) 
)/

CREATE TABLE IF NOT EXISTS LesSportifs 
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SP_PK PRIMARY KEY (numSp),
  CONSTRAINT SP_FK_pa FOREIGN KEY (pays) REFERENCES Pays(pays) ON DELETE CASCADE,
  CONSTRAINT SP_CK1 CHECK(numSp > 999),
  CONSTRAINT SP_CK2 CHECK(numSp < 1501),
  CONSTRAINT SP_CK3 CHECK(categorieSp IN ('feminin','masculin'))
  
)/

CREATE TABLE IF NOT EXISTS LesEpreuves 
(
  numEp NUMBER(3),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  nomDi VARCHAR2(25),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  dateEp DATE,
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_FK_nd FOREIGN KEY (nomDi) REFERENCES Discipline(nomDi) ON DELETE CASCADE,
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 1)
)/

CREATE TABLE IF NOT EXISTS Participe 
(
  numSp NUMBER(4),
  numEp NUMBER(3),
  CONSTRAINT Pa_PK PRIMARY KEY (numSp,numEp),
  CONSTRAINT PA_FK_Sp FOREIGN KEY (numSp) REFERENCES LesSportifs(numSp) ON DELETE CASCADE,
  CONSTRAINT PA_FK_Ep FOREIGN KEY (numEp) REFERENCES LesEpreuves(numEp) ON DELETE CASCADE
)/

CREATE TABLE IF NOT EXISTS Equipe 
(
  numEq NUMBER(4),
  CONSTRAINT Eq_PK PRIMARY KEY (numEq),
  CONSTRAINT Eq_CK1 CHECK (numEq > 0) ,
  CONSTRAINT Eq_CK2 CHECK (numEq < 101) 
)/

CREATE TABLE IF NOT EXISTS Enroler 
( 
  numSp NUMBER(4),
  numEq NUMBER(3),
  CONSTRAINT En_PK PRIMARY KEY (numSp,numEq),
  CONSTRAINT En_FK_Sp FOREIGN KEY (numSp) REFERENCES LesSportifs(numSp) ON DELETE CASCADE,
  CONSTRAINT En_FK_Eq FOREIGN KEY (numEq) REFERENCES Equipe(numEq) ON DELETE CASCADE
)/

CREATE TABLE IF NOT EXISTS Resultat 
(
  numEp NUMBER(4),
  numOrSp NUMBER(4),
  numArgentSp NUMBER(4),
  numBronzeSp NUMBER(4),
  numOrEq NUMBER(3),
  numArgentEq NUMBER(3),
  numBronzeEq NUMBER(3),
  CONSTRAINT Re_PK PRIMARY KEY (numEp) ,
  CONSTRAINT Re_FK_Ep FOREIGN KEY (numEp) REFERENCES LesEpreuves(numEp) ON DELETE CASCADE,
  CONSTRAINT Re_FK_OrSp FOREIGN KEY (numOrSp) REFERENCES LesSportifs(numSp) ON DELETE CASCADE,
  CONSTRAINT Re_FK_ArSp FOREIGN KEY (numArgentSp) REFERENCES LesSportifs(numSp) ON DELETE CASCADE,
  CONSTRAINT Re_FK_BrSp FOREIGN KEY (numBronzeSp) REFERENCES LesSportifs(numSp) ON DELETE CASCADE,
  CONSTRAINT Re_FK_OrEq FOREIGN KEY (numOrEq) REFERENCES Equipe(numEq) ON DELETE CASCADE,
  CONSTRAINT Re_FK_ArEq FOREIGN KEY (numArgentEq) REFERENCES Equipe(numEq) ON DELETE CASCADE,
  CONSTRAINT Re_FK_BrEq FOREIGN KEY (numBronzeEq) REFERENCES Equipe(numEq) ON DELETE CASCADE
)/





--Créer une vue LesAgesSportifs (numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, ageSp)




CREATE VIEW IF NOT EXISTS LesAgesSportifs AS
SELECT numSp, nomSp, prenomSp, pays, categorieSp, dateNaisSp, ((strftime('%Y', 'now') - strftime('%Y', dateNaisSp)) - (strftime('%m-%d', 'now') < strftime('%m-%d', dateNaisSp))) AS ageSp
FROM LesSportifs /






-- Créer une vue LesNbsEquipiers(numEq, nbEquipiersEq)




CREATE VIEW IF NOT EXISTS LesNbsEquipiers AS
SELECT numEq, COUNT(numSp) AS nbEquipiersEq
FROM LesSportifs
JOIN Enroler USING(numSp)
GROUP BY numEq/







--Créer une vue calculant l’age moyen des équipes qui ont gagné une médaille d’or



CREATE VIEW IF NOT EXISTS AgeMoyEqOr AS
SELECT numOrEq, AVG(((strftime('%Y', 'now') - strftime('%Y', dateNaisSp)) - (strftime('%m-%d', 'now') < strftime('%m-%d', dateNaisSp)))) AS moyAge
FROM Resultat 
JOIN Enroler ON (numEq = numOrEq)
JOIN LesSportifs  USING (numSp)
GROUP BY numOrEq/




--Créer une vue donnant le classement des pays selon leur nombre de médailles (pays, nbOr, nbArgent, nbBronze)



CREATE VIEW IF NOT EXISTS ClassementPays AS
WITH nbMedailleOrEq AS (
    SELECT S1.pays, COUNT(DISTINCT numOrEq) AS nbOrEq
    FROM Resultat
    JOIN Enroler E1 ON (E1.numEq = numOrEq)
    JOIN LesSportifs S1 ON (S1.numSp = E1.numSp)
    GROUP BY S1.pays
),
nbMedailleArEq AS (
    SELECT S1.pays AS pays, COUNT(DISTINCT numArgentEq) AS nbArEq
    FROM Resultat
    JOIN Enroler E1 ON (E1.numEq = numArgentEq)
    JOIN LesSportifs S1 ON (S1.numSp = E1.numSp)
    GROUP BY S1.pays
),
nbMedailleBrEq AS(
    SELECT S1.pays AS pays, COUNT(DISTINCT numBronzeEq) AS nbBrEq
    FROM Resultat
    JOIN Enroler E1 ON (E1.numEq = numBronzeEq)
    JOIN LesSportifs S1 ON (S1.numSp = E1.numSp)
    GROUP BY S1.pays
),
nbMedailleOrSp AS (
    SELECT S1.pays AS pays, COUNT(numOrSp) AS nbOrSp
    FROM Resultat
    JOIN LesSportifs S1 ON (S1.numSp = numOrSp)
    GROUP BY S1.pays
),
nbMedailleArSp AS (
    SELECT S1.pays AS pays, COUNT(numArgentSp) AS nbArSp
    FROM Resultat
    JOIN LesSportifs S1 ON (S1.numSp = numArgentSp)
    GROUP BY S1.pays
),
nbMedailleBrSp AS (
    SELECT S1.pays AS pays, COUNT(numBronzeSp) AS nbBrSp
    FROM Resultat
    JOIN LesSportifs S1 ON (S1.numSp = numBronzeSp)
    GROUP BY S1.pays
)
SELECT pays, IFNULL(nbOrEq, 0) + IFNULL(nbOrSp, 0) AS nbOr, IFNULL(nbArEq, 0) + IFNULL(nbArSp, 0) AS nbArgent, IFNULL(nbBrEq, 0) + IFNULL(nbBrSp, 0) AS nbBronze
FROM Pays
LEFT JOIN nbMedailleOrEq USING(pays)
LEFT JOIN nbMedailleArEq USING(pays)
LEFT JOIN nbMedailleBrEq USING(pays)
LEFT JOIN nbMedailleOrSp USING(pays)
LEFT JOIN nbMedailleArSp USING(pays)
LEFT JOIN nbMedailleBrSp USING(pays)
ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC/







