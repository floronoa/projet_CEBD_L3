PRAGMA foreign_keys = ON /

--CREATE TRIGGER

-- Verifie si les membre d'une equipe vienne du meme pays

CREATE TRIGGER IF NOT EXISTS Pays_Eq
BEFORE INSERT ON Enroler
FOR EACH ROW
WHEN EXISTS (
  SELECT 1
  FROM Enroler E
  JOIN LesSportifs S ON E.numSp = S.numSp
  WHERE E.numEq = NEW.numEq
    AND S.pays != (SELECT pays 
      FROM LesSportifs 
      WHERE numSp = NEW.numSp)
)
BEGIN
  SELECT RAISE(ABORT, "Les membres d'une équipe doivent venir du même pays");
END/


-- Verifie si un sportif s'inscrit dans la bonne categorie


CREATE TRIGGER IF NOT EXISTS Categorie_Ep_Sp
BEFORE INSERT ON Participe
FOR EACH ROW
WHEN EXISTS (
  SELECT 1
  FROM LesEpreuves E
  WHERE E.numEp = NEW.numEp
    AND E.categorieEp != 'mixte'
    AND E.categorieEp != (SELECT categorieSp 
      FROM LesSportifs 
      WHERE numSp = NEW.numSp)
)
BEGIN
  SELECT RAISE(ABORT, "Le sportif ne correspond pas à la catégorie de l'épreuve");
END/


-- Verifie si dateNaisSp > dateEp


CREATE TRIGGER IF NOT EXISTS Date_Sp_Ep
BEFORE INSERT ON Participe
FOR EACH ROW
WHEN EXISTS (
  SELECT 1
  FROM LesEpreuves E
  WHERE E.numEp = NEW.numEp
    AND E.dateEp < (SELECT dateNaisSp 
      FROM LesSportifs 
      WHERE numSp = NEW.numSp)
)
BEGIN
  SELECT RAISE(ABORT, "Le sportif ne peut pas participer à une épreuve avant sa naissance");
END/
-- Verifie si le nombre de personne dans une equipe est superieur à deux

CREATE TRIGGER IF NOT EXISTS  NbSportifEquipe
AFTER DELETE ON Enroler
FOR EACH ROW
WHEN EXISTS (
  SELECT 1
  FROM Enroler
  GROUP BY numEq
  HAVING COUNT(numSp) < 2 AND OLD.numEq = numEq 
  )
BEGIN
  SELECT RAISE (ABORT , "ntm joe");
END/

-- Verifie si le nombre d'inscrit dans une epreuve permet d'avoir resultat

CREATE TRIGGER IF NOT EXISTS  NbParticpant
BEFORE INSERT ON Resultat
FOR EACH ROW
WHEN EXISTS (
 SELECT 1
 FROM Participe
 GROUP BY numEp
 HAVING COUNT(numSP) < 3 AND NEW.numEp = numEp
)
BEGIN
  SELECT RAISE (ABORT , "Une épreuve s'est terminé sans avoir assez de participant");
END/
