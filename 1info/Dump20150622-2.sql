-- MySQL dump 10.13  Distrib 5.6.23, for Win32 (x86)
--
-- Host: localhost    Database: fin_analyzer
-- ------------------------------------------------------
-- Server version	5.6.25-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `id` int(11) NOT NULL,
  `ticker` varchar(15) NOT NULL,
  `name` varchar(65) NOT NULL,
  `index_id` int(11) NOT NULL,
  `exchange_id` int(11) DEFAULT NULL,
  `fb_page` varchar(45) NOT NULL,
  `tw_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ticker_UNIQUE` (`ticker`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'MMM','3M',1,NULL,'3M',NULL),(2,'ANF','Abercrombie & Fitch',1,NULL,'abercrombie',NULL),(3,'ADBE','Adobe Systems',1,NULL,'110534035634837',NULL),(4,'AMD','Advanced Micro Devices',1,NULL,'AMD',NULL),(5,'AET','Aetna',1,NULL,'aetna',NULL),(6,'AFL','AFLAC',1,NULL,'Aflac',NULL),(7,'A','Agilent Technologies',1,NULL,'Agilent.Tech',NULL),(8,'AKAM','Akamai Technologies',1,NULL,'AkamaiTechnologies',NULL),(9,'AA','Alcoa',1,NULL,'alcoa',NULL),(10,'ALL','Allstate',1,NULL,'Allstate',NULL),(11,'ALTR','Altera',1,NULL,'alteracorp',NULL),(12,'AMZN','Amazon.com',1,NULL,'Amazon',NULL),(13,'AEE','Ameren',1,NULL,'AmerenCorp',NULL),(14,'AEP','American Electric Power',1,NULL,'americanelectricpower',NULL),(15,'AXP','American Express',1,NULL,'AmericanExpress',NULL),(16,'AIG','American International Group',1,NULL,'AIGInsurance',NULL),(17,'ASD','American Standard',1,NULL,'AmericanStandardPlumbing',NULL),(18,'AMP','Ameriprise Financial',1,NULL,'Ameriprise',NULL),(19,'APC','Anadarko Petroleum',1,NULL,'AnadarkoPetroleumCorporation',NULL),(20,'BUD','Anheuser-Busch',1,NULL,'AnheuserBusch',NULL),(21,'T','AT&T',1,NULL,'ATT',NULL),(22,'ADSK','Autodesk',1,NULL,'autodesk',NULL),(23,'ADP','Automatic Data Processing',1,NULL,'AutomaticDataProcessing',NULL),(24,'AN','AutoNation',1,NULL,'autonation',NULL),(25,'AVY','Avery Dennison',1,NULL,'AveryDennisonCorporation',NULL),(26,'AVP','Avon Products',1,NULL,'Avon',NULL),(27,'BAC','Bank of America',1,NULL,'BankofAmerica',NULL),(28,'BAX','Baxter International',1,NULL,'102035033580',NULL),(29,'BBT','BB&T',1,NULL,'BBTBank',NULL),(30,'BBBY','Bed Bath & Beyond',1,NULL,'BedBathAndBeyond',NULL),(31,'BIG','Big Lots',1,NULL,'BigLots',NULL),(32,'BDK','Black & Decker',1,NULL,'BlackAndDecker',NULL),(33,'BMC','BMC Software',1,NULL,'bmcsoftware',NULL),(34,'BC','Brunswick',1,NULL,'GlobalNB',NULL),(35,'CPB','Campbell Soup',1,NULL,'campbells',NULL),(36,'COF','Capital One Financial',1,NULL,'capitalone',NULL),(37,'CCL','Carnival',1,NULL,'Carnival',NULL),(38,'CAT','Caterpillar',1,NULL,'caterpillar',NULL),(39,'CBG','CB Richard Ellis Group',1,NULL,'cbre',NULL),(40,'CBS','CBS',1,NULL,'CBS',NULL),(41,'CNP','CenterPoint Energy',1,NULL,'CenterPointEnergy',NULL),(42,'CTX','Centex',1,NULL,'Centexhomes',NULL),(43,'CTL','CenturyTel',1,NULL,'CenturyLink',NULL),(44,'CI','CIGNA',1,NULL,'CIGNA',NULL),(45,'CINF','Cincinnati Financial',1,NULL,'CincinnatiInsurance',NULL),(46,'CTAS','Cintas',1,NULL,'Cintas',NULL),(47,'CSCO','Cisco Systems',1,NULL,'Cisco',NULL),(48,'CIT','CIT Group',1,NULL,'CITGroup',NULL),(49,'C','Citigroup',1,NULL,'citi',NULL),(50,'CTXS','Citrix Systems',1,NULL,'Citrix',NULL),(51,'CLX','Clorox',1,NULL,'Clorox',NULL),(52,'CME','CME Group',1,NULL,'CMEGroup',NULL),(53,'KO','Coca-Cola',1,NULL,'cocacola',NULL),(54,'CTSH','Cognizant Technology Solutions',1,NULL,'Cognizant',NULL),(55,'CMCSA','Comcast',1,NULL,'xfinity',NULL),(56,'CPWR','Compuware',1,NULL,'compuware',NULL),(57,'CAG','ConAgra Foods',1,NULL,'ConAgraFoods',NULL),(58,'COP','ConocoPhillips',1,NULL,'conocophillips',NULL),(59,'CNX','CONSOL Energy',1,NULL,'consolenergy',NULL),(60,'STZ','Constellation Energy Group',1,NULL,'ConstellationEnergy',NULL),(61,'CVG','Convergys',1,NULL,'convergysglobal',NULL),(62,'GLW','Corning',1,NULL,'CorningGorillaGlass',NULL),(63,'COST','Costco',1,NULL,'Costco',NULL),(64,'CSX','CSX',1,NULL,'OfficialCSX',NULL),(65,'CMI','Cummins',1,NULL,'CUMMINS',NULL),(66,'DF','Dean Foods',1,NULL,'DeanFoods',NULL),(67,'DELL','Dell',1,NULL,'Dell',NULL),(68,'DDR','Developers Diversified Realty',1,NULL,'ddrcorp',NULL),(69,'DDS','Dillard',1,NULL,'Dillards',NULL),(70,'DTV','DIRECTV Group',1,NULL,'directv',NULL),(71,'DJ','Dow Jones & Company',1,NULL,'dowjones',NULL),(72,'DTE','DTE Energy',1,NULL,'dteenergy',NULL),(73,'DUK','Duke Energy',1,NULL,'duke.energy',NULL),(74,'DYN','Dynegy',1,NULL,'DynegyOhio',NULL),(75,'ETFC','E TRADE Financial',1,NULL,'ETRADE',NULL),(76,'SSP','E.W. Scripps',1,NULL,'EWScrippsCo',NULL),(77,'EMN','Eastman Chemical',1,NULL,'EastmanChemicalCo',NULL),(78,'EBAY','eBay',1,NULL,'eBay',NULL),(79,'EP','El Paso',1,NULL,'eptimes',NULL),(80,'ERTS','Electronic Arts',1,NULL,'EA',NULL),(81,'EMC','EMC',1,NULL,'emccorp',NULL),(82,'EMR','Emerson Electric',1,NULL,'EmersonCorporate',NULL),(83,'ETR','Entergy',1,NULL,'entergy',NULL),(84,'EFX','Equifax',1,NULL,'Equifax',NULL),(85,'EL','Estee Lauder',1,NULL,'EsteeLauder',NULL),(86,'EXPE','Expedia',1,NULL,'expedia',NULL),(87,'ESRX','Express Scripts',1,NULL,'ExpressScripts',NULL),(88,'FDO','Family Dollar Stores',1,NULL,'familydollar',NULL),(89,'FNM','Fannie Mae',1,NULL,'fanniemae',NULL),(90,'FDX','FedEx',1,NULL,'FedEx',NULL),(91,'FITB','Fifth Third Bancorp',1,NULL,'FifthThirdBank',NULL),(92,'F','Ford Motor',1,NULL,'ford',NULL),(93,'BEN','Franklin Resources',1,NULL,'franklintempleton',NULL),(94,'GE','General Electric',1,NULL,'GE',NULL),(95,'GM','General Motors',1,NULL,'generalmotors',NULL),(96,'GGP','Genl Growth Properties',1,NULL,'GeneralGrowthProperties',NULL),(97,'GNW','Genworth Financial',1,NULL,'Genworth',NULL),(98,'GT','Goodyear Tire & Rubber',1,NULL,'Goodyear',NULL),(99,'GOOG','Google',1,NULL,'Google',NULL),(100,'HRB','H&R Block',1,NULL,'hrblock',NULL),(101,'HAL','Halliburton',1,NULL,'halliburton',NULL),(102,'HOG','Harley-Davidson',1,NULL,'harley-davidson',NULL),(103,'HET','Harrah\'s Entertainment',1,NULL,'HarrahsVegas',NULL),(104,'HAS','Hasbro',1,NULL,'hasbrogaming',NULL),(105,'HSY','Hershey',1,NULL,'HERSHEYS',NULL),(106,'HPQ','Hewlett-Packard',1,NULL,'HP',NULL),(107,'HD','Home Depot',1,NULL,'homedepot',NULL),(108,'HON','Honeywell',1,NULL,'honeywellhome',NULL),(109,'HUM','Humana',1,NULL,'Humana',NULL),(110,'SCHW','Charles Schwab',1,NULL,'CharlesSchwab',NULL),(111,'CHK','Chesapeake Energy',1,NULL,'Chesapeake',NULL),(112,'CVX','Chevron',1,NULL,'Chevron',NULL),(113,'IBM','IBM',1,NULL,'IBM',NULL),(114,'IR','Ingersoll-Rand',1,NULL,'ingersollrand',NULL),(115,'INTC','Intel',1,NULL,'Intel',NULL),(116,'INTU','Intuit',1,NULL,'intuit',NULL),(117,'JCP','J.C. Penney',1,NULL,'jcp',NULL),(118,'JNJ','Johnson & Johnson',1,NULL,'jnj',NULL),(119,'JCI','Johnson Controls',1,NULL,'JohnsonControls',NULL),(120,'JPM','JPMorgan Chase',1,NULL,'jpmorgancommunity',NULL),(121,'JNPR','Juniper Networks',1,NULL,'JuniperNetworks',NULL),(122,'KBH','KB Home',1,NULL,'KBHome',NULL),(123,'KMB','Kimberly-Clark',1,NULL,'KimberlyClarkCorp',NULL),(124,'KSS','Kohl\'s',1,NULL,'kohls',NULL),(125,'KFT','Kraft Foods',1,NULL,'KraftFoods',NULL),(126,'KR','Kroger',1,NULL,'Kroger',NULL),(127,'LEN','Lennar',1,NULL,'Lennar',NULL),(128,'LNC','Lincoln National',1,NULL,'lincolnfinancialgroup',NULL),(129,'LLTC','Linear Technology',1,NULL,'LinearTechnologyCorporation',NULL),(130,'LMT','Lockheed Martin',1,NULL,'lockheedmartin',NULL),(131,'LTR','Loews',1,NULL,'LoewsHotels',NULL),(132,'LOW','Lowe\'s Companies',1,NULL,'lowes',NULL),(133,'M','Macy\'s',1,NULL,'Macys',NULL),(134,'MAR','Marriott International',1,NULL,'marriottinternational',NULL),(135,'MAT','Mattel',1,NULL,'Mattel',NULL),(136,'MCD','McDonald\'s',1,NULL,'McDonalds',NULL),(137,'MHP','McGraw-Hill',1,NULL,'mcgrawhillprofessional.business',NULL),(138,'MCK','McKesson',1,NULL,'McKessonCorporation',NULL),(139,'MDT','Medtronic',1,NULL,'Medtronic',NULL),(140,'MRK','Merck',1,NULL,'MerckBeWell',NULL),(141,'MET','MetLife',1,NULL,'metlife',NULL),(142,'MCHP','Microchip Technology',1,NULL,'microchiptechnology',NULL),(143,'MSFT','Microsoft',1,NULL,'Microsoft',NULL),(144,'MON','Monsanto',1,NULL,'MonsantoCo',NULL),(145,'MOT','Motorola',1,NULL,'Motorola',NULL),(146,'NOV','National Oilwell Varco',1,NULL,'NationalOilwellVarco',NULL),(147,'NTAP','Network Appliance',1,NULL,'NetApp',NULL),(148,'NYT','New York Times',1,NULL,'nytimes',NULL),(149,'NWL','Newell Rubbermaid',1,NULL,'NEWELLRUBBERMAID',NULL),(150,'NKE','NIKE',1,NULL,'nike',NULL),(151,'JWN','Nordstrom',1,NULL,'Nordstrom',NULL),(152,'NOC','Northrop Grumman',1,NULL,'NorthropGrumman',NULL),(153,'NVDA','NVIDIA',1,NULL,'NVIDIA',NULL),(154,'NYX','NYSE Euronext',1,NULL,'NYSE',NULL),(155,'ODP','Office Depot',1,NULL,'OfficeDepot',NULL),(156,'ORCL','Oracle',1,NULL,'Oracle',NULL),(157,'PAYX','Paychex',1,NULL,'Paychex',NULL),(158,'PEP','PepsiCo',1,NULL,'pepsi',NULL),(159,'PKI','PerkinElmer',1,NULL,'PerkinElmer',NULL),(160,'PFE','Pfizer',1,NULL,'Pfizer',NULL),(161,'PBI','Pitney Bowes',1,NULL,'PitneyBowes',NULL),(162,'RL','Polo Ralph Lauren',1,NULL,'RalphLauren',NULL),(163,'PPG','PPG Industries',1,NULL,'ppgindustries',NULL),(164,'PFG','Principal Financial Group',1,NULL,'PrincipalFinancial',NULL),(165,'PG','Procter & Gamble',1,NULL,'PG',NULL),(166,'PGR','Progressive',1,NULL,'progressive',NULL),(167,'PRU','Prudential Financial',1,NULL,'PrudentialBYC',NULL),(168,'PEG','Public Service Enterprise Group',1,NULL,'PSEG',NULL),(169,'PSA','Public Storage',1,NULL,'PublicStorage',NULL),(170,'PHM','Pulte Homes',1,NULL,'PulteGroup',NULL),(171,'QCOM','QUALCOMM',1,NULL,'Qualcomm',NULL),(172,'DGX','Quest Diagnostics',1,NULL,'questdiagnostics',NULL),(173,'RSH','RadioShack',1,NULL,'RadioShack',NULL),(174,'RTN','Raytheon',1,NULL,'Raytheon',NULL),(175,'RF','Regions Financial',1,NULL,'RegionsBank',NULL),(176,'ROK','Rockwell Automation',1,NULL,'ROKAutomation',NULL),(177,'R','Ryder System',1,NULL,'RyderSystemInc',NULL),(178,'SAF','SAFECO',1,NULL,'SafecoInsurance',NULL),(179,'SWY','Safeway',1,NULL,'Safeway',NULL),(180,'SNDK','SanDisk',1,NULL,'sandisk',NULL),(181,'SLE','Sara Lee',1,NULL,'saraleedeli',NULL),(182,'SEE','Sealed Air',1,NULL,'287944878104',NULL),(183,'SHLD','Sears Holdings',1,NULL,'sears',NULL),(184,'SHW','Sherwin-Williams',1,NULL,'SherwinWilliamsforYourHome',NULL),(185,'SNA','Snap-On',1,NULL,'SnaponTools',NULL),(186,'LUV','Southwest Airlines',1,NULL,'Southwest',NULL),(187,'SE','Spectra Energy',1,NULL,'SpectraEnergy',NULL),(188,'S','Sprint Nextel',1,NULL,'sprint',NULL),(189,'SPLS','Staples',1,NULL,'staples',NULL),(190,'SBUX','Starbucks',1,NULL,'Starbucks',NULL),(191,'HOT','Starwood Hotels & Resorts',1,NULL,'starwood',NULL),(192,'JAVAD','Sun Microsystems',1,NULL,'sunmicrosystemsincorporated',NULL),(193,'STI','SunTrust Banks',1,NULL,'suntrust',NULL),(194,'SVU','Supervalu',1,NULL,'SuperValu',NULL),(195,'SYMC','Symantec',1,NULL,'Symantec',NULL),(196,'TROW','T. Rowe Price Group',1,NULL,'troweprice',NULL),(197,'TGT','Target',1,NULL,'target',NULL),(198,'TLAB','Tellabs',1,NULL,'Tellabs',NULL),(199,'TDC','Teradata',1,NULL,'Teradata',NULL),(200,'TEX','Terex',1,NULL,'TerexCorporation',NULL),(201,'TXN','Texas Instruments',1,NULL,'texasinstruments',NULL),(202,'TIF','Tiffany',1,NULL,'Tiffany',NULL),(203,'TWX','Time Warner',1,NULL,'TimeWarner',NULL),(204,'TSN','Tyson Foods',1,NULL,'TysonFoods',NULL),(205,'USB','U.S. Bancorp',1,NULL,'usbank',NULL),(206,'UIS','Unisys',1,NULL,'UnisysCorp',NULL),(207,'UPS','United Parcel Service',1,NULL,'ups',NULL),(208,'VLO','Valero Energy',1,NULL,'valeroenergy',NULL),(209,'VRSN','Verisign',1,NULL,'Verisign',NULL),(210,'VZ','Verizon Communications',1,NULL,'verizon',NULL),(211,'VIA.B','Viacom',1,NULL,'Viacom',NULL),(212,'GWW','W.W. Grainger',1,NULL,'grainger',NULL),(213,'WAG','Walgreen',1,NULL,'Walgreens',NULL),(214,'WMT','Wal-Mart',1,NULL,'walmart',NULL),(215,'DIS','Walt Disney',1,NULL,'DisneyAnimation',NULL),(216,'WMI','Waste Management',1,NULL,'WasteManagement',NULL),(217,'WAT','Waters Corporation',1,NULL,'Waters',NULL),(218,'WFC','Wells Fargo',1,NULL,'wellsfargo',NULL),(219,'WEN','Wendy\'s International',1,NULL,'wendys',NULL),(220,'WU','Western Union',1,NULL,'WesternUnion',NULL),(221,'WHR','Whirlpool',1,NULL,'whirlpoolusa',NULL),(222,'WFMI','Whole Foods Market',1,NULL,'wholefoods',NULL),(223,'WMB','Williams Companies',1,NULL,'WilliamsEnergyCo',NULL),(224,'WIN','Windstream',1,NULL,'windstreamconnects',NULL),(225,'WYE','Wyeth',1,NULL,'WyethNutrition',NULL),(226,'WYN','Wyndham Worldwide',1,NULL,'WyndhamWorldwide',NULL),(227,'XEL','Xcel Energy',1,NULL,'xcelenergy',NULL),(228,'XRX','Xerox',1,NULL,'xerox',NULL),(229,'YHOO','Yahoo',1,NULL,'yahoofinance',NULL),(230,'YUM','Yum! Brands',1,NULL,'yumbrands',NULL);
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fb_comment`
--

DROP TABLE IF EXISTS `fb_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fb_comment` (
  `id` varchar(50) NOT NULL,
  `fb_post_id` varchar(50) NOT NULL,
  `company_id` int(11) NOT NULL,
  `created_timestamp` int(11) unsigned NOT NULL,
  `text` text NOT NULL,
  `fb_author_id` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fb_comment`
--

LOCK TABLES `fb_comment` WRITE;
/*!40000 ALTER TABLE `fb_comment` DISABLE KEYS */;
INSERT INTO `fb_comment` VALUES ('10152885483571850_10152885584596850','22707976849_10152885483571850',115,1434673551,'אינטל צריכה לפתח מערכת רזה של שבבים לטלוויזיות חכמות שיתמקדו ברוולוציה וחיסכון בחשמל ומהירות עבור משימות פשוטות ביחד עם ארכיטקטורת 64 ביט למשחקים בדומה לאייפון.','859871327383653'),('10152885483571850_10152886365681850','22707976849_10152885483571850',115,1434702932,'wow','850664708359855'),('10152885483571850_10152886403801850','22707976849_10152885483571850',115,1434705926,'Wow! Hey I have a scen :)','1461696667476922'),('10152885483571850_10152886405751850','22707976849_10152885483571850',115,1434706081,'Aswome...','1594655294124333'),('10152885483571850_10152886749566850','22707976849_10152885483571850',115,1434722704,'(y)','943469955684619'),('10152885483571850_10152886955451850','22707976849_10152885483571850',115,1434731017,'Aswome','1630138797203222'),('10152885483571850_10152887412906850','22707976849_10152885483571850',115,1434747244,'كل سنه وانت طيب يا عم احمد','1459095901071814'),('10152885483571850_10152888344956850','22707976849_10152885483571850',115,1434784988,'amazing','102895093387342'),('10152885483571850_10152888357011850','22707976849_10152885483571850',115,1434785671,'يا إبن الحلال قولتلك قبل كده إحلم علي أدك','1424869317838830'),('10152885483571850_10152888622396850','22707976849_10152885483571850',115,1434796543,'Internet of things.','852350184855839'),('10152885483571850_10152889266711850','22707976849_10152885483571850',115,1434822171,'I like it.','363982860467701'),('10152885483571850_10152890752256850','22707976849_10152885483571850',115,1434869375,'Abdul asnfap','1458295251152968'),('10152885483571850_10152891253376850','22707976849_10152885483571850',115,1434893166,'بووق','1597918813809887'),('10152885483571850_10152891420521850','22707976849_10152885483571850',115,1434898583,'Bodo amat. Ngak ngreken blass aku.','1662312870653426'),('10152885483571850_10152893767851850','22707976849_10152885483571850',115,1434984552,'gr8 work....','844119522341383'),('10152885483571850_10152893777166850','22707976849_10152885483571850',115,1434984941,'Mna jempol indonesia....','499327890225753'),('10152886660191850_10152887693556850','22707976849_10152886660191850',115,1434758505,'Creative !!!','10203623979074463'),('10152886660191850_10152889422011850','22707976849_10152886660191850',115,1434827114,'en smukt pc til hans','10207576296111125'),('10152886660191850_10152889637131850','22707976849_10152886660191850',115,1434833507,'Killing Intel, I, I just had to resign from the Apple Board.\nArthur Rock','321034581258800'),('10152886660191850_10152890082806850','22707976849_10152886660191850',115,1434848543,'I wanna see a solution to offer internet to the whole world for free','829911310421310'),('10152886660191850_10152892055976850','22707976849_10152886660191850',115,1434920500,'yh er amrzimg lc dc lap top','1462007394096964'),('10152891426386850_10152891451151850','22707976849_10152891426386850',115,1434899799,'Thank you @intel for consistently focusing on early education!!','10154178568533561'),('10152891426386850_10152891508851850','22707976849_10152891426386850',115,1434901827,'STEM stands for Science, Technology, Engineering, Mathematics. They have a similar program at the college I work at.','648279618650444'),('10152891426386850_10152891621571850','22707976849_10152891426386850',115,1434905512,'kfc bbc','1449474682039293'),('10152891426386850_10152891633906850','22707976849_10152891426386850',115,1434905988,'What a wonderful company!','10205469913120064'),('10152891426386850_10152891652771850','22707976849_10152891426386850',115,1434906763,'Waoo its good work. Well done','653337594799228'),('10152891426386850_10152891780626850','22707976849_10152891426386850',115,1434911071,'Wow.......','1669976829900434'),('10152891426386850_10152891855991850','22707976849_10152891426386850',115,1434913853,'I taught myself about computers.','1597404667192734'),('10152891426386850_10152892584731850','22707976849_10152891426386850',115,1434940158,'Wow','1487658691526144'),('10152893623051850_10152893646371850','22707976849_10152893623051850',115,1434979022,'Dear Intel, please pimp my render farm with some  E5-Xeons. These Q8200-CPUs have been on for at least 6-7 years now and they render 24/7. I need power and swiftness to render high quality renders, https://www.dropbox.com/s/462tltf28thzct9/photo%2022.6.2015%2016.09.45.jpg?dl=0','10153392886312432'),('10152893623051850_10152893724996850','22707976849_10152893623051850',115,1434982639,'Why intel hd graphics doesn\'t matter with Nvidia video cards :/','627142650755996'),('10152893623051850_10152893974746850','22707976849_10152893623051850',115,1434991550,'Intel is Xeon for gaming experience  ? :D','478614098964318');
/*!40000 ALTER TABLE `fb_comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fb_comment_history`
--

DROP TABLE IF EXISTS `fb_comment_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fb_comment_history` (
  `fb_comment_id` varchar(50) NOT NULL,
  `company_id` int(11) NOT NULL,
  `download_timestamp` int(11) unsigned NOT NULL,
  `likes_count` int(11) unsigned NOT NULL,
  PRIMARY KEY (`fb_comment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fb_comment_history`
--

LOCK TABLES `fb_comment_history` WRITE;
/*!40000 ALTER TABLE `fb_comment_history` DISABLE KEYS */;
INSERT INTO `fb_comment_history` VALUES ('10152885483571850_10152885584596850',115,1435000023,1),('10152885483571850_10152886365681850',115,1435000023,2),('10152885483571850_10152886403801850',115,1435000023,0),('10152885483571850_10152886405751850',115,1435000023,0),('10152885483571850_10152886749566850',115,1435000023,0),('10152885483571850_10152886955451850',115,1435000023,0),('10152885483571850_10152887412906850',115,1435000023,0),('10152885483571850_10152888344956850',115,1435000023,0),('10152885483571850_10152888357011850',115,1435000023,1),('10152885483571850_10152888622396850',115,1435000023,0),('10152885483571850_10152889266711850',115,1435000023,0),('10152885483571850_10152890752256850',115,1435000023,1),('10152885483571850_10152891253376850',115,1435000023,0),('10152885483571850_10152891420521850',115,1435000023,0),('10152885483571850_10152893767851850',115,1435000023,0),('10152885483571850_10152893777166850',115,1435000023,1),('10152886660191850_10152887693556850',115,1435000023,4),('10152886660191850_10152889422011850',115,1435000023,0),('10152886660191850_10152889637131850',115,1435000023,0),('10152886660191850_10152890082806850',115,1435000023,0),('10152886660191850_10152892055976850',115,1435000023,0),('10152891426386850_10152891451151850',115,1435000023,2),('10152891426386850_10152891508851850',115,1435000023,5),('10152891426386850_10152891621571850',115,1435000023,0),('10152891426386850_10152891633906850',115,1435000023,0),('10152891426386850_10152891652771850',115,1435000023,0),('10152891426386850_10152891780626850',115,1435000023,0),('10152891426386850_10152891855991850',115,1435000023,0),('10152891426386850_10152892584731850',115,1435000023,1),('10152893623051850_10152893646371850',115,1435000023,2),('10152893623051850_10152893724996850',115,1435000023,0),('10152893623051850_10152893974746850',115,1435000023,0);
/*!40000 ALTER TABLE `fb_comment_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fb_post`
--

DROP TABLE IF EXISTS `fb_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fb_post` (
  `id` varchar(50) NOT NULL,
  `company_id` int(11) NOT NULL,
  `created_timestamp` int(11) unsigned NOT NULL,
  `text` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fb_post`
--

LOCK TABLES `fb_post` WRITE;
/*!40000 ALTER TABLE `fb_post` DISABLE KEYS */;
INSERT INTO `fb_post` VALUES ('22707976849_10152884896636850',115,1434650411,'Self-driving cars, Skype, and the Mars Rover. At the 1964 World’s Fair, sci-fi icon Isaac Asimov made some eerily accurate predictions for 2014. #RealScience'),('22707976849_10152885483571850',115,1434669602,'What do facial recognition security, audio biometrics, and motion-controlled cuisine have in common? See how the IoT is empowering people and cities around the world. http://intel.ly/1JYrWNz'),('22707976849_10152886660191850',115,1434718802,'What sorts of beautiful tech do you want to see on our Instagram page next? http://intel.ly/1dBae4J'),('22707976849_10152891426386850',115,1434898803,'We couldn’t agree more, which is why we’re donating $5 million to Oakland Public School STEM programs in 2015.'),('22707976849_10152893623051850',115,1434978005,'Check out monster gaming rigs on our Instagram account this month. Then submit your own tricked-out DIY machine using #ExpertMode. http://intel.ly/1Bsemzf');
/*!40000 ALTER TABLE `fb_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fb_post_history`
--

DROP TABLE IF EXISTS `fb_post_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fb_post_history` (
  `post_id` varchar(50) NOT NULL,
  `company_id` int(11) NOT NULL,
  `download_timestamp` int(11) unsigned NOT NULL,
  `likes_count` int(11) unsigned NOT NULL,
  `shares_count` int(11) unsigned NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fb_post_history`
--

LOCK TABLES `fb_post_history` WRITE;
/*!40000 ALTER TABLE `fb_post_history` DISABLE KEYS */;
INSERT INTO `fb_post_history` VALUES ('22707976849_10152884896636850',115,1435000023,149,96),('22707976849_10152885483571850',115,1435000023,3192,36),('22707976849_10152886660191850',115,1435000023,709,20),('22707976849_10152891426386850',115,1435000023,966,35),('22707976849_10152893623051850',115,1435000023,511,14);
/*!40000 ALTER TABLE `fb_post_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `last_download`
--

DROP TABLE IF EXISTS `last_download`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `last_download` (
  `company_id` int(11) NOT NULL,
  `fb_post_timestamp` int(11) unsigned NOT NULL,
  PRIMARY KEY (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `last_download`
--

LOCK TABLES `last_download` WRITE;
/*!40000 ALTER TABLE `last_download` DISABLE KEYS */;
INSERT INTO `last_download` VALUES (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(8,1),(9,1),(10,1),(11,1),(12,1),(13,1),(14,1),(15,1),(16,1),(17,1),(18,1),(19,1),(20,1),(21,1),(22,1),(23,1),(24,1),(25,1),(26,1),(27,1),(28,1),(29,1),(30,1),(31,1),(32,1),(33,1),(34,1),(35,1),(36,1),(37,1),(38,1),(39,1),(40,1),(41,1),(42,1),(43,1),(44,1),(45,1),(46,1),(47,1),(48,1),(49,1),(50,1),(51,1),(52,1),(53,1),(54,1),(55,1),(56,1),(57,1),(58,1),(59,1),(60,1),(61,1),(62,1),(63,1),(64,1),(65,1),(66,1),(67,1),(68,1),(69,1),(70,1),(71,1),(72,1),(73,1),(74,1),(75,1),(76,1),(77,1),(78,1),(79,1),(80,1),(81,1),(82,1),(83,1),(84,1),(85,1),(86,1),(87,1),(88,1),(89,1),(90,1),(91,1),(92,1),(93,1),(94,1),(95,1),(96,1),(97,1),(98,1),(99,1),(100,1),(101,1),(102,1),(103,1),(104,1),(105,1),(106,1),(107,1),(108,1),(109,1),(110,1),(111,1),(112,1),(113,1),(114,1),(115,1434978005),(116,1),(117,1),(118,1),(119,1),(120,1),(121,1),(122,1),(123,1),(124,1),(125,1),(126,1),(127,1),(128,1),(129,1),(130,1),(131,1),(132,1),(133,1),(134,1),(135,1),(136,1),(137,1),(138,1),(139,1),(140,1),(141,1),(142,1),(143,1),(144,1),(145,1),(146,1),(147,1),(148,1),(149,1),(150,1),(151,1),(152,1),(153,1),(154,1),(155,1),(156,1),(157,1),(158,1),(159,1),(160,1),(161,1),(162,1),(163,1),(164,1),(165,1),(166,1),(167,1),(168,1),(169,1),(170,1),(171,1),(172,1),(173,1),(174,1),(175,1),(176,1),(177,1),(178,1),(179,1),(180,1),(181,1),(182,1),(183,1),(184,1),(185,1),(186,1),(187,1),(188,1),(189,1),(190,1),(191,1),(192,1),(193,1),(194,1),(195,1),(196,1),(197,1),(198,1),(199,1),(200,1),(201,1),(202,1),(203,1),(204,1),(205,1),(206,1),(207,1),(208,1),(209,1),(210,1),(211,1),(212,1),(213,1),(214,1),(215,1),(216,1),(217,1),(218,1),(219,1),(220,1),(221,1),(222,1),(223,1),(224,1),(225,1),(226,1),(227,1),(228,1),(229,1),(230,1);
/*!40000 ALTER TABLE `last_download` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-06-22 21:31:16
