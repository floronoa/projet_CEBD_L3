
CREATE TABLE Discipline IF NOT EXISTS
(
  nomDi VARCHAR2(25),
  CONSTRAINT Di_PK PRIMARY KEY (nomDi)
);

CREATE TABLE Pays IF NOT EXISTS
(
  pays VARCHAR2(20),
  CONSTRAINT Pa_PK PRIMARY KEY (pays)
);

CREATE TABLE LesSportifs IF NOT EXISTS
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SP_PK PRIMARY KEY (numSp),
  CONSTRAINT SP_FK_pa FOREIGN KEY Pays(pays),
  CONSTRAINT SP_CK1 CHECK(numSp > 999),
  CONSTRAINT SP_CK2 CHECK(numSp > 1001),
  CONSTRAINT SP_CK3 CHECK(categorieSp IN ('feminin','masculin'))
  
);

CREATE TABLE LesEpreuves IF NOT EXISTS
(
  numEp NUMBER(3),
  nomEp VARCHAR2(20),
  formeEp VARCHAR2(13),
  nomDi VARCHAR2(25),
  categorieEp VARCHAR2(10),
  nbSportifsEp NUMBER(2),
  dateEp DATE,
  CONSTRAINT EP_PK PRIMARY KEY (numEp),
  CONSTRAINT EP_FK_nd FOREIGN KEY Discipline(nomDi),
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 2)
);


CREATE TABLE Participe IF NOT EXISTS
(
  numSp NUMBER(4),
  numEp NUMBER(3),
  CONSTRAINT Pa_PK PRIMARY KEY (numSp,NumEp),
  CONSTRAINT PA_FK_Sp FOREIGN KEY LesSportifs(numSp),
  CONSTRAINT PA_FK_Ep FOREIGN KEY LesEpreuves(numEp)
);

CREATE TABLE Equipe IF NOT EXISTS
(
  numEq NUMBER(4),
  CONSTRAINT Eq_PK PRIMARY KEY (NumEq),
  CONSTRAINT Eq_CK1 CHECK (numEq > 0),
  CONSTRAINT Eq_CK2 CHECK (numEq < 101)
);

CREATE TABLE Enroler IF NOT EXISTS
( 
  numSp NUMBER(4),
  numEp NUMBER(4),
  CONSTRAINT En_PK PRIMARY KEY (numSp,NumEp),
  CONSTRAINT En_FK_Sp FOREIGN KEY LesSportifs(numSp),
  CONSTRAINT En_FK_Eq FOREIGN KEY Equipe(numEq)
);


CREATE TABLE Resultat IF NOT EXISTS
(
  numEp NUMBER(4),
  numOr NUMBER(4),
  numArgent NUMBER(4),
  numBronze NUMBER(4),
  CONSTRAINT Re_PK PRIMARY KEY (NumEp),
  CONSTRAINT Re_FK_Or FOREIGN KEY LesSportifs(numSp),
  CONSTRAINT Re_FK_Ar FOREIGN KEY LesSportifs(numSp),
  CONSTRAINT Re_FK_Br FOREIGN KEY LesSportifs(numSp)
);