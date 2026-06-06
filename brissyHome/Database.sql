CREATE DATABASE  IF NOT EXISTS `brissyhome` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `brissyhome`;
-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: brissyhome
-- ------------------------------------------------------
-- Server version	8.4.0

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
-- Table structure for table `bookmarks`
--

DROP TABLE IF EXISTS `bookmarks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bookmarks` (
  `bookmark_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `property_id` int NOT NULL,
  `notes` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`bookmark_id`),
  UNIQUE KEY `unique_bookmark` (`user_id`,`property_id`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `bookmarks_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `bookmarks_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bookmarks`
--

LOCK TABLES `bookmarks` WRITE;
/*!40000 ALTER TABLE `bookmarks` DISABLE KEYS */;
INSERT INTO `bookmarks` VALUES (1,3,2,NULL,'2026-06-06 10:02:35');
/*!40000 ALTER TABLE `bookmarks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `enquiries`
--

DROP TABLE IF EXISTS `enquiries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `enquiries` (
  `enquiry_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `property_id` int NOT NULL,
  `message` text NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`enquiry_id`),
  KEY `user_id` (`user_id`),
  KEY `property_id` (`property_id`),
  CONSTRAINT `enquiries_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  CONSTRAINT `enquiries_ibfk_2` FOREIGN KEY (`property_id`) REFERENCES `properties` (`property_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `enquiries`
--

LOCK TABLES `enquiries` WRITE;
/*!40000 ALTER TABLE `enquiries` DISABLE KEYS */;
/*!40000 ALTER TABLE `enquiries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `properties`
--

DROP TABLE IF EXISTS `properties`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `properties` (
  `property_id` int NOT NULL AUTO_INCREMENT,
  `seller_id` int NOT NULL,
  `title` varchar(160) NOT NULL,
  `description` text NOT NULL,
  `address` varchar(180) NOT NULL,
  `suburb` varchar(80) NOT NULL,
  `postcode` varchar(10) NOT NULL,
  `property_type` varchar(50) NOT NULL,
  `rent_per_week` decimal(10,2) NOT NULL,
  `bedrooms` int NOT NULL,
  `bathrooms` int NOT NULL,
  `solar_available` tinyint(1) NOT NULL DEFAULT '0',
  `pet_friendly` tinyint(1) NOT NULL DEFAULT '0',
  `image_filename` varchar(120) NOT NULL DEFAULT 'property1.jpg',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`property_id`),
  KEY `seller_id` (`seller_id`),
  CONSTRAINT `properties_ibfk_1` FOREIGN KEY (`seller_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `properties`
--

LOCK TABLES `properties` WRITE;
/*!40000 ALTER TABLE `properties` DISABLE KEYS */;
INSERT INTO `properties` VALUES (1,2,'Brand New Apartment in Brisbane','Modern Kitchen \r\nNewly Built\r\nClose to major Schools \r\nClose to Supermarkets\r\n\r\n','13 204 Alice Street','Brisbane City','4000','Apartment',420.00,1,1,1,1,'home4.jpg','2026-06-06 08:12:30'),(2,2,'Newly Built Home for Rent','in Brisbane City \r\nClose to all requirements \r\n','108 Margaret Street','Brisbane City','4000','House',450.00,3,2,1,1,'property2.jpg','2026-06-06 09:11:52'),(3,2,'Home for Rent in Mcdowall','Newly Renovated Home in Mcdowall. \r\nClose to supermarkets \r\nBusway is walking distance away \r\nSolar Panel is available\r\n','22/906 Hamilton Road','Mcdowall','4028','House',500.00,2,2,1,1,'property3.jpg','2026-06-06 09:13:17'),(4,2,'Home for rent in Hamilton','Rent Includes:\r\n- Water\r\n- Electricity\r\n- Internet\r\n\r\nPrivate Inclusions:\r\n- Queen bedframe + 2 bedside tables\r\n- Wall-mounted HD TV\r\n- Air conditioner + ceiling fan\r\n- Built-in wardrobe\r\n- Modern private ensuite\r\n- Lockable pantry space\r\n\r\nShared Inclusions:\r\n- Modern kitchen with fridge/freezer, dishwasher, oven, stove, and appliances\r\n- Internal laundry with modern washing machine and dryer\r\n- Air-conditioned living/dining with couches, dining table & HD TV\r\n- Outdoor patio with table & chairs\r\n','1/9 Birt Street, Morayfield, Qld 4506','Morayfield','4506','House',310.00,4,2,0,0,'image_3.jpg','2026-06-06 10:06:40');
/*!40000 ALTER TABLE `properties` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `first_name` varchar(80) NOT NULL,
  `last_name` varchar(80) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `role` enum('seller','buyer') NOT NULL DEFAULT 'buyer',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'tharakar','tharakaravishan@gmail.com','pbkdf2:sha256:1000000$7oNEf4ui7bLKCvhK$6b53b104148ebe6bcd64b32bbf26ee974100fd5a27d2a0d0750868d8ba6c984e','Tharaka','Ranathunga','0712937878','buyer','2026-06-06 08:00:48'),(2,'agent1','agent1@gmail.com','pbkdf2:sha256:1000000$xuQITkQOp9Z14NRL$8b1bb7a5ee0069df23887afdebfabbefbf283413be4b7aa040e6ac1f9eb9b626','agent','1 ','0493344930','seller','2026-06-06 08:07:29'),(3,'user1','user1@gmail.com','pbkdf2:sha256:1000000$tZZ8fJYaOwS7rMl6$3a014b2d31dc66d6caf3d44963b6bdf4639e5b7352f6a3d16b1d1574baf0ad8d','user','1','0493344930','buyer','2026-06-06 09:56:03');
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

-- Dump completed on 2026-06-06 20:09:16
