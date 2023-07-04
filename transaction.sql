CREATE DATABASE IF NOT EXISTS bdsuperbowl;

USE bdsuperbowl;

CREATE TABLE IF NOT EXISTS matchs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    equipe1 VARCHAR(50),
    equipe2 VARCHAR(50),
    jour VARCHAR(10),
    debut VARCHAR(10),
    fin VARCHAR(10),
    statut VARCHAR(20),
    score VARCHAR(10),
    meteo VARCHAR(20),
    joueurs VARCHAR(100),
    cote1 VARCHAR(20),
    cote2 VARCHAR(20),
    commentaires VARCHAR(100),
    UNIQUE KEY (equipe1, equipe2)
);

TRUNCATE TABLE matchs;

INSERT IGNORE INTO matchs (equipe1, equipe2, jour, debut, fin, statut, score, meteo, joueurs, cote1, cote2, commentaires)
VALUES
    ('Kansas City Chiefs', 'Dallas Cowboys', '23/05', '09:00', '11:00', 'En cours', '4-2', 'soleil', 'pepe', '500$', '200$', 'el mejor jugador'),
    ('New England Patriots', 'Green Bay Packers', '24/05', '08:00', '10:00', 'Terminé', '0-3', 'pluie', 'batista', '400$', '200$', 'que rule'),
    ('Pittsburgh Steelers', 'San Francisco 49ers', '29/05', '10:00', '12:00', 'À venir', '', 'horage', 'ronaldinho', '2000$', '200$', 'El gaucho');


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

CREATE TABLE IF NOT EXISTS joueurs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom_joueur VARCHAR(255),
  prenom_joueur VARCHAR(255),
  numero_tshirt INT,
  equipe_id INT,
  FOREIGN KEY (equipe_id) REFERENCES equipes(id),
  CHECK (numero_tshirt BETWEEN 1 AND 99)
);

CREATE TABLE IF NOT EXISTS equipes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nom_equipe VARCHAR(255),
  pays_appartenance VARCHAR(255)
);



CREATE TABLE IF NOT EXISTS mises (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mise1 DECIMAL(10, 2),
    mise2 DECIMAL(10, 2),
    resultat1 VARCHAR(20),
    resultat2 VARCHAR(20),
    equipe1 VARCHAR(50),
    equipe2 VARCHAR(50),
    cote1 VARCHAR(20),
    cote2 VARCHAR(20),
    id_match INT,
    FOREIGN KEY (id_match) REFERENCES matchs(id),
    id_utilisateur INT,
    FOREIGN KEY (id_utilisateur) REFERENCES users(id)
);