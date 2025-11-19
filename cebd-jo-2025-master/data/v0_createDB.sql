
CREATE TABLE IF NOT EXISTS Discipline 
(
  nomDi VARCHAR2(25),
  CONSTRAINT Di_PK PRIMARY KEY (nomDi)
);

CREATE TABLE IF NOT EXISTS Pays 
(
  pays VARCHAR2(20),
  CONSTRAINT Pa_PK PRIMARY KEY (pays)
);

CREATE TABLE IF NOT EXISTS LesSportifs 
(
  numSp NUMBER(4),
  nomSp VARCHAR2(20),
  prenomSp VARCHAR2(20),
  pays VARCHAR2(20),
  categorieSp VARCHAR2(10),
  dateNaisSp DATE,
  CONSTRAINT SP_PK PRIMARY KEY (numSp),
  CONSTRAINT SP_FK_pa FOREIGN KEY (pays) REFERENCES Pays(pays),
  CONSTRAINT SP_CK1 CHECK(numSp > 999),
  CONSTRAINT SP_CK2 CHECK(numSp < 1501),
  CONSTRAINT SP_CK3 CHECK(categorieSp IN ('feminin','masculin'))
  
);

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
  CONSTRAINT EP_FK_nd FOREIGN KEY (nomDi) REFERENCES Discipline(nomDi),
  CONSTRAINT EP_CK1 CHECK (formeEp IN ('individuelle','par equipe','par couple')),
  CONSTRAINT EP_CK2 CHECK (categorieEp IN ('feminin','masculin','mixte')),
  CONSTRAINT EP_CK3 CHECK (numEp > 0),
  CONSTRAINT EP_CK4 CHECK (nbSportifsEp > 2)
);

CREATE TABLE IF NOT EXISTS Participe 
(
  numSp NUMBER(4),
  numEp NUMBER(3),
  CONSTRAINT Pa_PK PRIMARY KEY (numSp,numEp),
  CONSTRAINT PA_FK_Sp FOREIGN KEY (numSp) REFERENCES LesSportifs(numSp),
  CONSTRAINT PA_FK_Ep FOREIGN KEY (numEp) REFERENCES LesEpreuves(numEp)
);

CREATE TABLE IF NOT EXISTS Equipe 
(
  numEq NUMBER(4),
  CONSTRAINT Eq_PK PRIMARY KEY (numEq),
  CONSTRAINT Eq_CK1 CHECK (numEq > 0),
  CONSTRAINT Eq_CK2 CHECK (numEq < 101)
);

CREATE TABLE IF NOT EXISTS Enroler 
( 
  numSp NUMBER(4),
  numEq NUMBER(3),
  CONSTRAINT En_PK PRIMARY KEY (numSp,numEq),
  CONSTRAINT En_FK_Sp FOREIGN KEY (numSp) REFERENCES LesSportifs(numSp),
  CONSTRAINT En_FK_Eq FOREIGN KEY (numEq) REFERENCES Equipe(numEq)
);

CREATE TABLE IF NOT EXISTS Resultat 
(
  numEp NUMBER(4),
  numOrSp NUMBER(4),
  numArgentSp NUMBER(4),
  numBronzeSp NUMBER(4),
  numOrEq NUMBER(3),
  numArgentEq NUMBER(3),
  numBronzeEq NUMBER(3),
  CONSTRAINT Re_PK PRIMARY KEY (numEp),
  CONSTRAINT Re_FK_OrSp FOREIGN KEY (numOrSp) REFERENCES LesSportifs(numSp),
  CONSTRAINT Re_FK_ArSp FOREIGN KEY (numArgentSp) REFERENCES LesSportifs(numSp),
  CONSTRAINT Re_FK_BrSp FOREIGN KEY (numBronzeSp) REFERENCES LesSportifs(numSp),
  CONSTRAINT Re_FK_OrEq FOREIGN KEY (numOrEq) REFERENCES Equipe(numEq),
  CONSTRAINT Re_FK_ArEq FOREIGN KEY (numArgentEq) REFERENCES Equipe(numEq),
  CONSTRAINT Re_FK_BrEq FOREIGN KEY (numBronzeEq) REFERENCES Equipe(numEq)
);