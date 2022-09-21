-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: tour_service
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `booking` (
  `booking_id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `client_id` int(11) NOT NULL,
  `service_id` int(45) DEFAULT NULL,
  PRIMARY KEY (`booking_id`),
  KEY `fk_booking_client1_idx` (`client_id`),
  KEY `fk_booking_service1_idx` (`service_id`),
  CONSTRAINT `fk_booking_client1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`),
  CONSTRAINT `fk_booking_service1` FOREIGN KEY (`service_id`) REFERENCES `service` (`service_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,'Enver','2030-06-01',100,1,1),(2,'Marlen','2020-06-01',400,2,2),(3,'Aider','2030-06-01',200,3,3),(4,'Enver','2020-06-01',0,1,3);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `client_id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'Enver','st.Closs 13','+79781179428','test@mail.ru'),(2,'Marlen','st.Volvo 3','+79785149151','test@mail.ru'),(3,'Aider','st.Gorkogo 4','+797803156496','test@mail.ru');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `paid` int(11) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `client_id` int(11) NOT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `fk_payment_client1_idx` (`client_id`),
  CONSTRAINT `fk_payment_client1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,'Enver',117450,'st.Closs 13','+79781179428','test@mail.ru',1),(2,'Marlen',27180,'st.Volvo 3','+79785149151','test@mail.ru',2),(3,'Aider',4500,'st.Gorkogo 4','+797803156496','test@mail.ru',3);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `service`
--

DROP TABLE IF EXISTS `service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `service` (
  `service_id` int(11) NOT NULL,
  `price` int(11) DEFAULT NULL,
  `Availability` tinyint(4) DEFAULT NULL,
  `name` varchar(45) DEFAULT NULL,
  `type` varchar(45) DEFAULT NULL,
  `team_size` int(11) DEFAULT NULL,
  `date` varchar(45) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `route` varchar(45) DEFAULT NULL,
  `image` varchar(200) DEFAULT NULL,
  `client_id` int(11) NOT NULL,
  PRIMARY KEY (`service_id`),
  KEY `fk_service_client_idx` (`client_id`),
  CONSTRAINT `fk_service_client` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `service`
--

LOCK TABLES `service` WRITE;
/*!40000 ALTER TABLE `service` DISABLE KEYS */;
INSERT INTO `service` VALUES (1,30000,1,'Egypt','tour',1,'2020-04-20',7,NULL,'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/Egypt.Giza.Sphinx.02.jpg/440px-Egypt.Giza.Sphinx.02.jpg',2),(2,80000,1,'Turkey','cruise',1,'2020-06-20',3,NULL,'https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/View_on_Ayvalik.JPG/440px-View_on_Ayvalik.JPG',3),(3,260000,1,'Australia','tour',5,'2020-06-20',10,NULL,'https://99px.ru/sstorage/53/2011/02/mid_10642_3431.jpg',1),(4,20000,1,'USA','tour',1,'2020-06-20',7,NULL,'https://cdn.musavat.com/news/thumbnails/dir289/img1807080.jpg',3);
/*!40000 ALTER TABLE `service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(145) NOT NULL,
  `password` varchar(145) NOT NULL,
  `email` varchar(145) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'1','$pbkdf2-sha256$29000$eE/p3XsvhTBGKEXImdO6tw$M2DPaIWfe4qTiym.3UIIWfNQjzzaSB6bZwgHu/LjQDc','1@1.1'),(3,'2','$pbkdf2-sha256$29000$EiLEuFcKgZBSKsX4/78Xwg$NjB9errx7Cj70vCmwjmQ6S4./nU5yZ/HcYCqqjBFdos','2@2.2');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-10-31  1:08:09
