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
  equipe_id VARCHAR(255),
  FOREIGN KEY (equipe_id) REFERENCES equipes(nom_equipe),
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

-- Código del disparador aquí
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

ALTER TABLE equipes ADD UNIQUE KEY unique_nom_equipe (nom_equipe);


INSERT IGNORE INTO equipes (nom_equipe, pays_appartenance, logo)
VALUES
  ('Arizona Cardinals', 'États Unis', NULL),
  ('Atlanta Falcons', 'États Unis', NULL),
  ('Baltimore Ravens', 'États Unis', NULL),
  ('Buffalo Bills', 'États Unis', NULL),
  ('Carolina Panthers', 'États Unis', NULL),
  ('Chicago Bears', 'États Unis', NULL),
  ('Cincinnati Bengals', 'États Unis', 'sources/cincinnati_bengals.png'),
  ('Cleveland Browns', 'États Unis', NULL),
  ('Dallas Cowboys', 'États Unis', NULL),
  ('Denver Broncos', 'États Unis', NULL),
  ('Detroit Lions', 'États Unis', NULL),
  ('Green Bay Packers', 'États Unis', NULL),
  ('Houston Texans', 'États Unis', NULL),
  ('Indianapolis Colts', 'États Unis', NULL),
  ('Jacksonville Jaguars', 'États Unis', NULL),
  ('Kansas City Chiefs', 'États Unis', NULL),
  ('Las Vegas Raiders', 'États Unis', NULL),
  ('Los Angeles Chargers', 'États Unis', NULL),
  ('Los Angeles Rams', 'États Unis', NULL),
  ('Miami Dolphins', 'États Unis', NULL),
  ('Minnesota Vikings', 'États Unis', NULL),
  ('New England Patriots', 'États Unis', NULL),
  ('New Orleans Saints', 'États Unis', NULL),
  ('New York Giants', 'États Unis', NULL),
  ('New York Jets', 'États Unis', NULL),
  ('Philadelphia Eagles', 'États Unis', NULL),
  ('Pittsburgh Steelers', 'États Unis', NULL),
  ('San Francisco 49ers', 'États Unis', NULL),
  ('Seattle Seahawks', 'États Unis', NULL),
  ('Tampa Bay Buccaneers', 'États Unis', NULL),
  ('Tennessee Titans', 'États Unis', NULL),
  ('Washington Commanders', 'États Unis', NULL);

