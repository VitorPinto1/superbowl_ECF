CREATE DATABASE IF NOT EXISTS bdsuperbowl;

USE bdsuperbowl;



CREATE TABLE IF NOT EXISTS matchs (
    id INT AUTO_INCREMENT,
    equipe1 VARCHAR(50),
    equipe2 VARCHAR(50),
    jour DATE,
    debut VARCHAR(10),
    fin VARCHAR(10) DEFAULT ' - ',
    statut VARCHAR(20) DEFAULT ' - ',
    score VARCHAR(10) DEFAULT ' - ',
    meteo VARCHAR(20) DEFAULT ' - ',
    cote1 INT,
    cote2 INT,
    commentaires VARCHAR(100) DEFAULT ' - ',
    but1 INT,
    but2 INT,
    vainqueur VARCHAR(50),
    PRIMARY KEY (id),
    UNIQUE KEY unique_match (equipe1, equipe2, jour)
);



CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom VARCHAR(255),
  prenom VARCHAR(255),
  email VARCHAR(255),
  mot_de_passe VARCHAR(255),
  token VARCHAR(255),
  confirmed BOOLEAN DEFAULT FALSE,
  role VARCHAR(50) DEFAULT 'user'
);

CREATE TABLE IF NOT EXISTS equipes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom_equipe VARCHAR(255),
  pays_appartenance VARCHAR(255),
  logo VARCHAR(255)
);



CREATE TABLE IF NOT EXISTS joueurs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom_joueur VARCHAR(255),
  prenom_joueur VARCHAR(255),
  numero_tshirt INT,
  equipe_id INT,
  FOREIGN KEY (equipe_id) REFERENCES equipes(id),
  CHECK (numero_tshirt BETWEEN 1 AND 99)
);



CREATE TABLE IF NOT EXISTS mises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mise1 DECIMAL(10, 2),
    mise2 DECIMAL(10, 2),
    resultat1 DECIMAL(10, 2),
    resultat2 DECIMAL(10, 2),
    equipe1 VARCHAR(50),
    equipe2 VARCHAR(50),
    cote1 INT,
    cote2 INT,
    id_match INT,
    datemise DATE,
    FOREIGN KEY (id_match) REFERENCES matchs(id),
    id_utilisateur INT,
    FOREIGN KEY (id_utilisateur) REFERENCES users(id)
);


DELIMITER //

CREATE TRIGGER actualizacion_fin_match
BEFORE INSERT ON matchs
FOR EACH ROW
BEGIN
    SET NEW.fin = DATE_FORMAT(DATE_ADD(STR_TO_DATE(NEW.debut, '%H:%i'), INTERVAL 1 HOUR), '%H:%i');
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER maj_score
BEFORE INSERT ON matchs
FOR EACH ROW
BEGIN
    SET NEW.score = CONCAT(NEW.but1, ' - ', NEW.but2);
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER maj_score_update
BEFORE UPDATE ON matchs
FOR EACH ROW
BEGIN
    SET NEW.score = CONCAT(NEW.but1, ' - ', NEW.but2);
END //

DELIMITER ;




INSERT IGNORE INTO equipes (nom_equipe, pays_appartenance, logo)
VALUES
  ('Arizona Cardinals', 'États Unis', 'sources/arizona_cardinals.png'),
  ('Atlanta Falcons', 'États Unis', 'sources/atlanta_falcons.png'),
  ('Baltimore Ravens', 'États Unis', 'sources/baltimore_ravens.png'),
  ('Buffalo Bills', 'États Unis', 'sources/buffalo_bills.png'),
  ('Carolina Panthers', 'États Unis', 'sources/carolina_panthers.png'),
  ('Chicago Bears', 'États Unis', 'sources/chicago_bears.png'),
  ('Cincinnati Bengals', 'États Unis', 'sources/cincinnati_bengals.png'),
  ('Cleveland Browns', 'États Unis', 'sources/cleveland_browns.png'),
  ('Dallas Cowboys', 'États Unis', 'sources/dallas-cowboys.png'),
  ('Denver Broncos', 'États Unis', 'sources/denver_broncos.png'),
  ('Detroit Lions', 'États Unis', 'sources/detroit_lions.png'),
  ('Green Bay Packers', 'États Unis', 'sources/green_bay_packers.png'),
  ('Houston Texans', 'États Unis', 'sources/houston_texans.png'),
  ('Indianapolis Colts', 'États Unis', 'sources/indianapolis_colts.png'),
  ('Jacksonville Jaguars', 'États Unis', 'sources/jacksonville_jaguars.png'),
  ('Kansas City Chiefs', 'États Unis', 'sources/kansas_city_chiefs.png'),
  ('Las Vegas Raiders', 'États Unis', 'sources/las_vegas_raiders.png'),
  ('Los Angeles Chargers', 'États Unis', 'sources/los_angeles__chargers.png'),
  ('Los Angeles Rams', 'États Unis', 'sources/los_angeles_rams.png'),
  ('Miami Dolphins', 'États Unis', 'sources/miami_dolphins.png'),
  ('Minnesota Vikings', 'États Unis', 'sources/minnesota_vikings.png'),
  ('New England Patriots', 'États Unis', 'sources/new_england_patriots.png'),
  ('New Orleans Saints', 'États Unis', 'sources/new_orleans_saints.png'),
  ('New York Giants', 'États Unis', 'sources/new_york_giants.png'),
  ('New York Jets', 'États Unis', 'sources/new_york_jets.png'),
  ('Philadelphia Eagles', 'États Unis', 'sources/philadelphia_eagles.png'),
  ('Pittsburgh Steelers', 'États Unis', 'sources/pittsburgh_steelers.png'),
  ('San Francisco 49ers', 'États Unis', 'sources/san_francisco_49ers.png'),
  ('Seattle Seahawks', 'États Unis', 'sources/seattle_seahawks.png'),
  ('Tampa Bay Buccaneers', 'États Unis', 'sources/tampa_bay_buccaneers.png'),
  ('Tennessee Titans', 'États Unis', 'sources/tennessee_titans.png'),
  ('Washington Commanders', 'États Unis', 'sources/washington_commanders.png');

