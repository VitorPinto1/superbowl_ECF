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
  pays_appartenance VARCHAR(255)
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


INSERT INTO equipes (nom_equipe, pays_appartenance)
VALUES
  ('Arizona Cardinals', 'États Unis'),
  ('Atlanta Falcons', 'États Unis'),
  ('Baltimore Ravens', 'États Unis'),
  ('Buffalo Bills', 'États Unis'),
  ('Carolina Panthers', 'États Unis'),
  ('Chicago Bears', 'États Unis'),
  ('Cincinnati Bengals', 'États Unis'),
  ('Cleveland Browns', 'États Unis'),
  ('Dallas Cowboys', 'États Unis'),
  ('Denver Broncos', 'États Unis'),
  ('Detroit Lions', 'États Unis'),
  ('Green Bay Packers', 'États Unis'),
  ('Houston Texans', 'États Unis'),
  ('Indianapolis Colts', 'États Unis'),
  ('Jacksonville Jaguars', 'États Unis'),
  ('Kansas City Chiefs', 'États Unis'),
  ('Las Vegas Raiders', 'États Unis'),
  ('Los Angeles Chargers', 'États Unis'),
  ('Los Angeles Rams', 'États Unis'),
  ('Miami Dolphins', 'États Unis'),
  ('Minnesota Vikings', 'États Unis'),
  ('New England Patriots', 'États Unis'),
  ('New Orleans Saints', 'États Unis'),
  ('New York Giants', 'États Unis'),
  ('New York Jets', 'États Unis'),
  ('Philadelphia Eagles', 'États Unis'),
  ('Pittsburgh Steelers', 'États Unis'),
  ('San Francisco 49ers', 'États Unis'),
  ('Seattle Seahawks', 'États Unis'),
  ('Tampa Bay Buccaneers', 'États Unis'),
  ('Tennessee Titans', 'États Unis'),
  ('Washington Commanders', 'États Unis');

