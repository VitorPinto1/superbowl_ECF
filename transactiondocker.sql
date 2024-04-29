-- MySQL dump 10.13  Distrib 8.0.33, for macos13 (arm64)
--
-- Host: localhost    Database: bdsuperbowl
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `equipes`
--

DROP TABLE IF EXISTS `equipes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_equipe` varchar(255) DEFAULT NULL,
  `pays_appartenance` varchar(255) DEFAULT NULL,
  `logo` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_nom_equipe` (`nom_equipe`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipes`
--

LOCK TABLES `equipes` WRITE;
/*!40000 ALTER TABLE `equipes` DISABLE KEYS */;
INSERT INTO `equipes` VALUES (1,'Arizona Cardinals','États Unis','sources/arizona_cardinals.png'),(2,'Atlanta Falcons','États Unis','sources/atlanta_falcons.png'),(3,'Baltimore Ravens','États Unis','sources/baltimore_ravens.png'),(4,'Buffalo Bills','États Unis','sources/buffalo_bills.png'),(5,'Carolina Panthers','États Unis','sources/carolina_panthers.png'),(6,'Chicago Bears','États Unis','sources/chicago_bears.png'),(7,'Cincinnati Bengals','États Unis','sources/cincinnati_bengals.png'),(8,'Cleveland Browns','États Unis','sources/cleveland_browns.png'),(9,'Dallas Cowboys','États Unis','sources/dallas-cowboys.png'),(10,'Denver Broncos','États Unis','sources/denver_broncos.png'),(11,'Detroit Lions','États Unis','sources/detroit_lions.png'),(12,'Green Bay Packers','États Unis','sources/green_bay_packers.png'),(13,'Houston Texans','États Unis','sources/houston_texans.png'),(14,'Indianapolis Colts','États Unis','sources/indianapolis_colts.png'),(15,'Jacksonville Jaguars','États Unis','sources/jacksonville_jaguars.png'),(16,'Kansas City Chiefs','États Unis','sources/kansas_city_chiefs.png'),(17,'Las Vegas Raiders','États Unis','sources/las_vegas_raiders.png'),(18,'Los Angeles Chargers','États Unis','sources/los_angeles__chargers.png'),(19,'Los Angeles Rams','États Unis','sources/los_angeles_rams.png'),(20,'Miami Dolphins','États Unis','sources/miami_dolphins.png'),(21,'Minnesota Vikings','États Unis','sources/minnesota_vikings.png'),(22,'New England Patriots','États Unis','sources/new_england_patriots.png'),(23,'New Orleans Saints','États Unis','sources/new_orleans_saints.png'),(24,'New York Giants','États Unis','sources/new_york_giants.png'),(25,'New York Jets','États Unis','sources/new_york_jets.png'),(26,'Philadelphia Eagles','États Unis','sources/philadelphia_eagles.png'),(27,'Pittsburgh Steelers','États Unis','sources/pittsburgh_steelers.png'),(28,'San Francisco 49ers','États Unis','sources/san_francisco_49ers.png'),(29,'Seattle Seahawks','États Unis','sources/seattle_seahawks.png'),(30,'Tampa Bay Buccaneers','États Unis','sources/tampa_bay_buccaneers.png'),(31,'Tennessee Titans','États Unis','sources/tennessee_titans.png'),(32,'Washington Commanders','États Unis','sources/washington_commanders.png');
/*!40000 ALTER TABLE `equipes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `joueurs`
--

DROP TABLE IF EXISTS `joueurs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `joueurs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom_joueur` varchar(255) DEFAULT NULL,
  `prenom_joueur` varchar(255) DEFAULT NULL,
  `numero_tshirt` int DEFAULT NULL,
  `equipe_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `equipe_id` (`equipe_id`),
  CONSTRAINT `joueurs_ibfk_1` FOREIGN KEY (`equipe_id`) REFERENCES `equipes` (`id`),
  CONSTRAINT `joueurs_chk_1` CHECK ((`numero_tshirt` between 1 and 99))
) ENGINE=InnoDB AUTO_INCREMENT=353 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `joueurs`
--

LOCK TABLES `joueurs` WRITE;
/*!40000 ALTER TABLE `joueurs` DISABLE KEYS */;
INSERT INTO `joueurs` VALUES (1,'Jonathan','Levine',4,1),(2,'Susan','Hill',73,1),(3,'Marissa','Martin',4,1),(4,'John','Rogers',11,1),(5,'Matthew','Travis',98,1),(6,'Alejandro','Bell',49,1),(7,'Tammy','Collins',45,1),(8,'Joseph','Hammond',17,1),(9,'Bradley','Hernandez',48,1),(10,'Amanda','Hill',11,1),(11,'Jose','Horton',34,1),(12,'Kelly','Ramirez',9,2),(13,'Stephanie','Hodges',62,2),(14,'Joshua','Anderson',13,2),(15,'Tina','Jones',8,2),(16,'Joshua','Rowland',71,2),(17,'Calvin','Williamson',60,2),(18,'Mark','Kim',43,2),(19,'Carla','Bell',17,2),(20,'Mark','Johnson',12,2),(21,'Bryan','Smith',74,2),(22,'Steven','Martin',37,2),(23,'Daniel','Hubbard',47,3),(24,'Clarence','Herman',57,3),(25,'Jonathan','Garcia',51,3),(26,'Amber','Peterson',12,3),(27,'Nichole','Weber',43,3),(28,'Kimberly','Chen',46,3),(29,'Theodore','Santiago',48,3),(30,'Nicole','Williams',3,3),(31,'David','Bell',91,3),(32,'Daniel','Howell',18,3),(33,'Steven','Smith',36,3),(34,'Thomas','Morrison',5,4),(35,'Amber','Johnson',86,4),(36,'Jonathan','Harper',95,4),(37,'Brianna','Williams',60,4),(38,'Matthew','Williams',76,4),(39,'Christina','Jackson',96,4),(40,'Robert','Sparks',48,4),(41,'Deborah','Harding',42,4),(42,'David','King',76,4),(43,'Samantha','Adams',53,4),(44,'William','Walls',17,4),(45,'Sydney','Flores',93,5),(46,'Christopher','Hughes',5,5),(47,'Robert','Smith',2,5),(48,'Maria','Miller',35,5),(49,'Adam','Ellis',91,5),(50,'Cameron','Barrera Jr.',20,5),(51,'Megan','James',76,5),(52,'Brittany','Franklin',22,5),(53,'Jason','Hunter',12,5),(54,'Mr.','Mark Hughes',10,5),(55,'Michelle','Jefferson',89,5),(56,'Dawn','Sanchez',46,6),(57,'Rita','Mendoza',31,6),(58,'Raymond','White',72,6),(59,'Kimberly','Summers',99,6),(60,'Zachary','Brooks',79,6),(61,'Thomas','Sanchez',12,6),(62,'Julie','Hicks',23,6),(63,'Larry','Mathews',87,6),(64,'Laura','Myers',30,6),(65,'Brianna','Tran',67,6),(66,'Melissa','Vasquez',1,6),(67,'Mary','Zimmerman',58,7),(68,'Edward','Nguyen',47,7),(69,'Elijah','Mullen',99,7),(70,'Kelsey','Berry',12,7),(71,'Cory','Whitehead',13,7),(72,'Jordan','Gilbert DDS',74,7),(73,'Micheal','Williams',35,7),(74,'Larry','Weber',31,7),(75,'Stephanie','Martinez',22,7),(76,'Julia','Jones',3,7),(77,'Lauren','Clarke',79,7),(78,'Kayla','Harrison',7,8),(79,'Brian','Knight',30,8),(80,'Robert','Smith',47,8),(81,'Michael','Fleming',64,8),(82,'Matthew','Fleming',42,8),(83,'Nicole','Robles',97,8),(84,'Michael','Campbell',50,8),(85,'Roy','Taylor',60,8),(86,'Heather','Williams',48,8),(87,'Marissa','Waters',36,8),(88,'Deborah','Sutton',57,8),(89,'Mrs.','Amber Johnson',47,9),(90,'David','Mitchell',37,9),(91,'Nicole','Grant',5,9),(92,'Anne','Bass',4,9),(93,'Crystal','Ashley',56,9),(94,'Paul','Cisneros',74,9),(95,'Laura','Thompson',26,9),(96,'Rachel','Boyd',91,9),(97,'Tina','Navarro',84,9),(98,'Victor','Baker',23,9),(99,'Nicole','Montes',47,9),(100,'Lance','Page',61,10),(101,'Sheila','Hill',83,10),(102,'Sarah','Herrera',41,10),(103,'Christopher','Atkinson',6,10),(104,'Dr.','Veronica Irwin',13,10),(105,'Charles','Short',87,10),(106,'Karen','Sanchez',79,10),(107,'James','Brown',25,10),(108,'Justin','Burton',9,10),(109,'Bryan','Smith',77,10),(110,'Charles','Hall',85,10),(111,'Emily','Wright',41,11),(112,'Sherry','Williams',34,11),(113,'Tracey','Klein',95,11),(114,'Christopher','Ramsey',87,11),(115,'Ernest','Dean',96,11),(116,'Robert','Dennis',66,11),(117,'Heather','Cox',41,11),(118,'Darrell','Nunez',84,11),(119,'Andrea','Adams MD',18,11),(120,'Nicole','Sims MD',31,11),(121,'Charlene','Spears',55,11),(122,'Andrew','Glenn DDS',89,12),(123,'Lee','Nelson',43,12),(124,'Laura','Hughes',38,12),(125,'Felicia','Hall',15,12),(126,'Heather','Walters',36,12),(127,'Jason','White',10,12),(128,'Kristin','Williams',52,12),(129,'Eric','Holt DVM',50,12),(130,'Kevin','Cook',31,12),(131,'Amy','Chen',55,12),(132,'Jessica','Garcia',55,12),(133,'Logan','Briggs',29,13),(134,'Adam','Hughes',17,13),(135,'Allen','Powell',57,13),(136,'Renee','Williams',12,13),(137,'Kenneth','Lee',27,13),(138,'David','Beltran',42,13),(139,'Derek','Webb',69,13),(140,'Amber','Ponce',92,13),(141,'Dylan','Randolph',64,13),(142,'Tina','Pierce',33,13),(143,'Sharon','Smith',41,13),(144,'Theodore','Leblanc',23,14),(145,'Kelly','Grant',57,14),(146,'Nicholas','Brown',93,14),(147,'Adam','Murphy',54,14),(148,'Ross','Gates',38,14),(149,'Lori','Carlson',20,14),(150,'Kathy','Campbell',42,14),(151,'Tiffany','Noble',81,14),(152,'Michele','Rogers',84,14),(153,'Cody','Peters',50,14),(154,'Wendy','Jones',33,14),(155,'Aaron','Garrett',92,15),(156,'Amanda','Hamilton',37,15),(157,'Samuel','White',51,15),(158,'Cole','Mahoney',90,15),(159,'Lisa','Johnson',90,15),(160,'William','Green',35,15),(161,'David','Burns',63,15),(162,'Robert','Bass',48,15),(163,'Mackenzie','Velasquez',28,15),(164,'Kyle','Horton',66,15),(165,'Jack','Gray',14,15),(166,'Rachel','Contreras',13,16),(167,'James','Blair',71,16),(168,'Shelly','Price',63,16),(169,'Mr.','Colton Walls',46,16),(170,'Benjamin','Hunter',66,16),(171,'Stefanie','Taylor',16,16),(172,'Hannah','Garrett',85,16),(173,'Steven','Castro',44,16),(174,'Joshua','Estrada',28,16),(175,'Tammy','Ruiz',42,16),(176,'Bryan','Garcia',23,16),(177,'Jennifer','Garcia',17,17),(178,'James','Butler',58,17),(179,'Stanley','Perez',12,17),(180,'Laura','Woods',27,17),(181,'Angela','Sandoval',24,17),(182,'Angela','Becker',10,17),(183,'James','Hill',5,17),(184,'Patricia','West',25,17),(185,'Sheila','Carlson',9,17),(186,'Julie','Martin',61,17),(187,'Karen','Johnson',80,17),(188,'Stacey','Williams',3,18),(189,'Michael','Diaz',30,18),(190,'Michael','Dean',72,18),(191,'Anna','Perkins',44,18),(192,'Dr.','Edward White',25,18),(193,'Joseph','Wilson',19,18),(194,'Kelly','Farmer',76,18),(195,'Matthew','Vaughn',41,18),(196,'Gabriel','Hopkins',35,18),(197,'Wanda','Higgins',72,18),(198,'Jared','Harrison',19,18),(199,'Stephanie','Hanson',60,19),(200,'Austin','Murray',81,19),(201,'Jesse','Shaw',19,19),(202,'Daniel','Gomez',69,19),(203,'Christina','Hendricks',13,19),(204,'Michael','Bailey',66,19),(205,'Wendy','Dean',45,19),(206,'Mark','Russell',80,19),(207,'Wendy','Cohen',27,19),(208,'Cory','Carey',74,19),(209,'Vincent','Banks',48,19),(210,'Stacie','Olson',93,20),(211,'Larry','Lee',34,20),(212,'Derrick','Johnson',22,20),(213,'Sharon','Brown',32,20),(214,'Joseph','Gomez',15,20),(215,'Melissa','Becker',7,20),(216,'Robert','King',87,20),(217,'Jane','Chan',96,20),(218,'Johnathan','Valenzuela',64,20),(219,'Kayla','Bowman',90,20),(220,'Lisa','Berry',31,20),(221,'Edward','Washington',20,21),(222,'Stephen','Ramos',89,21),(223,'Edward','Hernandez',97,21),(224,'Sharon','Taylor',10,21),(225,'Christopher','Kim',59,21),(226,'Phillip','Lopez',45,21),(227,'Deanna','Rose',8,21),(228,'Julie','Harris',10,21),(229,'Brent','Ross',18,21),(230,'Margaret','Lopez',75,21),(231,'Robert','Bolton',41,21),(232,'Mr.','John Randall',46,22),(233,'William','Perry',38,22),(234,'Jennifer','Carroll',4,22),(235,'Megan','Fuller',62,22),(236,'Michelle','Owen',46,22),(237,'Joseph','Hardin',65,22),(238,'Anthony','Reid',86,22),(239,'Alyssa','Garcia',36,22),(240,'David','Patel',42,22),(241,'Gary','Mitchell',19,22),(242,'Barbara','Parks',76,22),(243,'Joshua','Schmidt',48,23),(244,'Kayla','Harris',6,23),(245,'Rebecca','Combs',16,23),(246,'Janet','Collins',7,23),(247,'Kaitlyn','Cox',19,23),(248,'Joe','Keller',46,23),(249,'Timothy','Miller',6,23),(250,'Christopher','Jones',86,23),(251,'Donald','Wilson',37,23),(252,'Donald','Sherman',7,23),(253,'Jeremy','Contreras',13,23),(254,'William','Cohen',42,24),(255,'Suzanne','Paul',3,24),(256,'Michael','Hughes',31,24),(257,'Christopher','Santiago',26,24),(258,'Jose','Huffman',23,24),(259,'Carlos','Moore',94,24),(260,'Michele','Shelton',85,24),(261,'Christine','Stone',75,24),(262,'Stephanie','Johnson',99,24),(263,'Holly','Smith',21,24),(264,'Kristin','Rogers',25,24),(265,'Suzanne','Carter',84,25),(266,'Alicia','Jones',39,25),(267,'Benjamin','Guerra',77,25),(268,'Daniel','Tucker MD',4,25),(269,'Christopher','Ray',36,25),(270,'Justin','Roman',56,25),(271,'Jeffrey','Navarro',43,25),(272,'Jill','Holt',3,25),(273,'Allison','Smith',17,25),(274,'Gregory','Moore',93,25),(275,'Christopher','Burgess',82,25),(276,'Erin','Cox',4,26),(277,'Alexis','Anderson',23,26),(278,'Toni','Randall',25,26),(279,'Casey','Mcconnell',39,26),(280,'John','Williams',38,26),(281,'Dana','Scott',38,26),(282,'Gary','Smith',66,26),(283,'Julie','Phelps',99,26),(284,'Linda','Morgan',20,26),(285,'Daniel','Andrews',45,26),(286,'Troy','Dickson',10,26),(287,'Robert','Holland',41,27),(288,'Olivia','Kim',89,27),(289,'Tiffany','Harrington',43,27),(290,'Wesley','Rich',38,27),(291,'Kimberly','Gaines',34,27),(292,'Sherry','Arnold',89,27),(293,'Antonio','Berger',59,27),(294,'Bryan','Brewer',24,27),(295,'Melanie','Long',26,27),(296,'Kerry','Ramirez',40,27),(297,'Ana','Barker',13,27),(298,'Susan','Morris',86,28),(299,'Calvin','Patterson',12,28),(300,'Donald','Hurley',40,28),(301,'Michael','Jenkins',44,28),(302,'Kari','Lopez',71,28),(303,'Gabrielle','Sullivan',82,28),(304,'Bailey','Lopez',43,28),(305,'Richard','Chavez',2,28),(306,'Mary','George',63,28),(307,'Cynthia','Lynch',59,28),(308,'Paula','Adkins',67,28),(309,'Christine','Perkins',65,29),(310,'William','Martin',67,29),(311,'Alexander','Adams',32,29),(312,'Robert','Barrett',60,29),(313,'John','Wright',97,29),(314,'Sherry','Davis',90,29),(315,'Angela','Kim',50,29),(316,'Stacy','Burton',64,29),(317,'Lisa','Barnes',69,29),(318,'Melvin','Harris',91,29),(319,'Jonathan','Perry',90,29),(320,'Michael','Mccoy',73,30),(321,'Angelica','Thompson',71,30),(322,'Jon','Robinson',75,30),(323,'Alexa','Santos DVM',76,30),(324,'Janice','Simmons',10,30),(325,'Paul','Barber',7,30),(326,'Shelia','Garcia',36,30),(327,'Austin','Ballard',62,30),(328,'John','Myers',69,30),(329,'Kristy','Liu',15,30),(330,'Matthew','Hayes',87,30),(331,'Kylie','Farmer',33,31),(332,'Lori','Carroll',50,31),(333,'Victoria','Chen',89,31),(334,'Cynthia','Cole',47,31),(335,'Jon','Bennett',56,31),(336,'Nancy','Hoover',71,31),(337,'Dr.','Mallory White',95,31),(338,'Sierra','Joseph',16,31),(339,'Allison','Baker',10,31),(340,'Rodney','Diaz',89,31),(341,'Tina','Kelly',76,31),(342,'Brenda','Knight',29,32),(343,'Jennifer','Carroll',74,32),(344,'Christina','Nunez',63,32),(345,'Tonya','Farrell',90,32),(346,'Wanda','Moore',70,32),(347,'Susan','Long',39,32),(348,'Cathy','Torres',53,32),(349,'Dustin','Leonard',89,32),(350,'Shirley','Lynch',45,32),(351,'Jennifer','Kelly',25,32),(352,'Jason','Chapman',75,32);
/*!40000 ALTER TABLE `joueurs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `matchs`
--

DROP TABLE IF EXISTS `matchs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `matchs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `equipe1` varchar(50) DEFAULT NULL,
  `equipe2` varchar(50) DEFAULT NULL,
  `jour` date NOT NULL,
  `debut` varchar(10) DEFAULT NULL,
  `fin` varchar(10) DEFAULT ' - ',
  `statut` varchar(20) DEFAULT ' - ',
  `score` varchar(10) DEFAULT ' - ',
  `meteo` varchar(20) DEFAULT ' - ',
  `cote1` int DEFAULT NULL,
  `cote2` int DEFAULT NULL,
  `commentaires` varchar(100) DEFAULT ' - ',
  `but1` int DEFAULT NULL,
  `but2` int DEFAULT NULL,
  `vainqueur` varchar(50) DEFAULT '-',
  PRIMARY KEY (`id`,`jour`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `matchs`
--

LOCK TABLES `matchs` WRITE;
/*!40000 ALTER TABLE `matchs` DISABLE KEYS */;
INSERT INTO `matchs` VALUES (1,'Kansas City Chiefs','Chicago Bears','2024-01-03','12:00','13:00','Terminé',NULL,'Pluvieux, -10°C',5,2,' - ',NULL,NULL,'-'),(2,'Indianapolis Colts','Buffalo Bills','2024-01-10','12:00','13:00','À venir',NULL,'Nuageux, 27°C',4,2,' - ',NULL,NULL,'-'),(3,'Cincinnati Bengals','Detroit Lions','2024-01-15','15:00','16:00','Terminé','3 - 2','Nuageux, 11°C',5,5,'Great',3,2,'Cincinnati Bengals'),(4,'Green Bay Packers','Minnesota Vikings','2024-01-15','20:00','21:00','À venir',NULL,'Nuageux, 16°C',5,2,' - ',NULL,NULL,'-'),(5,'Miami Dolphins','San Francisco 49ers','2024-01-15','22:00','23:00','À venir',NULL,'Venteux, 24°C',5,2,' - ',NULL,NULL,'-'),(6,'Cincinnati Bengals','Chicago Bears','2024-01-17','10:00','11:00','À venir',NULL,'Neigeux, 4°C',5,2,' - ',NULL,NULL,'-'),(7,'Pittsburgh Steelers','Houston Texans','2024-01-17','12:00','13:00','Terminé','2 - 3','Nuageux, 30°C',2,2,'el pepe el rulas el pepafqsefqsdcqosifhqsodfiqsdcfqsdf',2,3,'-'),(8,'Jacksonville Jaguars','Las Vegas Raiders','2024-01-17','13:00','14:00','À venir',NULL,'Nuageux, 14°C',4,2,' - ',NULL,NULL,'-'),(9,'Cincinnati Bengals','Detroit Lions','2024-01-18','10:00','11:00','Terminé',NULL,'Neigeux, 21°C',4,2,' - ',NULL,NULL,'-'),(10,'Buffalo Bills','Dallas Cowboys','2024-01-18','12:00','13:00','À venir',NULL,'Venteux, -7°C',5,2,' - ',NULL,NULL,'-'),(11,'Tennessee Titans','Atlanta Falcons','2024-01-18','15:00','16:00','À venir',NULL,'Nuageux, 20°C',5,2,' - ',NULL,NULL,'-'),(12,'Las Vegas Raiders','Jacksonville Jaguars','2024-01-19','14:00','15:00','À venir',NULL,'Pluvieux, 29°C',5,3,' - ',NULL,NULL,'-'),(13,'Minnesota Vikings','Chicago Bears','2024-01-19','15:00','16:00','À venir',NULL,'Nuageux, 30°C',3,2,' - ',NULL,NULL,'-'),(14,'Green Bay Packers','Baltimore Ravens','2024-01-19','20:00','21:00','À venir',NULL,'Venteux, 30°C',2,2,' - ',NULL,NULL,'-'),(15,'Houston Texans','Indianapolis Colts','2024-01-19','13:00','14:00','À venir',NULL,'Venteux, 27°C',2,3,' - ',NULL,NULL,'-'),(16,'New York Giants','Miami Dolphins','2024-01-20','10:00','11:00','À venir',NULL,'Pluvieux, 2°C',7,6,' - ',NULL,NULL,'-'),(17,'Arizona Cardinals','Denver Broncos','2024-01-20','12:00','13:00','À venir',NULL,'Venteux, -9°C',2,3,' - ',NULL,NULL,'-'),(18,'Kansas City Chiefs','Minnesota Vikings','2024-01-20','14:00','15:00','À venir',NULL,'Nuageux, -5°C',4,5,' - ',NULL,NULL,'-'),(22,'Arizona Cardinals','Baltimore Ravens','2024-01-23','16:00','17:00','À venir',NULL,'Pluvieux, 14°C',5,2,' - ',NULL,NULL,'-'),(23,'Dallas Cowboys','Buffalo Bills','2024-01-23','20:00','21:00','À venir',NULL,'Ensoleillé, 14°C',5,2,' - ',NULL,NULL,'-'),(24,'Houston Texans','New York Giants','2024-01-23','20:00','21:00','À venir',NULL,'Nuageux, 10°C',2,3,' - ',NULL,NULL,'-'),(25,'Arizona Cardinals','Baltimore Ravens','2024-01-24','10:00','11:00','À venir',NULL,'Neigeux, -9°C',5,2,' - ',NULL,NULL,'-'),(26,'Jacksonville Jaguars','Carolina Panthers','2024-01-24','12:00','13:00','À venir',NULL,'Ensoleillé, 19°C',3,2,' - ',NULL,NULL,'-'),(27,'Kansas City Chiefs','Chicago Bears','2024-01-24','13:00','14:00','À venir',NULL,'Venteux, 15°C',2,3,' - ',NULL,NULL,'-'),(28,'Tampa Bay Buccaneers','Atlanta Falcons','2024-01-25','10:00','11:00','À venir',NULL,'Ensoleillé, 0°C',2,3,' - ',NULL,NULL,'-'),(29,'Las Vegas Raiders','Minnesota Vikings','2024-01-25','14:00','15:00','À venir',NULL,'Ensoleillé, 4°C',2,4,' - ',NULL,NULL,'-'),(30,'Kansas City Chiefs','New York Jets','2024-01-25','14:00','15:00','À venir',NULL,'Nuageux, 22°C',5,2,' - ',NULL,NULL,'-'),(31,'Miami Dolphins','Carolina Panthers','2024-01-25','17:00','18:00','À venir',NULL,'Pluvieux, 14°C',4,2,' - ',NULL,NULL,'-'),(32,'Las Vegas Raiders','Cincinnati Bengals','2024-01-26','10:00','11:00','À venir',NULL,'Venteux, 6°C',5,2,' - ',NULL,NULL,'-'),(33,'Dallas Cowboys','Los Angeles Chargers','2024-01-26','12:00','13:00','À venir',NULL,'Ensoleillé, 12°C',4,3,' - ',NULL,NULL,'-'),(34,'Tennessee Titans','Washington Commanders','2024-01-26','18:00','19:00','À venir',NULL,'Venteux, 1°C',2,3,' - ',NULL,NULL,'-'),(35,'New England Patriots','Miami Dolphins','2024-01-26','21:00','22:00','À venir',NULL,'Ensoleillé, 8°C',2,5,' - ',NULL,NULL,'-'),(36,'Arizona Cardinals','Buffalo Bills','2024-01-29','10:00','11:00','À venir',NULL,'Pluvieux, 30°C',4,3,' - ',NULL,NULL,'-'),(37,'Carolina Panthers','Chicago Bears','2024-01-29','12:00','13:00','À venir',NULL,'Pluvieux, 31°C',2,3,' - ',NULL,NULL,'-'),(38,'Las Vegas Raiders','Houston Texans','2024-01-29','16:00','17:00','À venir',NULL,'Nuageux, -8°C',4,5,' - ',NULL,NULL,'-'),(39,'Jacksonville Jaguars','Miami Dolphins','2024-01-29','19:00','20:00','À venir',NULL,'Pluvieux, -7°C',2,3,' - ',NULL,NULL,'-'),(40,'Arizona Cardinals','Atlanta Falcons','2024-01-30','15:00','16:00','Terminé','5 - 6','Nuageux, 22°C',4,6,'Parfait',5,6,'Atlanta Falcons'),(41,'Buffalo Bills','Chicago Bears','2024-01-30','17:00','18:00','Terminé',NULL,'Pluvieux, 9°C',2,3,' - ',NULL,NULL,'-'),(42,'Houston Texans','Detroit Lions','2024-01-30','19:00','20:00','À venir',NULL,'Ensoleillé, 9°C',2,5,' - ',NULL,NULL,'-'),(43,'Detroit Lions','Baltimore Ravens','2024-01-30','20:00','21:00','Terminé',NULL,'Nuageux, -1°C',5,3,' - ',NULL,NULL,'-'),(44,'Baltimore Ravens','Buffalo Bills','2024-01-31','11:00','12:00','Terminé',NULL,'Ensoleillé, -7°C',5,3,' - ',NULL,NULL,'-'),(45,'Las Vegas Raiders','Los Angeles Rams','2024-01-31','15:00','16:00','En cours','2 - 3','Neigeux, 24°C',2,6,'pepe',2,3,'Los Angeles Rams'),(46,'Philadelphia Eagles','Seattle Seahawks','2024-01-31','14:00','15:00','Terminé','3 - 1','Pluvieux, 20°C',5,4,'pepe',3,1,'Philadelphia Eagles'),(47,'New York Giants','Minnesota Vikings','2024-01-31','17:00','18:00','Terminé','5 - 6','Venteux, 6°C',3,4,'PEPE',5,6,'Minnesota Vikings'),(48,'Arizona Cardinals','Baltimore Ravens','2024-02-28','10:56','11:56','Terminé','2 - 5','Nuageux, 17°C',5,6,'ganador',2,5,'Baltimore Ravens'),(49,'Arizona Cardinals','Atlanta Falcons','2024-03-26','14:18','15:18','À venir',NULL,'Pluvieux, -10°C',5,10,' - ',NULL,NULL,'-'),(50,'Chicago Bears','Carolina Panthers','2024-03-26','15:18','16:18','À venir',NULL,'Venteux, 33°C',4,3,' - ',NULL,NULL,'-'),(51,'Baltimore Ravens','Houston Texans','2024-03-26','15:19','16:19','À venir',NULL,'Nuageux, 8°C',4,10,' - ',NULL,NULL,'-');
/*!40000 ALTER TABLE `matchs` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`PEPE`@`localhost`*/ /*!50003 TRIGGER `actualizacion_fin_match` BEFORE INSERT ON `matchs` FOR EACH ROW BEGIN
    SET NEW.fin = DATE_FORMAT(DATE_ADD(STR_TO_DATE(NEW.debut, '%H:%i'), INTERVAL 1 HOUR), '%H:%i');
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`PEPE`@`localhost`*/ /*!50003 TRIGGER `maj_score` BEFORE INSERT ON `matchs` FOR EACH ROW BEGIN
    SET NEW.score = CONCAT(NEW.but1, ' - ', NEW.but2);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`PEPE`@`localhost`*/ /*!50003 TRIGGER `maj_score_update` BEFORE UPDATE ON `matchs` FOR EACH ROW BEGIN
    SET NEW.score = CONCAT(NEW.but1, ' - ', NEW.but2);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `mises`
--

DROP TABLE IF EXISTS `mises`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mises` (
  `id` int NOT NULL AUTO_INCREMENT,
  `mise1` decimal(10,2) DEFAULT NULL,
  `mise2` decimal(10,2) DEFAULT NULL,
  `resultat1` varchar(20) DEFAULT NULL,
  `resultat2` varchar(20) DEFAULT NULL,
  `equipe1` varchar(50) DEFAULT NULL,
  `equipe2` varchar(50) DEFAULT NULL,
  `cote1` varchar(20) DEFAULT NULL,
  `cote2` varchar(20) DEFAULT NULL,
  `id_match` int DEFAULT NULL,
  `id_utilisateur` int DEFAULT NULL,
  `datemise` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_utilisateur` (`id_utilisateur`),
  KEY `mises_ibfk_2` (`id_match`),
  CONSTRAINT `mises_ibfk_1` FOREIGN KEY (`id_match`) REFERENCES `matchs` (`id`),
  CONSTRAINT `mises_ibfk_2` FOREIGN KEY (`id_match`) REFERENCES `matchs` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mises`
--

LOCK TABLES `mises` WRITE;
/*!40000 ALTER TABLE `mises` DISABLE KEYS */;
INSERT INTO `mises` VALUES (25,4.00,NULL,'16',NULL,'Indianapolis Colts',NULL,'4',NULL,2,1,'2024-01-13'),(26,NULL,2.00,NULL,'4',NULL,'Buffalo Bills',NULL,'2',2,1,'2024-01-13'),(28,NULL,1.00,NULL,'2',NULL,'Chicago Bears',NULL,'2',1,1,'2024-01-13'),(29,7.00,NULL,'35',NULL,'Miami Dolphins',NULL,'5',NULL,5,1,'2024-01-25'),(30,NULL,4.00,NULL,'8',NULL,'San Francisco 49ers',NULL,'2',5,1,'2024-01-25'),(32,NULL,2.00,NULL,'4',NULL,'Chicago Bears',NULL,'2',6,1,'2024-01-25'),(33,5.00,NULL,'25',NULL,'Las Vegas Raiders',NULL,'5',NULL,12,1,'2024-01-25'),(34,NULL,5.00,NULL,'15',NULL,'Jacksonville Jaguars',NULL,'3',12,1,'2024-01-25'),(35,12.00,NULL,'24',NULL,'Tampa Bay Buccaneers',NULL,'2',NULL,28,1,'2024-01-25'),(36,NULL,12.00,NULL,'36',NULL,'Atlanta Falcons',NULL,'3',28,1,'2024-01-25'),(37,2.00,NULL,'8',NULL,'Arizona Cardinals',NULL,'4',NULL,40,1,'2024-01-30'),(38,NULL,3.00,NULL,'18',NULL,'Atlanta Falcons',NULL,'6',40,1,'2024-01-30'),(39,4.00,NULL,'8',NULL,'Buffalo Bills',NULL,'2',NULL,41,1,'2024-01-30'),(40,NULL,1.00,NULL,'3',NULL,'Chicago Bears',NULL,'3',41,1,'2024-01-30'),(41,2.00,NULL,'10',NULL,'Detroit Lions',NULL,'5',NULL,43,1,'2024-01-30'),(42,NULL,1.00,NULL,'3',NULL,'Baltimore Ravens',NULL,'3',43,1,'2024-01-30'),(43,2.00,NULL,'10',NULL,'Arizona Cardinals',NULL,'5',NULL,48,1,'2024-02-28'),(44,NULL,2.00,NULL,'12',NULL,'Baltimore Ravens',NULL,'6',48,1,'2024-02-28'),(45,3.00,NULL,'15',NULL,'Kansas City Chiefs',NULL,'5',NULL,30,1,'2024-02-28'),(46,NULL,2.00,NULL,'4',NULL,'New York Jets',NULL,'2',30,1,'2024-02-28'),(47,2.00,NULL,'4',NULL,'Las Vegas Raiders',NULL,'2',NULL,45,8,'2024-04-10'),(48,NULL,1.00,NULL,'6',NULL,'Los Angeles Rams',NULL,'6',45,8,'2024-04-10');
/*!40000 ALTER TABLE `mises` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) DEFAULT NULL,
  `prenom` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `mot_de_passe` varchar(255) DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  `confirmed` tinyint(1) DEFAULT '0',
  `role` varchar(50) DEFAULT 'user',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'pinto','vitor','pintotest@hotmail.com','pbkdf2:sha256:600000$2rLEEDK8pM2YhiCK$35cd308f010800c79a0c5069e78d787e0832aa3515c3eff9f82e0621a393326a','c86f5c141cb96d4def884d3146ae0099',1,'user'),(2,'admin','admin','admin@hotmail.com','pbkdf2:sha256:600000$fzqDO6SnzOF4Mghc$cdf6069e8eec02ed598eaa0c51d393d2f19a9f733d42b4fe1a2d9fca4dab7fb8','e2c1d3a03299c1a2c5f06dde888ac001',1,'admin'),(8,'Test','User','testuser@hotmail.com','pbkdf2:sha256:600000$4xj3OJvgRYWFB7KW$8cc004c02fb718fa2f990656d579453534d2131286ae02774a66127082efb90f','7b300e581bc62b05b9d342efed5cb679',1,'user'),(9,'admin','user','adminuser@hotmail.com','pbkdf2:sha256:600000$MbcE8NsRnWpKGKDb$81d0f97c4e370502f3b88e33e740e6f9be8eaa25157321de4339b9aee8dd3da6','c16251f10f57cc4ac7515712b07c6464',1,'admin');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-26 10:40:49
