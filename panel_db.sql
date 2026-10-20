/*!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.6.18-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: panel
-- ------------------------------------------------------
-- Server version	10.6.18-MariaDB-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add domain',7,'add_domain'),(26,'Can change domain',7,'change_domain'),(27,'Can delete domain',7,'delete_domain'),(28,'Can view domain',7,'view_domain'),(29,'Can add profile',8,'add_profile'),(30,'Can change profile',8,'change_profile'),(31,'Can delete profile',8,'delete_profile'),(32,'Can view profile',8,'view_profile'),(33,'Can add association',9,'add_association'),(34,'Can change association',9,'change_association'),(35,'Can delete association',9,'delete_association'),(36,'Can view association',9,'view_association'),(37,'Can add code',10,'add_code'),(38,'Can change code',10,'change_code'),(39,'Can delete code',10,'delete_code'),(40,'Can view code',10,'view_code'),(41,'Can add nonce',11,'add_nonce'),(42,'Can change nonce',11,'change_nonce'),(43,'Can delete nonce',11,'delete_nonce'),(44,'Can view nonce',11,'view_nonce'),(45,'Can add user social auth',12,'add_usersocialauth'),(46,'Can change user social auth',12,'change_usersocialauth'),(47,'Can delete user social auth',12,'delete_usersocialauth'),(48,'Can view user social auth',12,'view_usersocialauth'),(49,'Can add partial',13,'add_partial'),(50,'Can change partial',13,'change_partial'),(51,'Can delete partial',13,'delete_partial'),(52,'Can view partial',13,'view_partial');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `pkg_id` int(11) DEFAULT 1,
  `whm` int(2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$PvElhgCTvL5ryzgZGMGKxX$gSzvKNdfd8iIfnZxSPPkTy55yeSzkKIZm2I6zJgKaus=','2025-01-23 12:53:46.240123',1,'admin','admin','panel','admin@owpanel.com',1,1,'2024-09-28 14:41:30.918564',1,1);
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup`
--

DROP TABLE IF EXISTS `backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(500) DEFAULT NULL,
  `userid` int(11) NOT NULL,
  `schedule` varchar(500) DEFAULT NULL,
  `path` varchar(500) DEFAULT NULL,
  `username` varchar(500) DEFAULT NULL,
  `host` varchar(500) DEFAULT NULL,
  `user` varchar(500) DEFAULT NULL,
  `password` varchar(500) DEFAULT NULL,
  `category` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup`
--

LOCK TABLES `backup` WRITE;
/*!40000 ALTER TABLE `backup` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bandwidth`
--

DROP TABLE IF EXISTS `bandwidth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bandwidth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(20) DEFAULT NULL,
  `total` varchar(255) DEFAULT '0',
  `line` int(111) DEFAULT 0,
  `userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bandwidth`
--

LOCK TABLES `bandwidth` WRITE;
/*!40000 ALTER TABLE `bandwidth` DISABLE KEYS */;
/*!40000 ALTER TABLE `bandwidth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comments`
--

DROP TABLE IF EXISTS `comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `comments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `type` varchar(10) NOT NULL,
  `modified_at` int(11) NOT NULL,
  `account` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  `comment` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  KEY `comments_name_type_idx` (`name`,`type`),
  KEY `comments_order_idx` (`domain_id`,`modified_at`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comments`
--

LOCK TABLES `comments` WRITE;
/*!40000 ALTER TABLE `comments` DISABLE KEYS */;
/*!40000 ALTER TABLE `comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cryptokeys`
--

DROP TABLE IF EXISTS `cryptokeys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cryptokeys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) NOT NULL,
  `flags` int(11) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `published` tinyint(1) DEFAULT 1,
  `content` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `domainidindex` (`domain_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cryptokeys`
--

LOCK TABLES `cryptokeys` WRITE;
/*!40000 ALTER TABLE `cryptokeys` DISABLE KEYS */;
/*!40000 ALTER TABLE `cryptokeys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `object_repr` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(7,'domains','domain'),(6,'sessions','session'),(9,'social_django','association'),(10,'social_django','code'),(11,'social_django','nonce'),(13,'social_django','partial'),(12,'social_django','usersocialauth'),(8,'users','profile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-09-28 12:47:34.311501'),(2,'auth','0001_initial','2024-09-28 12:47:35.232016'),(3,'admin','0001_initial','2024-09-28 12:47:35.468032'),(4,'admin','0002_logentry_remove_auto_add','2024-09-28 12:47:35.480821'),(5,'admin','0003_logentry_add_action_flag_choices','2024-09-28 12:47:35.493166'),(6,'contenttypes','0002_remove_content_type_name','2024-09-28 12:47:35.594702'),(7,'auth','0002_alter_permission_name_max_length','2024-09-28 12:47:35.666594'),(8,'auth','0003_alter_user_email_max_length','2024-09-28 12:47:35.694489'),(9,'auth','0004_alter_user_username_opts','2024-09-28 12:47:35.703926'),(10,'auth','0005_alter_user_last_login_null','2024-09-28 12:47:35.754070'),(11,'auth','0006_require_contenttypes_0002','2024-09-28 12:47:35.760235'),(12,'auth','0007_alter_validators_add_error_messages','2024-09-28 12:47:35.768694'),(13,'auth','0008_alter_user_username_max_length','2024-09-28 12:47:35.856555'),(14,'auth','0009_alter_user_last_name_max_length','2024-09-28 12:47:35.908058'),(15,'auth','0010_alter_group_name_max_length','2024-09-28 12:47:35.928446'),(16,'auth','0011_update_proxy_permissions','2024-09-28 12:47:35.938116'),(17,'auth','0012_alter_user_first_name_max_length','2024-09-28 12:47:35.993311'),(18,'sessions','0001_initial','2024-09-28 12:47:36.064964'),(19,'domains','0001_initial','2024-09-28 13:26:26.215540'),(20,'default','0001_initial','2024-09-28 14:32:45.638885'),(21,'social_auth','0001_initial','2024-09-28 14:32:45.643173'),(22,'default','0002_add_related_name','2024-09-28 14:32:45.656349'),(23,'social_auth','0002_add_related_name','2024-09-28 14:32:45.660105'),(24,'default','0003_alter_email_max_length','2024-09-28 14:32:45.671916'),(25,'social_auth','0003_alter_email_max_length','2024-09-28 14:32:45.678956'),(26,'default','0004_auto_20160423_0400','2024-09-28 14:32:45.726846'),(27,'social_auth','0004_auto_20160423_0400','2024-09-28 14:32:45.734457'),(28,'social_auth','0005_auto_20160727_2333','2024-09-28 14:32:45.773116'),(29,'social_django','0006_partial','2024-09-28 14:32:45.805740'),(30,'social_django','0007_code_timestamp','2024-09-28 14:32:45.902900'),(31,'social_django','0008_partial_timestamp','2024-09-28 14:32:46.024068'),(32,'social_django','0009_auto_20191118_0520','2024-09-28 14:32:46.442844'),(33,'social_django','0010_uid_db_index','2024-09-28 14:32:46.548887'),(34,'users','0001_initial','2024-09-28 14:32:46.755430'),(35,'users','0002_alter_profile_avatar','2024-09-28 14:32:46.768644'),(36,'users','0003_alter_profile_avatar','2024-09-28 14:32:46.798924'),(37,'users','0004_profile_bio','2024-09-28 14:32:46.868875'),(38,'social_django','0005_auto_20160727_2333','2024-09-28 14:32:46.881723'),(39,'social_django','0003_alter_email_max_length','2024-09-28 14:32:46.906663'),(40,'social_django','0002_add_related_name','2024-09-28 14:32:46.912317'),(41,'social_django','0004_auto_20160423_0400','2024-09-28 14:32:46.916869'),(42,'social_django','0001_initial','2024-09-28 14:32:46.923695');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(200) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `path` varchar(500) DEFAULT NULL,
  `time` datetime DEFAULT current_timestamp(),
  `php` varchar(20) DEFAULT NULL,
  `ssl_exp` varchar(500) DEFAULT NULL,
  `line` int(110) DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=102 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain`
--

LOCK TABLES `domain` WRITE;
/*!40000 ALTER TABLE `domain` DISABLE KEYS */;
/*!40000 ALTER TABLE `domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domainmetadata`
--

DROP TABLE IF EXISTS `domainmetadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domainmetadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) NOT NULL,
  `kind` varchar(32) DEFAULT NULL,
  `content` text DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `domainmetadata_idx` (`domain_id`,`kind`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domainmetadata`
--

LOCK TABLES `domainmetadata` WRITE;
/*!40000 ALTER TABLE `domainmetadata` DISABLE KEYS */;
/*!40000 ALTER TABLE `domainmetadata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `domains`
--

DROP TABLE IF EXISTS `domains`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domains` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `master` varchar(128) DEFAULT NULL,
  `last_check` int(11) DEFAULT NULL,
  `type` varchar(6) NOT NULL,
  `notified_serial` int(10) unsigned DEFAULT NULL,
  `account` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_index` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domains`
--

LOCK TABLES `domains` WRITE;
/*!40000 ALTER TABLE `domains` DISABLE KEYS */;
/*!40000 ALTER TABLE `domains` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email_forwardings`
--

DROP TABLE IF EXISTS `email_forwardings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `email_forwardings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(80) NOT NULL,
  `destination` longtext NOT NULL,
  `userid` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `path` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_forwardings`
--

LOCK TABLES `email_forwardings` WRITE;
/*!40000 ALTER TABLE `email_forwardings` DISABLE KEYS */;
/*!40000 ALTER TABLE `email_forwardings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email_pipe`
--

DROP TABLE IF EXISTS `email_pipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `email_pipe` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(500) DEFAULT NULL,
  `transport_command` varchar(5000) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `path` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_pipe`
--

LOCK TABLES `email_pipe` WRITE;
/*!40000 ALTER TABLE `email_pipe` DISABLE KEYS */;
/*!40000 ALTER TABLE `email_pipe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `email_users`
--

DROP TABLE IF EXISTS `email_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `email_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(500) DEFAULT NULL,
  `password` varchar(200) NOT NULL,
  `mail` varchar(200) DEFAULT NULL,
  `DiskUsage` varchar(200) DEFAULT '0',
  `userid` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `e_users_emailOwner_id_761bf267_fk_e_domains_domain` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `email_users`
--

LOCK TABLES `email_users` WRITE;
/*!40000 ALTER TABLE `email_users` DISABLE KEYS */;
/*!40000 ALTER TABLE `email_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `firewall_firewallrules`
--

DROP TABLE IF EXISTS `firewall_firewallrules`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `firewall_firewallrules` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `proto` varchar(10) NOT NULL,
  `port` varchar(25) NOT NULL,
  `ipAddress` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `firewall_firewallrules`
--

LOCK TABLES `firewall_firewallrules` WRITE;
/*!40000 ALTER TABLE `firewall_firewallrules` DISABLE KEYS */;
INSERT INTO `firewall_firewallrules` VALUES (1,'panel','tcp','8090','0.0.0.0/0'),(2,'http','tcp','80','0.0.0.0/0'),(3,'https','tcp','443','0.0.0.0/0'),(4,'ftp','tcp','21','0.0.0.0/0'),(5,'smtp','tcp','25','0.0.0.0/0'),(6,'smtps','tcp','587','0.0.0.0/0'),(7,'ssmtp','tcp','465','0.0.0.0/0'),(8,'pop3','tcp','110','0.0.0.0/0'),(9,'imap','tcp','143','0.0.0.0/0'),(10,'simap','tcp','993','0.0.0.0/0'),(11,'dns','udp','53','0.0.0.0/0'),(12,'dnstcp','tcp','53','0.0.0.0/0'),(13,'ftptls','tcp','40110-40210','0.0.0.0/0'),(14,'POP3S','tcp','995','0.0.0.0/0'),(15,'quic','udp','443','0.0.0.0/0'),(16,'terminal','tcp','5678','0.0.0.0/0');
/*!40000 ALTER TABLE `firewall_firewallrules` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ftp`
--

DROP TABLE IF EXISTS `ftp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ftp` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` varchar(32) NOT NULL,
  `password` varchar(255) NOT NULL,
  `uid` int(11) NOT NULL,
  `gid` int(11) NOT NULL,
  `dir` varchar(255) NOT NULL,
  `QuotaSize` int(11) NOT NULL,
  `status` varchar(1) DEFAULT '1',
  `ULBandwidth` int(11) DEFAULT NULL,
  `DLBandwidth` int(11) DEFAULT NULL,
  `sate` date DEFAULT NULL,
  `LastModif` varchar(255) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `User` (`user`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;



DROP TABLE IF EXISTS `packages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packages` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `disk_space` int(11) DEFAULT 0,
  `bandwidth` int(11) DEFAULT 0,
  `email_accounts` int(11) DEFAULT 0,
  `databases` int(11) DEFAULT 0,
  `ftp_accounts` int(11) DEFAULT 0,
  `allowed_domains` int(11) DEFAULT 0,
  `userid` int(11) DEFAULT NULL,
  `enforce_disk_limits` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `packageName` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packages`
--
INSERT INTO `packages` (`id`, `name`, `disk_space`, `bandwidth`, `email_accounts`, `databases`, `ftp_accounts`, `allowed_domains`, `userid`, `enforce_disk_limits`) VALUES
(1, 'unlimited', 0, 0, 0, 0, 0, 0, NULL, 0);

--
-- Table structure for table `php_lib`
--

DROP TABLE IF EXISTS `php_lib`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `php_lib` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `extensionName` varchar(50) NOT NULL,
  `description` varchar(255) NOT NULL,
  `status` int(11) NOT NULL,
  `phpVers_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `managePHP_installedp_phpVers_id_54d8b7bc_fk_managePHP` (`phpVers_id`),
  CONSTRAINT `managePHP_installedp_phpVers_id_54d8b7bc_fk_managePHP` FOREIGN KEY (`phpVers_id`) REFERENCES `php_version` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=414 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `php_lib`
--

LOCK TABLES `php_lib` WRITE;
/*!40000 ALTER TABLE `php_lib` DISABLE KEYS */;
INSERT INTO `php_lib` VALUES (1,'lsphp53-bcmath','A module for PHP applications for using the bcmath library',1,1),(2,'lsphp53-common','Common files for PHP',1,1),(3,'lsphp53-dba','A database abstraction layer module for PHP applications',1,1),(4,'lsphp53-enchant','Human Language and Character Encoding Support',1,1),(5,'lsphp53-gd','A module for PHP applications for using the gd graphics library',1,1),(6,'lsphp53-imap','A module for PHP applications that use IMAP',1,1),(7,'lsphp53-intl','Internationalization extension for PHP application',1,1),(8,'lsphp53-ioncube-loader','Ioncube Loader',1,1),(9,'lsphp53-ldap','A module for PHP applications that use LDAP',1,1),(10,'lsphp53-mbstring','A module for PHP applications which need multi-byte string handling',1,1),(11,'lsphp53-mcrypt','Standard PHP module provides mcrypt library support',1,1),(12,'lsphp53-mysql','A module for PHP applications that use MySQL databases',1,1),(13,'lsphp53-odbc','A module for PHP applications that use ODBC databases',1,1),(14,'lsphp53-pdo','A database access abstraction module for PHP applications',1,1),(15,'lsphp53-pear','PHP Extension and Application Repository framework',1,1),(16,'lsphp53-pecl-apc','APC caches and optimizes PHP intermediate code',1,1),(17,'lsphp53-pgsql','A PostgreSQL database module for PHP',1,1),(18,'lsphp53-process','Modules for PHP script using system process interfaces',1,1),(19,'lsphp53-pspell','A module for PHP applications for using pspell interfaces',1,1),(20,'lsphp53-recode','A module for PHP applications for using the recode library',1,1),(21,'lsphp53-snmp','A module for PHP applications that query SNMP-managed devices',1,1),(22,'lsphp53-soap','A module for PHP applications that use the SOAP protocol',1,1),(23,'lsphp53-tidy','Standard PHP module provides tidy library support',1,1),(24,'lsphp53-xml','A module for PHP applications which use XML',1,1),(25,'lsphp53-xmlrpc','A module for PHP applications which use the XML-RPC protocol',1,1),(26,'lsphp53-debuginfo','Debug information for package lsphp53',0,1),(27,'lsphp53-lsphp53-devel','Files needed for building PHP extensions',0,1),(28,'lsphp53-mysql56','PHP scripting language for creating dynamic web sites',0,1),(29,'lsphp53-mysqlnd','A module for PHP applications that use MySQL databases',0,1),(30,'lsphp53-opcache','The Zend OPcache',0,1),(31,'lsphp53-pecl-apc-devel','APC developer files (header)',0,1),(32,'lsphp53-pecl-apc-panel','APC control panel',0,1),(33,'lsphp53-sqlite','Extension for the SQLite V2 Embeddable SQL Database Engine',0,1),(34,'lsphp53-xcache','PHP accelerator, optimizer, encoder and dynamic content cacher',0,1),(35,'lsphp53-xcache-admin','XCache Administration',0,1),(36,'lsphp54-bcmath','A module for PHP applications for using the bcmath library',1,2),(37,'lsphp54-common','Common files for PHP',1,2),(38,'lsphp53-dba','A database abstraction layer module for PHP applications',1,2),(39,'lsphp54-enchant','Human Language and Character Encoding Support',1,1),(40,'lsphp54-gd','A module for PHP applications for using the gd graphics library',1,2),(41,'lsphp54-imap','A module for PHP applications that use IMAP',1,2),(42,'lsphp54-intl','Internationalization extension for PHP application',1,1),(43,'lsphp54-ioncube-loader','Ioncube Loader',1,2),(44,'lsphp54-ldap','A module for PHP applications that use LDAP',1,2),(45,'lsphp54-mbstring','A module for PHP applications which need multi-byte string handling',1,2),(46,'lsphp54-mcrypt','Standard PHP module provides mcrypt library support',1,2),(47,'lsphp54-mysql','A module for PHP applications that use MySQL databases',1,2),(48,'lsphp54-odbc','A module for PHP applications that use ODBC databases',1,2),(49,'lsphp54-pdo','A database access abstraction module for PHP applications',1,2),(50,'lsphp54-pear','PHP Extension and Application Repository framework',1,2),(51,'lsphp54-pecl-apc','APC caches and optimizes PHP intermediate code',1,2),(52,'lsphp54-pgsql','A PostgreSQL database module for PHP',1,1),(53,'lsphp54-process','Modules for PHP script using system process interfaces',1,2),(54,'lsphp54-pspell','A module for PHP applications for using pspell interfaces',1,2),(55,'lsphp54-recode','A module for PHP applications for using the recode library',1,2),(56,'lsphp54-snmp','A module for PHP applications that query SNMP-managed devices',1,2),(57,'lsphp54-soap','A module for PHP applications that use the SOAP protocol',1,2),(58,'lsphp54-tidy','Standard PHP module provides tidy library support',1,2),(59,'lsphp54-xml','A module for PHP applications which use XML',1,2),(60,'lsphp54-xmlrpc','A module for PHP applications which use the XML-RPC protocol',1,2),(61,'lsphp54-debuginfo','Debug information for package lsphp54',0,2),(62,'lsphp54-mysql56-debuginfo','Debug information for package lsphp54-mysql56',0,2),(63,'lsphp54-lsphp53-devel','Files needed for building PHP extensions',0,2),(64,'lsphp54-mysql56','PHP scripting language for creating dynamic web sites',0,2),(65,'lsphp54-mysqlnd','A module for PHP applications that use MySQL databases',0,2),(66,'lsphp54-opcache','The Zend OPcache',0,2),(67,'lsphp54-pecl-apc-devel','APC developer files (header)',0,2),(68,'lsphp54-pecl-apc-panel','APC control panel',0,2),(69,'lsphp54-sqlite','Extension for the SQLite V2 Embeddable SQL Database Engine',0,2),(70,'lsphp54-xcache','PHP accelerator, optimizer, encoder and dynamic content cacher',0,2),(71,'lsphp54-xcache-admin','XCache Administration',0,2),(72,'lsphp55-bcmath','A module for PHP applications for using the bcmath library',1,3),(73,'lsphp55-common','Common files for PHP',1,3),(74,'lsphp55-dba','A database abstraction layer module for PHP applications',1,3),(75,'lsphp55-enchant','Human Language and Character Encoding Support',1,3),(76,'lsphp55-gd','A module for PHP applications for using the gd graphics library',1,3),(77,'lsphp55-imap','A module for PHP applications that use IMAP',1,3),(78,'lsphp55-intl','Internationalization extension for PHP application',1,3),(79,'lsphp55-ioncube-loader','Ioncube Loader',1,3),(80,'lsphp55-ldap','A module for PHP applications that use LDAP',1,3),(81,'lsphp55-mbstring','A module for PHP applications which need multi-byte string handling',1,3),(82,'lsphp55-mcrypt','Standard PHP module provides mcrypt library support',1,3),(83,'lsphp55-mysql','A module for PHP applications that use MySQL databases',1,3),(84,'lsphp55-odbc','A module for PHP applications that use ODBC databases',1,3),(85,'lsphp55-pdo','A database access abstraction module for PHP applications',1,3),(86,'lsphp55-pear','PHP Extension and Application Repository framework',1,3),(87,'lsphp55-pgsql','A PostgreSQL database module for PHP',1,3),(88,'lsphp55-process','Modules for PHP script using system process interfaces',1,3),(89,'lsphp55-pspell','A module for PHP applications for using pspell interfaces',1,3),(90,'lsphp55-recode','A module for PHP applications for using the recode library',1,3),(91,'lsphp55-snmp','A module for PHP applications that query SNMP-managed devices',1,3),(92,'lsphp55-soap','A module for PHP applications that use the SOAP protocol',1,3),(93,'lsphp55-tidy','Standard PHP module provides tidy library support',1,3),(94,'lsphp55-xml','A module for PHP applications which use XML',1,3),(95,'lsphp55-xmlrpc','A module for PHP applications which use the XML-RPC protocol',1,3),(96,'lsphp55-debuginfo','Debug information for package lsphp55',0,3),(97,'lsphp55-mysql56-debuginfo','Debug information for package lsphp55-mysql56',0,3),(98,'lsphp55-lsphp53-devel','Files needed for building PHP extensions',0,3),(99,'lsphp55-mysql56','PHP scripting language for creating dynamic web sites',0,2),(100,'lsphp55-mysqlnd','A module for PHP applications that use MySQL databases',0,3),(101,'lsphp55-opcache','The Zend OPcache',0,3),(102,'lsphp55-sqlite','Extension for the SQLite V2 Embeddable SQL Database Engine',0,3),(103,'lsphp55-xcache','PHP accelerator, optimizer, encoder and dynamic content cacher',0,3),(104,'lsphp55-xcache-admin','XCache Administration',0,3),(105,'lsphp56-bcmath','A module for PHP applications for using the bcmath library',1,4),(106,'lsphp56-common','Common files for PHP',1,4),(107,'lsphp56-dba','A database abstraction layer module for PHP applications',1,4),(108,'lsphp56-enchant','Human Language and Character Encoding Support',1,4),(109,'lsphp56-gd','A module for PHP applications for using the gd graphics library',1,4),(110,'lsphp56-gmp','A module for PHP applications for using the GNU MP library',1,4),(111,'lsphp56-imap','A module for PHP applications that use IMAP',1,4),(112,'lsphp56-intl','Internationalization extension for PHP application',1,4),(113,'lsphp56-ioncube-loader','Ioncube Loader',1,4),(114,'lsphp56-ldap','A module for PHP applications that use LDAP',1,4),(115,'lsphp56-mbstring','A module for PHP applications which need multi-byte string handling',1,4),(116,'lsphp56-mcrypt','Standard PHP module provides mcrypt library support',1,4),(117,'lsphp56-mysql','A module for PHP applications that use MySQL databases',1,4),(118,'lsphp56-odbc','A module for PHP applications that use ODBC databases',1,4),(119,'lsphp56-pdo','A database access abstraction module for PHP applications',1,4),(120,'lsphp56-pear','PHP Extension and Application Repository framework',1,3),(121,'lsphp56-pgsql','A PostgreSQL database module for PHP',1,4),(122,'lsphp56-process','Modules for PHP script using system process interfaces',1,4),(123,'lsphp56-pspell','A module for PHP applications for using pspell interfaces',1,4),(124,'lsphp56-recode','A module for PHP applications for using the recode library',1,4),(125,'lsphp56-snmp','A module for PHP applications that query SNMP-managed devices',1,4),(126,'lsphp56-soap','A module for PHP applications that use the SOAP protocol',1,4),(127,'lsphp56-tidy','Standard PHP module provides tidy library support',1,4),(128,'lsphp56-xml','A module for PHP applications which use XML',1,4),(129,'lsphp56-xmlrpc','A module for PHP applications which use the XML-RPC protocol',1,4),(130,'lsphp56-debuginfo','Debug information for package lsphp56',0,4),(131,'lsphp56-mysql56-debuginfo','Debug information for package lsphp56-mysql56',0,4),(132,'lsphp56-devel','Files needed for building PHP extensions',0,4),(133,'lsphp56-mysql56','PHP scripting language for creating dynamic web sites',0,4),(134,'lsphp56-mysqlnd','A module for PHP applications that use MySQL databases',0,4),(135,'lsphp56-opcache','The Zend OPcache',0,4),(136,'lsphp56-sqlite','Extension for the SQLite V2 Embeddable SQL Database Engine',0,4),(137,'lsphp56-xcache','PHP accelerator, optimizer, encoder and dynamic content cacher',0,4),(138,'lsphp56-xcache-admin','XCache Administration',0,4),(139,'lsphp56-pecl-imagick','Extension to create and modify images using ImageMagick',0,4),(140,'lsphp70-debuginfo','Debug information for package lsphp70',0,5),(141,'lsphp70-pecl-igbinary-debuginfo','Debug information for package lsphp70-pecl-igbinary',0,5),(142,'lsphp70-pecl-mcrypt-debuginfo','LSPHP70 lsphp70-pecl-mcrypt-debuginfo Extension',0,5),(143,'lsphp70-bcmath','A extension for PHP applications for using the bcmath library.',1,5),(144,'lsphp70-common','Common files for PHP.',1,5),(145,'lsphp70-dba','A database abstraction layer extension for PHP applications.',1,5),(146,'lsphp70-devel','Files needed for building PHP extensions.',0,5),(147,'lsphp70-enchant','Enchant spelling extension for PHP applications.',1,5),(148,'lsphp70-gd','A extension for PHP applications for using the gd graphics library.',1,5),(149,'lsphp70-gmp','A extension for PHP applications for using the GNU MP library.',1,5),(150,'lsphp70-imap','A extension for PHP applications that use IMAP.',1,5),(151,'lsphp70-intl','Internationalization extension for PHP applications.',1,5),(152,'lsphp70-json','LSPHP70 Json PHP Extension',1,5),(153,'lsphp70-ldap','A extension for PHP applications that use LDAP.',1,5),(154,'lsphp70-mbstring','A extension for PHP applications which need multi-byte string handling.',1,5),(155,'lsphp70-mysqlnd','A extension for PHP applications that use MySQL databases.',1,5),(156,'lsphp70-odbc','A extension for PHP applications that use ODBC databases.',1,5),(157,'lsphp70-opcache','The Zend OPcache.',1,5),(158,'lsphp70-pdo','A database access abstraction extension for PHP applications.',1,5),(159,'lsphp70-pear','PHP Extension and Application Repository framework.',1,5),(160,'lsphp70-pecl-apcu','APC User Cache.',0,5),(161,'lsphp70-pecl-apcu-devel','APCu developer files (header).',0,5),(162,'lsphp70-pecl-apcu-panel','APCu control panel.',0,5),(163,'lsphp70-pecl-igbinary','Replacement for the standard PHP serializer.',0,5),(164,'lsphp70-pecl-igbinary-devel','Igbinary developer files (header).',0,5),(165,'lsphp70-pecl-mcrypt','LSPHP70 lsphp70-pecl-mcrypt Extension.',0,5),(166,'lsphp70-pecl-memcache','Extension to work with the Memcached caching daemon.',0,5),(167,'lsphp70-pecl-memcached','Extension to work with the Memcached caching daemon.',0,5),(168,'lsphp70-pecl-msgpack','API for communicating with MessagePack serialization.',0,5),(169,'lsphp70-pecl-msgpack-devel','MessagePack developer files (header).',0,5),(170,'lsphp70-pecl-redis','Extension for communicating with the Redis key-value store.',0,5),(171,'lsphp70-pgsql','A PostgreSQL database extension for PHP.',1,5),(172,'lsphp70-process','extensions for PHP script using system process interfaces.',1,5),(173,'lsphp70-pspell','A extension for PHP applications for using pspell interfaces.',1,5),(174,'lsphp70-recode','A extension for PHP applications for using the recode library.',1,5),(175,'lsphp70-snmp','A extension for PHP applications that query SNMP-managed devices.',1,5),(176,'lsphp70-soap','A extension for PHP applications that use the SOAP protocol.',1,5),(177,'lsphp70-tidy','Standard PHP extension provides tidy library support.',1,5),(178,'lsphp70-xml','A module for PHP applications which use XML.',1,5),(179,'lsphp70-xmlrpc','A extension for PHP applications which use the XML-RPC protocol.',1,5),(180,'lsphp70-zip','ZIP archive management extension for PHP',0,5),(181,'lsphp70-mcrypt','Standard PHP extension provides mcrypt library support.',1,5),(182,'lsphp70-dbg','php70-dbg lsphp70-package',0,5),(183,'lsphp70-ioncube','ioncube loaders',0,5),(184,'lsphp70-pecl-imagick','Extension to create and modify images using ImageMagick',0,5),(185,'lsphp71-debuginfo','Debug information for package lsphp71',0,6),(186,'lsphp71-pecl-igbinary-debuginfo','Debug information for package lsphp71-pecl-igbinary',0,6),(187,'lsphp71-pecl-mcrypt-debuginfo','LSPHP71 lsphp71-pecl-mcrypt-debuginfo Extension',0,6),(188,'lsphp71-bcmath','A extension for PHP applications for using the bcmath library.',1,6),(189,'lsphp71-common','Common files for PHP.',1,6),(190,'lsphp71-dba','A database abstraction layer extension for PHP applications.',1,6),(191,'lsphp71-devel','Files needed for building PHP extensions.',0,6),(192,'lsphp71-enchant','Enchant spelling extension for PHP applications.',1,6),(193,'lsphp71-gd','A extension for PHP applications for using the gd graphics library.',1,6),(194,'lsphp71-gmp','A extension for PHP applications for using the GNU MP library.',1,6),(195,'lsphp71-imap','A extension for PHP applications that use IMAP.',1,6),(196,'lsphp71-intl','Internationalization extension for PHP applications.',1,6),(197,'lsphp71-json','LSPHP71 Json PHP Extension',1,6),(198,'lsphp71-ldap','A extension for PHP applications that use LDAP.',1,6),(199,'lsphp71-mbstring','A extension for PHP applications which need multi-byte string handling.',1,6),(200,'lsphp71-mysqlnd','A extension for PHP applications that use MySQL databases.',1,6),(201,'lsphp71-odbc','A extension for PHP applications that use ODBC databases.',1,6),(202,'lsphp71-opcache','The Zend OPcache.',1,6),(203,'lsphp71-pdo','A database access abstraction extension for PHP applications.',1,6),(204,'lsphp71-pear','PHP Extension and Application Repository framework.',1,6),(205,'lsphp71-pecl-apcu','APC User Cache.',0,6),(206,'lsphp71-pecl-apcu-devel','APCu developer files (header).',0,6),(207,'lsphp71-pecl-apcu-panel','APCu control panel.',0,6),(208,'lsphp71-pecl-igbinary','Replacement for the standard PHP serializer.',0,6),(209,'lsphp71-pecl-igbinary-devel','Igbinary developer files (header).',0,6),(210,'lsphp71-pecl-mcrypt','LSPHP71 lsphp71-pecl-mcrypt Extension.',0,6),(211,'lsphp71-pecl-memcache','Extension to work with the Memcached caching daemon.',0,6),(212,'lsphp71-pecl-memcached','Extension to work with the Memcached caching daemon.',0,6),(213,'lsphp71-pecl-msgpack','API for communicating with MessagePack serialization.',0,6),(214,'lsphp71-pecl-msgpack-devel','MessagePack developer files (header).',0,6),(215,'lsphp71-pecl-redis','Extension for communicating with the Redis key-value store.',0,6),(216,'lsphp71-pgsql','A PostgreSQL database extension for PHP.',1,6),(217,'lsphp71-process','extensions for PHP script using system process interfaces.',1,6),(218,'lsphp71-pspell','A extension for PHP applications for using pspell interfaces.',1,6),(219,'lsphp71-recode','A extension for PHP applications for using the recode library.',1,6),(220,'lsphp71-snmp','A extension for PHP applications that query SNMP-managed devices.',1,6),(221,'lsphp71-soap','A extension for PHP applications that use the SOAP protocol.',1,6),(222,'lsphp71-tidy','Standard PHP extension provides tidy library support.',1,6),(223,'lsphp71-xml','A module for PHP applications which use XML.',1,6),(224,'lsphp71-xmlrpc','A extension for PHP applications which use the XML-RPC protocol.',1,6),(225,'lsphp71-zip','ZIP archive management extension for PHP',0,6),(226,'lsphp71-mcrypt','Standard PHP extension provides mcrypt library support.',1,6),(227,'lsphp71-dbg','php71-dbg lsphp71-package',0,6),(228,'lsphp71-ioncube','ioncube loaders',0,6),(229,'lsphp71-pecl-imagick','Extension to create and modify images using ImageMagick',0,6),(230,'lsphp72-debuginfo','Debug information for package lsphp72',0,7),(231,'lsphp72-pecl-igbinary-debuginfo','Debug information for package lsphp72-pecl-igbinary',0,7),(232,'lsphp72-pecl-mcrypt-debuginfo','LSPHP72 lsphp72-pecl-mcrypt-debuginfo Extension',0,7),(233,'lsphp72-bcmath','A extension for PHP applications for using the bcmath library.',1,7),(234,'lsphp72-common','Common files for PHP.',1,7),(235,'lsphp72-dba','A database abstraction layer extension for PHP applications.',1,7),(236,'lsphp72-devel','Files needed for building PHP extensions.',0,7),(237,'lsphp72-enchant','Enchant spelling extension for PHP applications.',1,7),(238,'lsphp72-gd','A extension for PHP applications for using the gd graphics library.',1,7),(239,'lsphp72-gmp','A extension for PHP applications for using the GNU MP library.',1,7),(240,'lsphp72-imap','A extension for PHP applications that use IMAP.',1,7),(241,'lsphp72-intl','Internationalization extension for PHP applications.',1,7),(242,'lsphp72-json','LSPHP72 Json PHP Extension',1,7),(243,'lsphp72-ldap','A extension for PHP applications that use LDAP.',1,7),(244,'lsphp72-mbstring','A extension for PHP applications which need multi-byte string handling.',1,7),(245,'lsphp72-mysqlnd','A extension for PHP applications that use MySQL databases.',1,7),(246,'lsphp72-odbc','A extension for PHP applications that use ODBC databases.',1,7),(247,'lsphp72-opcache','The Zend OPcache.',1,7),(248,'lsphp72-pdo','A database access abstraction extension for PHP applications.',1,7),(249,'lsphp72-pear','PHP Extension and Application Repository framework.',1,7),(250,'lsphp72-pecl-apcu','APC User Cache.',0,7),(251,'lsphp72-pecl-apcu-devel','APCu developer files (header).',0,7),(252,'lsphp72-pecl-apcu-panel','APCu control panel.',0,7),(253,'lsphp72-pecl-igbinary','Replacement for the standard PHP serializer.',0,7),(254,'lsphp72-pecl-igbinary-devel','Igbinary developer files (header).',0,7),(255,'lsphp72-pecl-mcrypt','LSPHP72 lsphp72-pecl-mcrypt Extension.',0,7),(256,'lsphp72-pecl-memcache','Extension to work with the Memcached caching daemon.',0,7),(257,'lsphp72-pecl-memcached','Extension to work with the Memcached caching daemon.',0,7),(258,'lsphp72-pecl-msgpack','API for communicating with MessagePack serialization.',0,7),(259,'lsphp72-pecl-msgpack-devel','MessagePack developer files (header).',0,7),(260,'lsphp72-pecl-redis','Extension for communicating with the Redis key-value store.',0,7),(261,'lsphp72-pgsql','A PostgreSQL database extension for PHP.',1,7),(262,'lsphp72-process','extensions for PHP script using system process interfaces.',1,7),(263,'lsphp72-pspell','A extension for PHP applications for using pspell interfaces.',1,7),(264,'lsphp72-recode','A extension for PHP applications for using the recode library.',1,7),(265,'lsphp72-snmp','A extension for PHP applications that query SNMP-managed devices.',1,7),(266,'lsphp72-soap','A extension for PHP applications that use the SOAP protocol.',1,7),(267,'lsphp72-tidy','Standard PHP extension provides tidy library support.',1,7),(268,'lsphp72-xml','A module for PHP applications which use XML.',1,7),(269,'lsphp72-xmlrpc','A extension for PHP applications which use the XML-RPC protocol.',1,7),(270,'lsphp72-zip','ZIP archive management extension for PHP',0,7),(271,'lsphp72-mcrypt','Standard PHP extension provides mcrypt library support.',1,7),(272,'lsphp72-dbg','php72-dbg lsphp72-package',0,7),(273,'lsphp72-ioncube','ioncube loaders',0,7),(274,'lsphp72-pecl-imagick','Extension to create and modify images using ImageMagick',0,7),(275,'lsphp72-sodium','The php-sodium extension provides strong encryption capabilities in an easy and consistent way.',0,7),(276,'lsphp73-debuginfo','Debug information for package lsphp73',0,8),(277,'lsphp73-pecl-igbinary-debuginfo','Debug information for package lsphp73-pecl-igbinary',0,8),(278,'lsphp73-pecl-mcrypt-debuginfo','LSPHP73 lsphp73-pecl-mcrypt-debuginfo Extension',0,8),(279,'lsphp73-bcmath','A extension for PHP applications for using the bcmath library.',1,8),(280,'lsphp73-common','Common files for PHP.',1,8),(281,'lsphp73-dba','A database abstraction layer extension for PHP applications.',1,8),(282,'lsphp73-devel','Files needed for building PHP extensions.',0,8),(283,'lsphp73-enchant','Enchant spelling extension for PHP applications.',1,8),(284,'lsphp73-gd','A extension for PHP applications for using the gd graphics library.',1,8),(285,'lsphp73-gmp','A extension for PHP applications for using the GNU MP library.',1,8),(286,'lsphp73-imap','A extension for PHP applications that use IMAP.',1,8),(287,'lsphp73-intl','Internationalization extension for PHP applications.',1,8),(288,'lsphp73-json','LSPHP73 Json PHP Extension',1,8),(289,'lsphp73-ldap','A extension for PHP applications that use LDAP.',1,8),(290,'lsphp73-mbstring','A extension for PHP applications which need multi-byte string handling.',1,8),(291,'lsphp73-mysqlnd','A extension for PHP applications that use MySQL databases.',1,8),(292,'lsphp73-odbc','A extension for PHP applications that use ODBC databases.',1,8),(293,'lsphp73-opcache','The Zend OPcache.',1,8),(294,'lsphp73-pdo','A database access abstraction extension for PHP applications.',1,8),(295,'lsphp73-pear','PHP Extension and Application Repository framework.',1,8),(296,'lsphp73-pecl-apcu','APC User Cache.',0,8),(297,'lsphp73-pecl-apcu-devel','APCu developer files (header).',0,8),(298,'lsphp73-pecl-apcu-panel','APCu control panel.',0,8),(299,'lsphp73-pecl-igbinary','Replacement for the standard PHP serializer.',0,8),(300,'lsphp73-pecl-igbinary-devel','Igbinary developer files (header).',0,8),(301,'lsphp73-pecl-mcrypt','LSPHP73 lsphp73-pecl-mcrypt Extension.',0,8),(302,'lsphp73-pecl-memcache','Extension to work with the Memcached caching daemon.',0,8),(303,'lsphp73-pecl-memcached','Extension to work with the Memcached caching daemon.',0,8),(304,'lsphp73-pecl-msgpack','API for communicating with MessagePack serialization.',0,8),(305,'lsphp73-pecl-msgpack-devel','MessagePack developer files (header).',0,8),(306,'lsphp73-pecl-redis','Extension for communicating with the Redis key-value store.',0,8),(307,'lsphp73-pgsql','A PostgreSQL database extension for PHP.',1,8),(308,'lsphp73-process','extensions for PHP script using system process interfaces.',1,8),(309,'lsphp73-pspell','A extension for PHP applications for using pspell interfaces.',1,8),(310,'lsphp73-recode','A extension for PHP applications for using the recode library.',1,8),(311,'lsphp73-snmp','A extension for PHP applications that query SNMP-managed devices.',1,8),(312,'lsphp73-soap','A extension for PHP applications that use the SOAP protocol.',1,8),(313,'lsphp73-tidy','Standard PHP extension provides tidy library support.',1,8),(314,'lsphp73-xml','A module for PHP applications which use XML.',1,8),(315,'lsphp73-xmlrpc','A extension for PHP applications which use the XML-RPC protocol.',1,8),(316,'lsphp73-zip','ZIP archive management extension for PHP',0,8),(317,'lsphp73-mcrypt','Standard PHP extension provides mcrypt library support.',1,8),(318,'lsphp73-dbg','php73-dbg lsphp73-package',0,8),(319,'lsphp73-ioncube','ioncube loaders',0,8),(320,'lsphp73-pecl-imagick','Extension to create and modify images using ImageMagick',0,8),(321,'lsphp73-sodium','The php-sodium extension provides strong encryption capabilities in an easy and consistent way.',0,8),(322,'lsphp74-debuginfo','Debug information for package lsphp74',0,9),(323,'lsphp74-pecl-igbinary-debuginfo','Debug information for package lsphp74-pecl-igbinary',0,9),(324,'lsphp74-pecl-mcrypt-debuginfo','lsphp74 lsphp74-pecl-mcrypt-debuginfo Extension',0,9),(325,'lsphp74-bcmath','A extension for PHP applications for using the bcmath library.',1,9),(326,'lsphp74-common','Common files for PHP.',1,9),(327,'lsphp74-dba','A database abstraction layer extension for PHP applications.',1,9),(328,'lsphp74-devel','Files needed for building PHP extensions.',0,9),(329,'lsphp74-enchant','Enchant spelling extension for PHP applications.',1,9),(330,'lsphp74-gd','A extension for PHP applications for using the gd graphics library.',1,9),(331,'lsphp74-gmp','A extension for PHP applications for using the GNU MP library.',1,9),(332,'lsphp74-imap','A extension for PHP applications that use IMAP.',1,9),(333,'lsphp74-intl','Internationalization extension for PHP applications.',1,9),(334,'lsphp74-json','lsphp74 Json PHP Extension',1,9),(335,'lsphp74-ldap','A extension for PHP applications that use LDAP.',1,9),(336,'lsphp74-mbstring','A extension for PHP applications which need multi-byte string handling.',1,9),(337,'lsphp74-mysqlnd','A extension for PHP applications that use MySQL databases.',1,9),(338,'lsphp74-odbc','A extension for PHP applications that use ODBC databases.',1,9),(339,'lsphp74-opcache','The Zend OPcache.',1,9),(340,'lsphp74-pdo','A database access abstraction extension for PHP applications.',1,9),(341,'lsphp74-pear','PHP Extension and Application Repository framework.',1,9),(342,'lsphp74-pecl-apcu','APC User Cache.',0,9),(343,'lsphp74-pecl-apcu-devel','APCu developer files (header).',0,9),(344,'lsphp74-pecl-apcu-panel','APCu control panel.',0,9),(345,'lsphp74-pecl-igbinary','Replacement for the standard PHP serializer.',0,9),(346,'lsphp74-pecl-igbinary-devel','Igbinary developer files (header).',0,9),(347,'lsphp74-pecl-mcrypt','lsphp74 lsphp74-pecl-mcrypt Extension.',0,9),(348,'lsphp74-pecl-memcache','Extension to work with the Memcached caching daemon.',0,9),(349,'lsphp74-pecl-memcached','Extension to work with the Memcached caching daemon.',0,9),(350,'lsphp74-pecl-msgpack','API for communicating with MessagePack serialization.',0,9),(351,'lsphp74-pecl-msgpack-devel','MessagePack developer files (header).',0,9),(352,'lsphp74-pecl-redis','Extension for communicating with the Redis key-value store.',0,9),(353,'lsphp74-pgsql','A PostgreSQL database extension for PHP.',1,9),(354,'lsphp74-process','extensions for PHP script using system process interfaces.',1,9),(355,'lsphp74-pspell','A extension for PHP applications for using pspell interfaces.',1,9),(356,'lsphp74-recode','A extension for PHP applications for using the recode library.',1,9),(357,'lsphp74-snmp','A extension for PHP applications that query SNMP-managed devices.',1,9),(358,'lsphp74-soap','A extension for PHP applications that use the SOAP protocol.',1,9),(359,'lsphp74-tidy','Standard PHP extension provides tidy library support.',1,9),(360,'lsphp74-xml','A module for PHP applications which use XML.',1,9),(361,'lsphp74-xmlrpc','A extension for PHP applications which use the XML-RPC protocol.',1,9),(362,'lsphp74-zip','ZIP archive management extension for PHP',0,9),(363,'lsphp74-mcrypt','Standard PHP extension provides mcrypt library support.',1,9),(364,'lsphp74-dbg','php73-dbg lsphp74-package',0,9),(365,'lsphp74-ioncube','ioncube loaders',0,9),(366,'lsphp74-pecl-imagick','Extension to create and modify images using ImageMagick',0,9),(367,'lsphp74-sodium','The php-sodium extension provides strong encryption capabilities in an easy and consistent way.',0,9),(368,'lsphp80-debuginfo','Debug information for package lsphp80',0,10),(369,'lsphp80-pecl-igbinary-debuginfo','Debug information for package lsphp80-pecl-igbinary',0,10),(370,'lsphp80-pecl-mcrypt-debuginfo','lsphp80 lsphp80-pecl-mcrypt-debuginfo Extension',0,10),(371,'lsphp80-bcmath','A extension for PHP applications for using the bcmath library.',1,10),(372,'lsphp80-common','Common files for PHP.',1,10),(373,'lsphp80-dba','A database abstraction layer extension for PHP applications.',1,10),(374,'lsphp80-devel','Files needed for building PHP extensions.',0,10),(375,'lsphp80-enchant','Enchant spelling extension for PHP applications.',1,10),(376,'lsphp80-gd','A extension for PHP applications for using the gd graphics library.',1,10),(377,'lsphp80-gmp','A extension for PHP applications for using the GNU MP library.',1,10),(378,'lsphp80-imap','A extension for PHP applications that use IMAP.',1,10),(379,'lsphp80-intl','Internationalization extension for PHP applications.',1,10),(380,'lsphp80-json','lsphp80 Json PHP Extension',1,10),(381,'lsphp80-ldap','A extension for PHP applications that use LDAP.',1,10),(382,'lsphp80-mbstring','A extension for PHP applications which need multi-byte string handling.',1,10),(383,'lsphp80-mysqlnd','A extension for PHP applications that use MySQL databases.',1,10),(384,'lsphp80-odbc','A extension for PHP applications that use ODBC databases.',1,10),(385,'lsphp80-opcache','The Zend OPcache.',1,10),(386,'lsphp80-pdo','A database access abstraction extension for PHP applications.',1,10),(387,'lsphp80-pear','PHP Extension and Application Repository framework.',1,10),(388,'lsphp80-pecl-apcu','APC User Cache.',0,10),(389,'lsphp80-pecl-apcu-devel','APCu developer files (header).',0,10),(390,'lsphp80-pecl-apcu-panel','APCu control panel.',0,10),(391,'lsphp80-pecl-igbinary','Replacement for the standard PHP serializer.',0,10),(392,'lsphp80-pecl-igbinary-devel','Igbinary developer files (header).',0,10),(393,'lsphp80-pecl-mcrypt','lsphp80 lsphp80-pecl-mcrypt Extension.',0,10),(394,'lsphp80-pecl-memcache','Extension to work with the Memcached caching daemon.',0,10),(395,'lsphp80-pecl-memcached','Extension to work with the Memcached caching daemon.',0,10),(396,'lsphp80-pecl-msgpack','API for communicating with MessagePack serialization.',0,10),(397,'lsphp80-pecl-msgpack-devel','MessagePack developer files (header).',0,10),(398,'lsphp80-pecl-redis','Extension for communicating with the Redis key-value store.',0,10),(399,'lsphp80-pgsql','A PostgreSQL database extension for PHP.',1,10),(400,'lsphp80-process','extensions for PHP script using system process interfaces.',1,10),(401,'lsphp80-pspell','A extension for PHP applications for using pspell interfaces.',1,10),(402,'lsphp80-recode','A extension for PHP applications for using the recode library.',1,10),(403,'lsphp80-snmp','A extension for PHP applications that query SNMP-managed devices.',1,10),(404,'lsphp80-soap','A extension for PHP applications that use the SOAP protocol.',1,10),(405,'lsphp80-tidy','Standard PHP extension provides tidy library support.',1,10),(406,'lsphp80-xml','A module for PHP applications which use XML.',1,10),(407,'lsphp80-xmlrpc','A extension for PHP applications which use the XML-RPC protocol.',1,10),(408,'lsphp80-zip','ZIP archive management extension for PHP',0,10),(409,'lsphp80-mcrypt','Standard PHP extension provides mcrypt library support.',1,10),(410,'lsphp80-dbg','php73-dbg lsphp80-package',0,10),(411,'lsphp80-ioncube','ioncube loaders',0,10),(412,'lsphp80-pecl-imagick','Extension to create and modify images using ImageMagick',0,10),(413,'lsphp80-sodium','The php-sodium extension provides strong encryption capabilities in an easy and consistent way.',0,10);
/*!40000 ALTER TABLE `php_lib` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `php_version`
--

DROP TABLE IF EXISTS `php_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `php_version` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phpVers` varchar(5) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phpVers` (`phpVers`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `php_version`
--

LOCK TABLES `php_version` WRITE;
/*!40000 ALTER TABLE `php_version` DISABLE KEYS */;
INSERT INTO `php_version` VALUES (1,'php53'),(2,'php54'),(3,'php55'),(4,'php56'),(5,'php70'),(6,'php71'),(7,'php72'),(8,'php73'),(9,'php74'),(10,'php80');
/*!40000 ALTER TABLE `php_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `records`
--

DROP TABLE IF EXISTS `records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `records` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `domain_id` int(11) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL,
  `content` varchar(64000) DEFAULT NULL,
  `ttl` int(11) DEFAULT NULL,
  `prio` int(11) DEFAULT NULL,
  `disabled` tinyint(1) DEFAULT 0,
  `ordername` varchar(255) CHARACTER SET latin1 COLLATE latin1_bin DEFAULT NULL,
  `auth` tinyint(1) DEFAULT 1,
  `userid` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `nametype_index` (`name`,`type`),
  KEY `domain_id` (`domain_id`),
  KEY `ordername` (`ordername`)
) ENGINE=InnoDB AUTO_INCREMENT=500 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `records`
--


--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_association` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int(11) NOT NULL,
  `lifetime` int(11) NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_association`
--

LOCK TABLES `social_auth_association` WRITE;
/*!40000 ALTER TABLE `social_auth_association` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_association` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_code`
--

DROP TABLE IF EXISTS `social_auth_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_code` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  KEY `social_auth_code_code_a2393167` (`code`),
  KEY `social_auth_code_timestamp_176b341f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_code`
--

LOCK TABLES `social_auth_code` WRITE;
/*!40000 ALTER TABLE `social_auth_code` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_code` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_nonce` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int(11) NOT NULL,
  `salt` varchar(65) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_nonce`
--

LOCK TABLES `social_auth_nonce` WRITE;
/*!40000 ALTER TABLE `social_auth_nonce` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_nonce` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_partial`
--

DROP TABLE IF EXISTS `social_auth_partial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_partial` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `next_step` smallint(5) unsigned NOT NULL,
  `backend` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `data` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `social_auth_partial_token_3017fea3` (`token`),
  KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_partial`
--

LOCK TABLES `social_auth_partial` WRITE;
/*!40000 ALTER TABLE `social_auth_partial` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_partial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `extra_data` longtext NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` (`user_id`),
  KEY `social_auth_usersocialauth_uid_796e51dc` (`uid`),
  CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `social_auth_usersocialauth`
--

LOCK TABLES `social_auth_usersocialauth` WRITE;
/*!40000 ALTER TABLE `social_auth_usersocialauth` DISABLE KEYS */;
/*!40000 ALTER TABLE `social_auth_usersocialauth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supermasters`
--

DROP TABLE IF EXISTS `supermasters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supermasters` (
  `ip` varchar(64) NOT NULL,
  `nameserver` varchar(255) NOT NULL,
  `account` varchar(40) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`ip`,`nameserver`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supermasters`
--

LOCK TABLES `supermasters` WRITE;
/*!40000 ALTER TABLE `supermasters` DISABLE KEYS */;
/*!40000 ALTER TABLE `supermasters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `timezone`
--

DROP TABLE IF EXISTS `timezone`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timezone` (
  `country_code` char(3) NOT NULL,
  `timezone` varchar(125) NOT NULL DEFAULT '',
  `gmt_offset` float(10,2) DEFAULT NULL,
  `dst_offset` float(10,2) DEFAULT NULL,
  `raw_offset` float(10,2) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`country_code`,`timezone`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=419 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timezone`
--

LOCK TABLES `timezone` WRITE;
/*!40000 ALTER TABLE `timezone` DISABLE KEYS */;
INSERT INTO `timezone` VALUES ('AD','Europe/Andorra',1.00,2.00,1.00,1),('AE','Asia/Dubai',4.00,4.00,4.00,2),('AF','Asia/Kabul',4.50,4.50,4.50,3),('AG','America/Antigua',-4.00,-4.00,-4.00,4),('AI','America/Anguilla',-4.00,-4.00,-4.00,5),('AL','Europe/Tirane',1.00,2.00,1.00,6),('AM','Asia/Yerevan',4.00,4.00,4.00,7),('AO','Africa/Luanda',1.00,1.00,1.00,8),('AQ','Antarctica/Casey',8.00,8.00,8.00,9),('AQ','Antarctica/Davis',7.00,7.00,7.00,10),('AQ','Antarctica/DumontDUrville',10.00,10.00,10.00,11),('AQ','Antarctica/Mawson',5.00,5.00,5.00,12),('AQ','Antarctica/McMurdo',13.00,12.00,12.00,13),('AQ','Antarctica/Palmer',-3.00,-4.00,-4.00,14),('AQ','Antarctica/Rothera',-3.00,-3.00,-3.00,15),('AQ','Antarctica/South_Pole',13.00,12.00,12.00,16),('AQ','Antarctica/Syowa',3.00,3.00,3.00,17),('AQ','Antarctica/Vostok',6.00,6.00,6.00,18),('AR','America/Argentina/Buenos_Aires',-3.00,-3.00,-3.00,19),('AR','America/Argentina/Catamarca',-3.00,-3.00,-3.00,20),('AR','America/Argentina/Cordoba',-3.00,-3.00,-3.00,21),('AR','America/Argentina/Jujuy',-3.00,-3.00,-3.00,22),('AR','America/Argentina/La_Rioja',-3.00,-3.00,-3.00,23),('AR','America/Argentina/Mendoza',-3.00,-3.00,-3.00,24),('AR','America/Argentina/Rio_Gallegos',-3.00,-3.00,-3.00,25),('AR','America/Argentina/Salta',-3.00,-3.00,-3.00,26),('AR','America/Argentina/San_Juan',-3.00,-3.00,-3.00,27),('AR','America/Argentina/San_Luis',-3.00,-3.00,-3.00,28),('AR','America/Argentina/Tucuman',-3.00,-3.00,-3.00,29),('AR','America/Argentina/Ushuaia',-3.00,-3.00,-3.00,30),('AS','Pacific/Pago_Pago',-11.00,-11.00,-11.00,31),('AT','Europe/Vienna',1.00,2.00,1.00,32),('AU','Antarctica/Macquarie',11.00,11.00,11.00,33),('AU','Australia/Adelaide',10.50,9.50,9.50,34),('AU','Australia/Brisbane',10.00,10.00,10.00,35),('AU','Australia/Broken_Hill',10.50,9.50,9.50,36),('AU','Australia/Currie',11.00,10.00,10.00,37),('AU','Australia/Darwin',9.50,9.50,9.50,38),('AU','Australia/Eucla',8.75,8.75,8.75,39),('AU','Australia/Hobart',11.00,10.00,10.00,40),('AU','Australia/Lindeman',10.00,10.00,10.00,41),('AU','Australia/Lord_Howe',11.00,10.50,10.50,42),('AU','Australia/Melbourne',11.00,10.00,10.00,43),('AU','Australia/Perth',8.00,8.00,8.00,44),('AU','Australia/Sydney',11.00,10.00,10.00,45),('AW','America/Aruba',-4.00,-4.00,-4.00,46),('AX','Europe/Mariehamn',2.00,3.00,2.00,47),('AZ','Asia/Baku',4.00,5.00,4.00,48),('BA','Europe/Sarajevo',1.00,2.00,1.00,49),('BB','America/Barbados',-4.00,-4.00,-4.00,50),('BD','Asia/Dhaka',6.00,6.00,6.00,51),('BE','Europe/Brussels',1.00,2.00,1.00,52),('BF','Africa/Ouagadougou',0.00,0.00,0.00,53),('BG','Europe/Sofia',2.00,3.00,2.00,54),('BH','Asia/Bahrain',3.00,3.00,3.00,55),('BI','Africa/Bujumbura',2.00,2.00,2.00,56),('BJ','Africa/Porto-Novo',1.00,1.00,1.00,57),('BL','America/St_Barthelemy',-4.00,-4.00,-4.00,58),('BM','Atlantic/Bermuda',-4.00,-3.00,-4.00,59),('BN','Asia/Brunei',8.00,8.00,8.00,60),('BO','America/La_Paz',-4.00,-4.00,-4.00,61),('BQ','America/Kralendijk',-4.00,-4.00,-4.00,62),('BR','America/Araguaina',-3.00,-3.00,-3.00,63),('BR','America/Bahia',-3.00,-3.00,-3.00,64),('BR','America/Belem',-3.00,-3.00,-3.00,65),('BR','America/Boa_Vista',-4.00,-4.00,-4.00,66),('BR','America/Campo_Grande',-3.00,-4.00,-4.00,67),('BR','America/Cuiaba',-3.00,-4.00,-4.00,68),('BR','America/Eirunepe',-5.00,-5.00,-5.00,69),('BR','America/Fortaleza',-3.00,-3.00,-3.00,70),('BR','America/Maceio',-3.00,-3.00,-3.00,71),('BR','America/Manaus',-4.00,-4.00,-4.00,72),('BR','America/Noronha',-2.00,-2.00,-2.00,73),('BR','America/Porto_Velho',-4.00,-4.00,-4.00,74),('BR','America/Recife',-3.00,-3.00,-3.00,75),('BR','America/Rio_Branco',-5.00,-5.00,-5.00,76),('BR','America/Santarem',-3.00,-3.00,-3.00,77),('BR','America/Sao_Paulo',-2.00,-3.00,-3.00,78),('BS','America/Nassau',-5.00,-4.00,-5.00,79),('BT','Asia/Thimphu',6.00,6.00,6.00,80),('BW','Africa/Gaborone',2.00,2.00,2.00,81),('BY','Europe/Minsk',3.00,3.00,3.00,82),('BZ','America/Belize',-6.00,-6.00,-6.00,83),('CA','America/Atikokan',-5.00,-5.00,-5.00,84),('CA','America/Blanc-Sablon',-4.00,-4.00,-4.00,85),('CA','America/Cambridge_Bay',-7.00,-6.00,-7.00,86),('CA','America/Creston',-7.00,-7.00,-7.00,87),('CA','America/Dawson',-8.00,-7.00,-8.00,88),('CA','America/Dawson_Creek',-7.00,-7.00,-7.00,89),('CA','America/Edmonton',-7.00,-6.00,-7.00,90),('CA','America/Glace_Bay',-4.00,-3.00,-4.00,91),('CA','America/Goose_Bay',-4.00,-3.00,-4.00,92),('CA','America/Halifax',-4.00,-3.00,-4.00,93),('CA','America/Inuvik',-7.00,-6.00,-7.00,94),('CA','America/Iqaluit',-5.00,-4.00,-5.00,95),('CA','America/Moncton',-4.00,-3.00,-4.00,96),('CA','America/Montreal',-5.00,-4.00,-5.00,97),('CA','America/Nipigon',-5.00,-4.00,-5.00,98),('CA','America/Pangnirtung',-5.00,-4.00,-5.00,99),('CA','America/Rainy_River',-6.00,-5.00,-6.00,100),('CA','America/Rankin_Inlet',-6.00,-5.00,-6.00,101),('CA','America/Regina',-6.00,-6.00,-6.00,102),('CA','America/Resolute',-6.00,-5.00,-6.00,103),('CA','America/St_Johns',-3.50,-2.50,-3.50,104),('CA','America/Swift_Current',-6.00,-6.00,-6.00,105),('CA','America/Thunder_Bay',-5.00,-4.00,-5.00,106),('CA','America/Toronto',-5.00,-4.00,-5.00,107),('CA','America/Vancouver',-8.00,-7.00,-8.00,108),('CA','America/Whitehorse',-8.00,-7.00,-8.00,109),('CA','America/Winnipeg',-6.00,-5.00,-6.00,110),('CA','America/Yellowknife',-7.00,-6.00,-7.00,111),('CC','Indian/Cocos',6.50,6.50,6.50,112),('CD','Africa/Kinshasa',1.00,1.00,1.00,113),('CD','Africa/Lubumbashi',2.00,2.00,2.00,114),('CF','Africa/Bangui',1.00,1.00,1.00,115),('CG','Africa/Brazzaville',1.00,1.00,1.00,116),('CH','Europe/Zurich',1.00,2.00,1.00,117),('CI','Africa/Abidjan',0.00,0.00,0.00,118),('CK','Pacific/Rarotonga',-10.00,-10.00,-10.00,119),('CL','America/Santiago',-3.00,-4.00,-4.00,120),('CL','Pacific/Easter',-5.00,-6.00,-6.00,121),('CM','Africa/Douala',1.00,1.00,1.00,122),('CN','Asia/Chongqing',8.00,8.00,8.00,123),('CN','Asia/Harbin',8.00,8.00,8.00,124),('CN','Asia/Kashgar',8.00,8.00,8.00,125),('CN','Asia/Shanghai',8.00,8.00,8.00,126),('CN','Asia/Urumqi',8.00,8.00,8.00,127),('CO','America/Bogota',-5.00,-5.00,-5.00,128),('CR','America/Costa_Rica',-6.00,-6.00,-6.00,129),('CU','America/Havana',-5.00,-4.00,-5.00,130),('CV','Atlantic/Cape_Verde',-1.00,-1.00,-1.00,131),('CW','America/Curacao',-4.00,-4.00,-4.00,132),('CX','Indian/Christmas',7.00,7.00,7.00,133),('CY','Asia/Nicosia',2.00,3.00,2.00,134),('CZ','Europe/Prague',1.00,2.00,1.00,135),('DE','Europe/Berlin',1.00,2.00,1.00,136),('DE','Europe/Busingen',1.00,2.00,1.00,137),('DJ','Africa/Djibouti',3.00,3.00,3.00,138),('DK','Europe/Copenhagen',1.00,2.00,1.00,139),('DM','America/Dominica',-4.00,-4.00,-4.00,140),('DO','America/Santo_Domingo',-4.00,-4.00,-4.00,141),('DZ','Africa/Algiers',1.00,1.00,1.00,142),('EC','America/Guayaquil',-5.00,-5.00,-5.00,143),('EC','Pacific/Galapagos',-6.00,-6.00,-6.00,144),('EE','Europe/Tallinn',2.00,3.00,2.00,145),('EG','Africa/Cairo',2.00,2.00,2.00,146),('EH','Africa/El_Aaiun',0.00,0.00,0.00,147),('ER','Africa/Asmara',3.00,3.00,3.00,148),('ES','Africa/Ceuta',1.00,2.00,1.00,149),('ES','Atlantic/Canary',0.00,1.00,0.00,150),('ES','Europe/Madrid',1.00,2.00,1.00,151),('ET','Africa/Addis_Ababa',3.00,3.00,3.00,152),('FI','Europe/Helsinki',2.00,3.00,2.00,153),('FJ','Pacific/Fiji',13.00,12.00,12.00,154),('FK','Atlantic/Stanley',-3.00,-3.00,-3.00,155),('FM','Pacific/Chuuk',10.00,10.00,10.00,156),('FM','Pacific/Kosrae',11.00,11.00,11.00,157),('FM','Pacific/Pohnpei',11.00,11.00,11.00,158),('FO','Atlantic/Faroe',0.00,1.00,0.00,159),('FR','Europe/Paris',1.00,2.00,1.00,160),('GA','Africa/Libreville',1.00,1.00,1.00,161),('GB','Europe/London',0.00,1.00,0.00,162),('GD','America/Grenada',-4.00,-4.00,-4.00,163),('GE','Asia/Tbilisi',4.00,4.00,4.00,164),('GF','America/Cayenne',-3.00,-3.00,-3.00,165),('GG','Europe/Guernsey',0.00,1.00,0.00,166),('GH','Africa/Accra',0.00,0.00,0.00,167),('GI','Europe/Gibraltar',1.00,2.00,1.00,168),('GL','America/Danmarkshavn',0.00,0.00,0.00,169),('GL','America/Godthab',-3.00,-2.00,-3.00,170),('GL','America/Scoresbysund',-1.00,0.00,-1.00,171),('GL','America/Thule',-4.00,-3.00,-4.00,172),('GM','Africa/Banjul',0.00,0.00,0.00,173),('GN','Africa/Conakry',0.00,0.00,0.00,174),('GP','America/Guadeloupe',-4.00,-4.00,-4.00,175),('GQ','Africa/Malabo',1.00,1.00,1.00,176),('GR','Europe/Athens',2.00,3.00,2.00,177),('GS','Atlantic/South_Georgia',-2.00,-2.00,-2.00,178),('GT','America/Guatemala',-6.00,-6.00,-6.00,179),('GU','Pacific/Guam',10.00,10.00,10.00,180),('GW','Africa/Bissau',0.00,0.00,0.00,181),('GY','America/Guyana',-4.00,-4.00,-4.00,182),('HK','Asia/Hong_Kong',8.00,8.00,8.00,183),('HN','America/Tegucigalpa',-6.00,-6.00,-6.00,184),('HR','Europe/Zagreb',1.00,2.00,1.00,185),('HT','America/Port-au-Prince',-5.00,-4.00,-5.00,186),('HU','Europe/Budapest',1.00,2.00,1.00,187),('ID','Asia/Jakarta',7.00,7.00,7.00,188),('ID','Asia/Jayapura',9.00,9.00,9.00,189),('ID','Asia/Makassar',8.00,8.00,8.00,190),('ID','Asia/Pontianak',7.00,7.00,7.00,191),('IE','Europe/Dublin',0.00,1.00,0.00,192),('IL','Asia/Jerusalem',2.00,3.00,2.00,193),('IM','Europe/Isle_of_Man',0.00,1.00,0.00,194),('IN','Asia/Kolkata',5.50,5.50,5.50,195),('IO','Indian/Chagos',6.00,6.00,6.00,196),('IQ','Asia/Baghdad',3.00,3.00,3.00,197),('IR','Asia/Tehran',3.50,4.50,3.50,198),('IS','Atlantic/Reykjavik',0.00,0.00,0.00,199),('IT','Europe/Rome',1.00,2.00,1.00,200),('JE','Europe/Jersey',0.00,1.00,0.00,201),('JM','America/Jamaica',-5.00,-5.00,-5.00,202),('JO','Asia/Amman',2.00,3.00,2.00,203),('JP','Asia/Tokyo',9.00,9.00,9.00,204),('KE','Africa/Nairobi',3.00,3.00,3.00,205),('KG','Asia/Bishkek',6.00,6.00,6.00,206),('KH','Asia/Phnom_Penh',7.00,7.00,7.00,207),('KI','Pacific/Enderbury',13.00,13.00,13.00,208),('KI','Pacific/Kiritimati',14.00,14.00,14.00,209),('KI','Pacific/Tarawa',12.00,12.00,12.00,210),('KM','Indian/Comoro',3.00,3.00,3.00,211),('KN','America/St_Kitts',-4.00,-4.00,-4.00,212),('KP','Asia/Pyongyang',9.00,9.00,9.00,213),('KR','Asia/Seoul',9.00,9.00,9.00,214),('KW','Asia/Kuwait',3.00,3.00,3.00,215),('KY','America/Cayman',-5.00,-5.00,-5.00,216),('KZ','Asia/Almaty',6.00,6.00,6.00,217),('KZ','Asia/Aqtau',5.00,5.00,5.00,218),('KZ','Asia/Aqtobe',5.00,5.00,5.00,219),('KZ','Asia/Oral',5.00,5.00,5.00,220),('KZ','Asia/Qyzylorda',6.00,6.00,6.00,221),('LA','Asia/Vientiane',7.00,7.00,7.00,222),('LB','Asia/Beirut',2.00,3.00,2.00,223),('LC','America/St_Lucia',-4.00,-4.00,-4.00,224),('LI','Europe/Vaduz',1.00,2.00,1.00,225),('LK','Asia/Colombo',5.50,5.50,5.50,226),('LR','Africa/Monrovia',0.00,0.00,0.00,227),('LS','Africa/Maseru',2.00,2.00,2.00,228),('LT','Europe/Vilnius',2.00,3.00,2.00,229),('LU','Europe/Luxembourg',1.00,2.00,1.00,230),('LV','Europe/Riga',2.00,3.00,2.00,231),('LY','Africa/Tripoli',2.00,2.00,2.00,232),('MA','Africa/Casablanca',0.00,0.00,0.00,233),('MC','Europe/Monaco',1.00,2.00,1.00,234),('MD','Europe/Chisinau',2.00,3.00,2.00,235),('ME','Europe/Podgorica',1.00,2.00,1.00,236),('MF','America/Marigot',-4.00,-4.00,-4.00,237),('MG','Indian/Antananarivo',3.00,3.00,3.00,238),('MH','Pacific/Kwajalein',12.00,12.00,12.00,239),('MH','Pacific/Majuro',12.00,12.00,12.00,240),('MK','Europe/Skopje',1.00,2.00,1.00,241),('ML','Africa/Bamako',0.00,0.00,0.00,242),('MM','Asia/Rangoon',6.50,6.50,6.50,243),('MN','Asia/Choibalsan',8.00,8.00,8.00,244),('MN','Asia/Hovd',7.00,7.00,7.00,245),('MN','Asia/Ulaanbaatar',8.00,8.00,8.00,246),('MO','Asia/Macau',8.00,8.00,8.00,247),('MP','Pacific/Saipan',10.00,10.00,10.00,248),('MQ','America/Martinique',-4.00,-4.00,-4.00,249),('MR','Africa/Nouakchott',0.00,0.00,0.00,250),('MS','America/Montserrat',-4.00,-4.00,-4.00,251),('MT','Europe/Malta',1.00,2.00,1.00,252),('MU','Indian/Mauritius',4.00,4.00,4.00,253),('MV','Indian/Maldives',5.00,5.00,5.00,254),('MW','Africa/Blantyre',2.00,2.00,2.00,255),('MX','America/Bahia_Banderas',-6.00,-5.00,-6.00,256),('MX','America/Cancun',-6.00,-5.00,-6.00,257),('MX','America/Chihuahua',-7.00,-6.00,-7.00,258),('MX','America/Hermosillo',-7.00,-7.00,-7.00,259),('MX','America/Matamoros',-6.00,-5.00,-6.00,260),('MX','America/Mazatlan',-7.00,-6.00,-7.00,261),('MX','America/Merida',-6.00,-5.00,-6.00,262),('MX','America/Mexico_City',-6.00,-5.00,-6.00,263),('MX','America/Monterrey',-6.00,-5.00,-6.00,264),('MX','America/Ojinaga',-7.00,-6.00,-7.00,265),('MX','America/Santa_Isabel',-8.00,-7.00,-8.00,266),('MX','America/Tijuana',-8.00,-7.00,-8.00,267),('MY','Asia/Kuala_Lumpur',8.00,8.00,8.00,268),('MY','Asia/Kuching',8.00,8.00,8.00,269),('MZ','Africa/Maputo',2.00,2.00,2.00,270),('NA','Africa/Windhoek',2.00,1.00,1.00,271),('NC','Pacific/Noumea',11.00,11.00,11.00,272),('NE','Africa/Niamey',1.00,1.00,1.00,273),('NF','Pacific/Norfolk',11.50,11.50,11.50,274),('NG','Africa/Lagos',1.00,1.00,1.00,275),('NI','America/Managua',-6.00,-6.00,-6.00,276),('NL','Europe/Amsterdam',1.00,2.00,1.00,277),('NO','Europe/Oslo',1.00,2.00,1.00,278),('NP','Asia/Kathmandu',5.75,5.75,5.75,279),('NR','Pacific/Nauru',12.00,12.00,12.00,280),('NU','Pacific/Niue',-11.00,-11.00,-11.00,281),('NZ','Pacific/Auckland',13.00,12.00,12.00,282),('NZ','Pacific/Chatham',13.75,12.75,12.75,283),('OM','Asia/Muscat',4.00,4.00,4.00,284),('PA','America/Panama',-5.00,-5.00,-5.00,285),('PE','America/Lima',-5.00,-5.00,-5.00,286),('PF','Pacific/Gambier',-9.00,-9.00,-9.00,287),('PF','Pacific/Marquesas',-9.50,-9.50,-9.50,288),('PF','Pacific/Tahiti',-10.00,-10.00,-10.00,289),('PG','Pacific/Port_Moresby',10.00,10.00,10.00,290),('PH','Asia/Manila',8.00,8.00,8.00,291),('PK','Asia/Karachi',5.00,5.00,5.00,292),('PL','Europe/Warsaw',1.00,2.00,1.00,293),('PM','America/Miquelon',-3.00,-2.00,-3.00,294),('PN','Pacific/Pitcairn',-8.00,-8.00,-8.00,295),('PR','America/Puerto_Rico',-4.00,-4.00,-4.00,296),('PS','Asia/Gaza',2.00,3.00,2.00,297),('PS','Asia/Hebron',2.00,3.00,2.00,298),('PT','Atlantic/Azores',-1.00,0.00,-1.00,299),('PT','Atlantic/Madeira',0.00,1.00,0.00,300),('PT','Europe/Lisbon',0.00,1.00,0.00,301),('PW','Pacific/Palau',9.00,9.00,9.00,302),('PY','America/Asuncion',-3.00,-4.00,-4.00,303),('QA','Asia/Qatar',3.00,3.00,3.00,304),('RE','Indian/Reunion',4.00,4.00,4.00,305),('RO','Europe/Bucharest',2.00,3.00,2.00,306),('RS','Europe/Belgrade',1.00,2.00,1.00,307),('RU','Asia/Anadyr',12.00,12.00,12.00,308),('RU','Asia/Irkutsk',9.00,9.00,9.00,309),('RU','Asia/Kamchatka',12.00,12.00,12.00,310),('RU','Asia/Khandyga',10.00,10.00,10.00,311),('RU','Asia/Krasnoyarsk',8.00,8.00,8.00,312),('RU','Asia/Magadan',12.00,12.00,12.00,313),('RU','Asia/Novokuznetsk',7.00,7.00,7.00,314),('RU','Asia/Novosibirsk',7.00,7.00,7.00,315),('RU','Asia/Omsk',7.00,7.00,7.00,316),('RU','Asia/Sakhalin',11.00,11.00,11.00,317),('RU','Asia/Ust-Nera',11.00,11.00,11.00,318),('RU','Asia/Vladivostok',11.00,11.00,11.00,319),('RU','Asia/Yakutsk',10.00,10.00,10.00,320),('RU','Asia/Yekaterinburg',6.00,6.00,6.00,321),('RU','Europe/Kaliningrad',3.00,3.00,3.00,322),('RU','Europe/Moscow',4.00,4.00,4.00,323),('RU','Europe/Samara',4.00,4.00,4.00,324),('RU','Europe/Volgograd',4.00,4.00,4.00,325),('RW','Africa/Kigali',2.00,2.00,2.00,326),('SA','Asia/Riyadh',3.00,3.00,3.00,327),('SB','Pacific/Guadalcanal',11.00,11.00,11.00,328),('SC','Indian/Mahe',4.00,4.00,4.00,329),('SD','Africa/Khartoum',3.00,3.00,3.00,330),('SE','Europe/Stockholm',1.00,2.00,1.00,331),('SG','Asia/Singapore',8.00,8.00,8.00,332),('SH','Atlantic/St_Helena',0.00,0.00,0.00,333),('SI','Europe/Ljubljana',1.00,2.00,1.00,334),('SJ','Arctic/Longyearbyen',1.00,2.00,1.00,335),('SK','Europe/Bratislava',1.00,2.00,1.00,336),('SL','Africa/Freetown',0.00,0.00,0.00,337),('SM','Europe/San_Marino',1.00,2.00,1.00,338),('SN','Africa/Dakar',0.00,0.00,0.00,339),('SO','Africa/Mogadishu',3.00,3.00,3.00,340),('SR','America/Paramaribo',-3.00,-3.00,-3.00,341),('SS','Africa/Juba',3.00,3.00,3.00,342),('ST','Africa/Sao_Tome',0.00,0.00,0.00,343),('SV','America/El_Salvador',-6.00,-6.00,-6.00,344),('SX','America/Lower_Princes',-4.00,-4.00,-4.00,345),('SY','Asia/Damascus',2.00,3.00,2.00,346),('SZ','Africa/Mbabane',2.00,2.00,2.00,347),('TC','America/Grand_Turk',-5.00,-4.00,-5.00,348),('TD','Africa/Ndjamena',1.00,1.00,1.00,349),('TF','Indian/Kerguelen',5.00,5.00,5.00,350),('TG','Africa/Lome',0.00,0.00,0.00,351),('TH','Asia/Bangkok',7.00,7.00,7.00,352),('TJ','Asia/Dushanbe',5.00,5.00,5.00,353),('TK','Pacific/Fakaofo',13.00,13.00,13.00,354),('TL','Asia/Dili',9.00,9.00,9.00,355),('TM','Asia/Ashgabat',5.00,5.00,5.00,356),('TN','Africa/Tunis',1.00,1.00,1.00,357),('TO','Pacific/Tongatapu',13.00,13.00,13.00,358),('TR','Europe/Istanbul',2.00,3.00,2.00,359),('TT','America/Port_of_Spain',-4.00,-4.00,-4.00,360),('TV','Pacific/Funafuti',12.00,12.00,12.00,361),('TW','Asia/Taipei',8.00,8.00,8.00,362),('TZ','Africa/Dar_es_Salaam',3.00,3.00,3.00,363),('UA','Europe/Kiev',2.00,3.00,2.00,364),('UA','Europe/Simferopol',2.00,4.00,4.00,365),('UA','Europe/Uzhgorod',2.00,3.00,2.00,366),('UA','Europe/Zaporozhye',2.00,3.00,2.00,367),('UG','Africa/Kampala',3.00,3.00,3.00,368),('UM','Pacific/Johnston',-10.00,-10.00,-10.00,369),('UM','Pacific/Midway',-11.00,-11.00,-11.00,370),('UM','Pacific/Wake',12.00,12.00,12.00,371),('US','America/Adak',-10.00,-9.00,-10.00,372),('US','America/Anchorage',-9.00,-8.00,-9.00,373),('US','America/Boise',-7.00,-6.00,-7.00,374),('US','America/Chicago',-6.00,-5.00,-6.00,375),('US','America/Denver',-7.00,-6.00,-7.00,376),('US','America/Detroit',-5.00,-4.00,-5.00,377),('US','America/Indiana/Indianapolis',-5.00,-4.00,-5.00,378),('US','America/Indiana/Knox',-6.00,-5.00,-6.00,379),('US','America/Indiana/Marengo',-5.00,-4.00,-5.00,380),('US','America/Indiana/Petersburg',-5.00,-4.00,-5.00,381),('US','America/Indiana/Tell_City',-6.00,-5.00,-6.00,382),('US','America/Indiana/Vevay',-5.00,-4.00,-5.00,383),('US','America/Indiana/Vincennes',-5.00,-4.00,-5.00,384),('US','America/Indiana/Winamac',-5.00,-4.00,-5.00,385),('US','America/Juneau',-9.00,-8.00,-9.00,386),('US','America/Kentucky/Louisville',-5.00,-4.00,-5.00,387),('US','America/Kentucky/Monticello',-5.00,-4.00,-5.00,388),('US','America/Los_Angeles',-8.00,-7.00,-8.00,389),('US','America/Menominee',-6.00,-5.00,-6.00,390),('US','America/Metlakatla',-8.00,-8.00,-8.00,391),('US','America/New_York',-5.00,-4.00,-5.00,392),('US','America/Nome',-9.00,-8.00,-9.00,393),('US','America/North_Dakota/Beulah',-6.00,-5.00,-6.00,394),('US','America/North_Dakota/Center',-6.00,-5.00,-6.00,395),('US','America/North_Dakota/New_Salem',-6.00,-5.00,-6.00,396),('US','America/Phoenix',-7.00,-7.00,-7.00,397),('US','America/Shiprock',-7.00,-6.00,-7.00,398),('US','America/Sitka',-9.00,-8.00,-9.00,399),('US','America/Yakutat',-9.00,-8.00,-9.00,400),('US','Pacific/Honolulu',-10.00,-10.00,-10.00,401),('UY','America/Montevideo',-2.00,-3.00,-3.00,402),('UZ','Asia/Samarkand',5.00,5.00,5.00,403),('UZ','Asia/Tashkent',5.00,5.00,5.00,404),('VA','Europe/Vatican',1.00,2.00,1.00,405),('VC','America/St_Vincent',-4.00,-4.00,-4.00,406),('VE','America/Caracas',-4.50,-4.50,-4.50,407),('VG','America/Tortola',-4.00,-4.00,-4.00,408),('VI','America/St_Thomas',-4.00,-4.00,-4.00,409),('VN','Asia/Ho_Chi_Minh',7.00,7.00,7.00,410),('VU','Pacific/Efate',11.00,11.00,11.00,411),('WF','Pacific/Wallis',12.00,12.00,12.00,412),('WS','Pacific/Apia',14.00,13.00,13.00,413),('YE','Asia/Aden',3.00,3.00,3.00,414),('YT','Indian/Mayotte',3.00,3.00,3.00,415),('ZA','Africa/Johannesburg',2.00,2.00,2.00,416),('ZM','Africa/Lusaka',2.00,2.00,2.00,417),('ZW','Africa/Harare',2.00,2.00,2.00,418);
/*!40000 ALTER TABLE `timezone` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tsigkeys`
--

DROP TABLE IF EXISTS `tsigkeys`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tsigkeys` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `algorithm` varchar(50) DEFAULT NULL,
  `secret` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `namealgoindex` (`name`,`algorithm`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tsigkeys`
--

LOCK TABLES `tsigkeys` WRITE;
/*!40000 ALTER TABLE `tsigkeys` DISABLE KEYS */;
/*!40000 ALTER TABLE `tsigkeys` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_profile`
--

DROP TABLE IF EXISTS `users_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users_profile` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `avatar` varchar(100) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `bio` longtext NOT NULL DEFAULT _utf8mb3'2024-09-28 14:32:46.817292+00:00',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `users_profile_user_id_2112e78d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_profile`
--

LOCK TABLES `users_profile` WRITE;
/*!40000 ALTER TABLE `users_profile` DISABLE KEYS */;
INSERT INTO `users_profile` VALUES (1,'default.jpg',1,'');
/*!40000 ALTER TABLE `users_profile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-26 15:22:08
