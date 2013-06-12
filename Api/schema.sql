
--
-- lieu
--
drop table if exists place;
CREATE TABLE place(
  id INTEGER PRIMARY KEY autoincrement,
  name TEXT NOT NULL,
  description_FR TEXT NOT NULL,
  description_AN TEXT NOT NULL
  
);

--
-- service
--
drop table if exists service;
CREATE TABLE service(
  id INTEGER PRIMARY KEY autoincrement,
  name TEXT NOT NULL,
  description_FR TEXT NOT NULL,
  description_AN TEXT NOT NULL,
  building TEXT 
  
);

--
-- est_voisin_de
--
drop table if exists est_voisin_de;
CREATE TABLE est_voisin_de(
  id INTEGER PRIMARY KEY autoincrement,
  voisin1_id INTEGER,
  voisin2_id INTEGER,
  poids integer not null,
  FOREIGN KEY(voisin1_id) REFERENCES lieu(id),
  FOREIGN KEY(voisin2_id) REFERENCES lieu(id)

);

--
-- personne
--
drop table if exists PERSON;
CREATE TABLE PERSON(
   id INTEGER PRIMARY KEY autoincrement,
   name TEXT NOT NULL,
   firstname TEXT NOT NULL,
   function TEXT NOT NULL,
   bureau TEXT NOT NULL,
   phone TEXT NOT NULL,
   mail TEXT NOT NULL
   

  );
