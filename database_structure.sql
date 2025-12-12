-- MySQL dump 10.11
--
-- Host: localhost    Database: 
-- ------------------------------------------------------
-- Server version	5.0.67-community-nt

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
-- Current Database: `etm_one`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `etm_one` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `etm_one`;

--
-- Table structure for table `advisorsalestarget`
--

DROP TABLE IF EXISTS `advisorsalestarget`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `advisorsalestarget` (
  `TargetGuid` char(36) NOT NULL,
  `AdvisorGuid` char(36) default NULL,
  `CreateMonth` varchar(255) default NULL,
  `Amount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `Notes` varchar(500) default NULL,
  PRIMARY KEY  (`TargetGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2498 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `assessrule`
--

DROP TABLE IF EXISTS `assessrule`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `assessrule` (
  `AssessRuleID` int(11) NOT NULL auto_increment,
  `AssessType` int(11) default NULL,
  `AssessItem` varchar(50) default NULL,
  `AssessValue` int(11) default NULL,
  `MaxValue` int(11) default NULL,
  `MinValue` int(11) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`AssessRuleID`)
) ENGINE=MyISAM AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `backupcardpackage`
--

DROP TABLE IF EXISTS `backupcardpackage`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `backupcardpackage` (
  `CardGuid` char(36) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `CurrentClassHours` decimal(10,2) default NULL,
  `Notes` varchar(255) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `bosssync`
--

DROP TABLE IF EXISTS `bosssync`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `bosssync` (
  `ID` int(11) NOT NULL auto_increment,
  `ProcedureName` varchar(255) default NULL,
  `IsMsg` bit(1) default NULL,
  `IsEmail` bit(1) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=36;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `budgetconfig`
--

DROP TABLE IF EXISTS `budgetconfig`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `budgetconfig` (
  `BudgetGuid` char(36) NOT NULL,
  `InOutType` int(11) default NULL,
  `InOutTypeGuid` char(36) default NULL,
  `Amount` decimal(10,2) default NULL,
  `BudgetDate` varchar(50) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`BudgetGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=141;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `calendar`
--

DROP TABLE IF EXISTS `calendar`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `calendar` (
  `CalendarGuid` char(36) NOT NULL,
  `ManagerGuid` char(36) NOT NULL COMMENT '员工Guid',
  `CalendarContent` text,
  `CalendarDate` datetime default NULL COMMENT '日期',
  `StartDate` datetime default NULL,
  `EndDate` datetime default NULL,
  `IsAllDay` bit(1) default NULL,
  `IsUseEndDate` bit(1) default NULL,
  `IsRemind` bit(1) default NULL,
  `RemindTime` datetime default NULL,
  `CancelRemind` bit(1) default NULL,
  `IsRepeat` bit(1) default NULL,
  `RepeatCycleTime` int(11) default NULL,
  `CancelCycleRemind` bit(1) default NULL,
  `Notes` varchar(550) default NULL,
  PRIMARY KEY  (`CalendarGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `callinfo`
--

DROP TABLE IF EXISTS `callinfo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `callinfo` (
  `Guid` varchar(36) NOT NULL,
  `StartDate` datetime default NULL,
  `EndDate` datetime default NULL,
  `TimeLength` int(11) default NULL,
  `CallType` int(11) default NULL,
  `PhoneNumber` varchar(50) default NULL,
  `ManagerGuid` varchar(36) default NULL,
  `AudioFileName` varchar(150) default NULL,
  `AudioFileFullName` varchar(250) default NULL,
  `Notes` varchar(550) default NULL,
  PRIMARY KEY  (`Guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `card`
--

DROP TABLE IF EXISTS `card`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `card` (
  `CardGuid` char(36) NOT NULL COMMENT '会员卡Guid',
  `CardNo` varchar(50) default NULL COMMENT '会员卡号',
  `CardTypeGuid` char(36) default NULL COMMENT '会员卡类型',
  `LeaveDays` int(11) default NULL COMMENT '可用请假次数',
  `EffectiveDuration` int(11) default NULL COMMENT '有效期',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `CreatorGuid` char(36) default NULL COMMENT '创建人',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `Notes` varchar(200) default NULL,
  `MainCardGuid` char(36) default NULL COMMENT '如果是附属卡，表示主卡Guid',
  `UseType` int(11) default NULL COMMENT '附属卡使用方式：0共享，1独享，3主卡',
  `Amount` decimal(18,2) default NULL COMMENT '卡的现金',
  `StopDate` datetime default NULL,
  PRIMARY KEY  (`CardGuid`),
  KEY `uk_maincardguid` (`MainCardGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `wxtemp_carddostatus_update` AFTER UPDATE ON `card` FOR EACH ROW BEGIN     DECLARE P_MemberGuid CHAR(36);   DECLARE P_WXOpenID   VARCHAR(100);   SET P_MemberGuid = '00000000-0000-0000-0000-000000000000';   SET P_WXOpenID = '';    IF new.DoStatus <> old.DoStatus THEN   SELECT a.MemberGuid      , b.WXOpenID INTO   P_MemberGuid, P_WXOpenID FROM   membercard a inner join member b on a.MemberGuid=b.MemberGuid WHERE   a.cardguid = new.CardGuid;   IF P_MemberGuid <> '00000000-0000-0000-0000-000000000000' && P_WXOpenID <> '' THEN     CALL P_WXTemp_Classhour(P_MemberGuid, P_WXOpenID, 3);   END IF;     INSERT INTO worklog(WorkLogGuid,LogDate,Title,LogContent,CreateTime,CreatorGuid) VALUES (uuid(), now(), P_MemberGuid, P_WXOpenID, now(), uuid()); END IF;  END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `cardflow`
--

DROP TABLE IF EXISTS `cardflow`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardflow` (
  `CardFlowGuid` char(36) NOT NULL,
  `FlowType` varchar(50) default NULL,
  `RelatedItemGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `CardGuid` char(36) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `BeforeClassHours` decimal(18,2) default NULL,
  `ChangeClassHours` decimal(18,2) default NULL,
  `Notes` varchar(200) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `realtime` datetime default NULL,
  `ReduceBuyClassHours` decimal(6,2) NOT NULL default '0.00',
  `ReduceGiftClassHours` decimal(6,2) NOT NULL default '0.00',
  `Cost` decimal(10,2) NOT NULL default '0.00',
  `AfterClassHours` decimal(6,2) NOT NULL default '0.00',
  `ContractGuid` char(36) default NULL,
  PRIMARY KEY  (`CardFlowGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardfreeze`
--

DROP TABLE IF EXISTS `cardfreeze`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardfreeze` (
  `CardFreezeGuid` char(36) default NULL,
  `CardGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `MemberOldStatus` int(11) default NULL,
  `MemberNewOldStatus` int(11) default NULL,
  `FreezeStartTime` datetime default NULL,
  `FreezeEndTime` datetime default NULL,
  `ContractGuid` char(36) default NULL,
  `ContractAddDays` int(11) default NULL,
  `DoStatus` int(11) default NULL,
  `FreezeTime` datetime default NULL,
  `FreezeUserName` varchar(255) default NULL,
  `UnFreezeTime` datetime default NULL,
  `UnFreezeUserName` varchar(255) default NULL,
  `Notes` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=228;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardgift`
--

DROP TABLE IF EXISTS `cardgift`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardgift` (
  `CardGiftGuid` char(36) NOT NULL COMMENT '课时变动Guid',
  `CardGuid` char(36) default NULL COMMENT '合同Guid',
  `ContractGuid` char(36) default NULL,
  `ClassHours` decimal(18,2) default NULL,
  `ChangeType` int(11) default NULL COMMENT '变动类型：0 赠送，1 扣减',
  `Cost` decimal(18,0) default NULL COMMENT '费用',
  `Notes` varchar(200) default NULL COMMENT '备注、说明',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `LessonSeriesGuid` char(36) default NULL,
  `ChangeClassHourType` int(11) default '0',
  `IsNewModel` int(11) default '0',
  PRIMARY KEY  (`CardGiftGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardpackage`
--

DROP TABLE IF EXISTS `cardpackage`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardpackage` (
  `CardGuid` char(36) NOT NULL,
  `LessonSeriesGuid` char(36) NOT NULL,
  `CurrentClassHours` decimal(10,2) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`CardGuid`,`LessonSeriesGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=989 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `wxtemp_classhour_insert` AFTER INSERT ON `cardpackage` FOR EACH ROW BEGIN  DECLARE P_MemberGuid CHAR(36);  DECLARE P_WXOpenID   VARCHAR(100);  DECLARE P_Type       INT;  SET P_MemberGuid = '00000000-0000-0000-0000-000000000000';  SET P_WXOpenID = '';  SET P_Type = 1; 
  SELECT c.memberguid       , c.wxopenid  INTO    P_MemberGuid, P_WXOpenID  FROM    cardpackage a  INNER JOIN    membercard b  ON a.cardguid = b.cardguid  INNER JOIN member c  ON b.memberguid = c.memberguid  WHERE    a.CardGuid = new.CardGuid    AND a.LessonSeriesGuid = new.LessonSeriesGuid;  IF P_MemberGuid <> '00000000-0000-0000-0000-000000000000' && P_WXOpenID <> '' THEN    CALL P_WXTemp_Classhour(P_MemberGuid, P_WXOpenID, P_Type);  END IF;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `wxtemp_classhour_update` AFTER UPDATE ON `cardpackage` FOR EACH ROW BEGIN  DECLARE P_MemberGuid CHAR(36);  DECLARE P_WXOpenID   VARCHAR(100);  DECLARE P_Type       INT;  SET P_MemberGuid = '00000000-0000-0000-0000-000000000000';  SET P_WXOpenID = '';  SET P_Type = 3; 
  SELECT c.memberguid       , c.wxopenid  INTO    P_MemberGuid, P_WXOpenID  FROM    cardpackage a  INNER JOIN    membercard b  ON a.cardguid = b.cardguid  INNER JOIN member c  ON b.memberguid = c.memberguid  WHERE    a.CardGuid = old.CardGuid    AND a.LessonSeriesGuid = old.LessonSeriesGuid;  IF P_MemberGuid <> '00000000-0000-0000-0000-000000000000' && P_WXOpenID <> '' THEN    CALL P_WXTemp_Classhour(P_MemberGuid, P_WXOpenID, P_Type);  END IF;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `wxtemp_classhour_delete` AFTER DELETE ON `cardpackage` FOR EACH ROW BEGIN

DECLARE P_MemberGuid CHAR (36) ;
DECLARE P_WXOpenID VARCHAR (100) ;
DECLARE P_Type INT ;
SET P_MemberGuid = '00000000-0000-0000-0000-000000000000' ;
SET P_WXOpenID = '' ;
SET P_Type = 2 ; SELECT
	b.memberguid,
	b.wxopenid INTO P_MemberGuid,
	P_WXOpenID
FROM
	membercard a
INNER JOIN member b ON a.memberguid = b.memberguid
WHERE
	a.CardGuid = old.CardGuid ;
IF P_MemberGuid <> '00000000-0000-0000-0000-000000000000' && P_MemberGuid IS NOT NULL && P_WXOpenID <> '' && P_WXOpenID IS NOT NULL THEN
	CALL P_WXTemp_Classhour (
		P_MemberGuid,
		P_WXOpenID,
		P_Type
	) ;
END
IF ; INSERT INTO worklog (
	WorkLogGuid,
	LogDate,
	Title,
	LogContent,
	CreateTime,
	CreatorGuid
)
VALUES
	(
		uuid(),
		now(),
		P_MemberGuid,
		P_WXOpenID,
		now(),
		uuid()
	) ;
END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `cardpackagetemp`
--

DROP TABLE IF EXISTS `cardpackagetemp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardpackagetemp` (
  `CardGuid` char(36) NOT NULL,
  `ContractGuid` char(36) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `LessonSeriesName` varchar(255) default NULL,
  `ClassHours` decimal(10,2) default NULL,
  `GiftClassHours` decimal(10,2) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=147;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardsignlog`
--

DROP TABLE IF EXISTS `cardsignlog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardsignlog` (
  `LogGuid` char(36) NOT NULL,
  `CardSignRoleGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `CardGuid` char(36) default NULL,
  `LessonSerialGuid` char(36) default NULL,
  `SignTime` datetime default NULL,
  `ReduceType` varchar(50) default NULL,
  `ReduceHours` decimal(10,2) default NULL,
  `ReducePoints` int(11) default NULL,
  `ChangePoints` int(11) default NULL,
  `Notes` text,
  `ContractNos` varchar(255) default NULL,
  `ReduceGiftClassHours` decimal(6,2) default NULL,
  `ReduceBuyClassHours` decimal(6,2) default NULL,
  `TeacherName` varchar(100) default NULL,
  PRIMARY KEY  (`LogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=231;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardsignrole`
--

DROP TABLE IF EXISTS `cardsignrole`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardsignrole` (
  `CardSignRoleGuid` char(36) NOT NULL,
  `CardSignRoleName` varchar(300) default NULL,
  `StartTime` varchar(50) default NULL,
  `EndTime` varchar(50) default NULL,
  `ReduceType` varchar(50) default NULL,
  `ReduceHours` decimal(10,2) default NULL,
  `ReducePoints` int(11) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `SignCount` int(11) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` text,
  `IsGeneralClassHour` int(11) default NULL,
  `GeneralClassHour` decimal(10,2) default NULL,
  `GiftPoint` decimal(10,2) default NULL,
  `SecordLessonSeriesGuid` varchar(36) default NULL COMMENT '备选扣减的课时课程系列标识',
  PRIMARY KEY  (`CardSignRoleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=181;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardtemp`
--

DROP TABLE IF EXISTS `cardtemp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardtemp` (
  `CardGuid` char(36) NOT NULL,
  `CardNo` varchar(255) default NULL,
  `CardTypeGuid` char(36) default NULL,
  `CardTypeName` varchar(255) default NULL,
  `ContractGuid` char(36) default NULL,
  `CardFlag` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=136;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardtransform`
--

DROP TABLE IF EXISTS `cardtransform`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardtransform` (
  `CardTransformGuid` char(36) NOT NULL,
  `CardGuid` char(36) default NULL,
  `ClassHours` decimal(18,2) default NULL,
  `Amount` decimal(18,2) default NULL,
  `Flow` int(11) default NULL COMMENT '1:现金充值   2:现金扣减   3:课时转换金额   4:金额转换课时',
  `Notes` varchar(200) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  PRIMARY KEY  (`CardTransformGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `cardtype`
--

DROP TABLE IF EXISTS `cardtype`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `cardtype` (
  `CardTypeGuid` char(36) NOT NULL COMMENT '会员卡类型',
  `CardTypeName` varchar(50) default NULL COMMENT '类型名',
  `EffectiveDuration` int(11) default NULL COMMENT '有效期',
  `SortID` int(11) default NULL COMMENT '排序ID',
  `Notes` varchar(50) default NULL COMMENT '备注',
  `DoStatus` int(11) default NULL COMMENT '状态： 99删除（统一）',
  `MallDiscount` decimal(10,2) default NULL,
  PRIMARY KEY  (`CardTypeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `changestorehouselog`
--

DROP TABLE IF EXISTS `changestorehouselog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `changestorehouselog` (
  `ChangeStorehouseLogGuid` char(36) NOT NULL,
  `ProductGuid` char(36) default NULL,
  `OldStorehouseGuid` char(36) default NULL,
  `NewStorehouseGuid` char(36) default NULL,
  `ChangeCount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`ChangeStorehouseLogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=204;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `chatlog`
--

DROP TABLE IF EXISTS `chatlog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `chatlog` (
  `ID` bigint(20) NOT NULL auto_increment,
  `WXOpenID` varchar(200) default NULL,
  `InOutType` varchar(50) default NULL,
  `CreateTime` datetime default NULL,
  `MsgType` varchar(50) default NULL,
  `MsgID` varchar(200) default NULL,
  `Contents` text,
  `MediaId` varchar(200) default NULL,
  `Picurl` text,
  `Format` varchar(150) default NULL,
  `ThumbMediaId` varchar(200) default NULL,
  `Location_X` varchar(50) default NULL,
  `Location_Y` varchar(50) default NULL,
  `Scale` varchar(50) default NULL,
  `Label` text,
  `Title` text,
  `Description` text,
  `Musicurl` text,
  `Hqmusicurl` text,
  `Url` text,
  `FilePath` varchar(230) default NULL,
  `Recognition` text,
  `ManagerGuid` char(36) default NULL,
  `Readed` varchar(50) default NULL,
  `ManagerName` varchar(150) default NULL,
  PRIMARY KEY  (`ID`),
  KEY `UK_chatlog_WXOpenID` (`WXOpenID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=215;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `UpdateActiveTime` AFTER INSERT ON `chatlog` FOR EACH ROW BEGIN  UPDATE subscribeuser  SET    Location = new.Label  WHERE    OpenId = new.WXOpenID    AND    new.MsgType = 'location';  UPDATE subscribeuser  SET    ActiveTime = new.CreateTime  WHERE    OpenId = new.WXOpenID    AND ActiveTime < new.CreateTime;END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `classhour`
--

DROP TABLE IF EXISTS `classhour`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `classhour` (
  `ClassHourGuid` char(36) NOT NULL COMMENT '课时包Guid',
  `ClassHourName` varchar(50) default NULL COMMENT '名称',
  `ClassHours` decimal(18,2) default NULL,
  `Price` decimal(18,0) default NULL COMMENT '价格',
  `Expire` varchar(50) default NULL COMMENT '有效时长',
  `ExpireExtend` int(11) default NULL COMMENT '有效期延长',
  `LeaveDays` int(11) default NULL COMMENT '允许请假天数',
  `Notes` varchar(200) default NULL COMMENT '备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `ComboType` int(11) default NULL,
  `SortID` int(11) default NULL,
  `TotalAmount` decimal(18,2) default NULL,
  `CreateTime` datetime default '1900-01-01 00:00:00',
  `Frequency` int(11) default NULL,
  `ClassPeriod` int(11) default NULL,
  `CourseSeries` int(11) default NULL,
  `WxPublic` int(11) default NULL COMMENT '微信合同套餐标志位,1为微信可见,0或NULL为不可见,默认为NULL',
  `Intro` text COMMENT '合同套餐简介',
  PRIMARY KEY  (`ClassHourGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `classhouritem`
--

DROP TABLE IF EXISTS `classhouritem`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `classhouritem` (
  `ClassHourItemGuid` char(36) NOT NULL COMMENT '主键',
  `ClassHourGuid` char(36) NOT NULL COMMENT '合同套餐主键',
  `ItemGuid` char(36) default NULL COMMENT '课程系列主键',
  `ItemName` varchar(255) default NULL COMMENT '课程系列名称',
  `ItemStandardPrice` decimal(10,2) default NULL COMMENT '单价（标准）',
  `ItemPrice` decimal(10,2) default NULL COMMENT '单价',
  `ItemAmount` decimal(15,2) default NULL,
  `BuyClassHours` decimal(10,2) default NULL,
  `GiftClassHoursLimit` decimal(6,2) default NULL COMMENT '赠送课时上限',
  PRIMARY KEY  (`ClassHourItemGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=150;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `classhourpicture`
--

DROP TABLE IF EXISTS `classhourpicture`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `classhourpicture` (
  `PictureGuid` char(36) NOT NULL COMMENT '主键',
  `ClassHourGuid` char(36) NOT NULL COMMENT '套餐Guid(外键)',
  `PictureSize` bigint(20) default NULL COMMENT '图片大小，单位KB',
  `PicturePath` varchar(255) NOT NULL COMMENT '图片路径',
  `Remark` varchar(255) default NULL COMMENT '备注',
  `Sort` int(11) default NULL COMMENT '套餐图片排序',
  PRIMARY KEY  (`PictureGuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='套餐图片表';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `classhourstransform`
--

DROP TABLE IF EXISTS `classhourstransform`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `classhourstransform` (
  `TransformGuid` char(36) NOT NULL,
  `NewCardGuid` char(36) default NULL,
  `OldCardGuid` char(36) default NULL,
  `NewLessonSeriesGuid` char(36) default NULL,
  `NewLessonSeriesName` varchar(100) default NULL,
  `OldLessonSeriesGuid` char(36) default NULL,
  `OldLessonSeriesName` varchar(100) default NULL,
  `ClassHours` decimal(10,2) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorName` varchar(100) default NULL,
  `Notes` varchar(1000) default NULL,
  `ToClassHours` decimal(10,2) default NULL,
  `SrcContractGuid` char(36) default NULL,
  `TagContractGuid` char(36) default NULL,
  `Cost` decimal(10,2) default '0.00',
  PRIMARY KEY  (`TransformGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=243;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `classroom`
--

DROP TABLE IF EXISTS `classroom`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `classroom` (
  `ClassroomGuid` char(36) NOT NULL COMMENT '教室Guid',
  `ClassroomName` varchar(50) default NULL COMMENT '教室名称',
  `Capacity` int(11) default NULL COMMENT '容纳人数',
  `SortID` int(11) default NULL COMMENT '排序ID',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `Notes` varchar(50) default NULL COMMENT '备注',
  `monitorName` varchar(250) default NULL,
  `monitorUrl` varchar(250) default NULL,
  PRIMARY KEY  (`ClassroomGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `classsection`
--

DROP TABLE IF EXISTS `classsection`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `classsection` (
  `ClassSectionGuid` char(36) NOT NULL COMMENT '第几节课Guid',
  `ClassSectionName` varchar(50) default NULL COMMENT '描述',
  `SortID` int(11) default NULL COMMENT '排序ID',
  `TimeLen` varchar(50) default NULL COMMENT '时间长度，分钟为单位(45)',
  `StartTime` varchar(50) default NULL COMMENT '上课时间(09:00)',
  `EndTime` varchar(50) default NULL COMMENT '下课时间(09:45)',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `Notes` varchar(50) default NULL COMMENT '备注',
  PRIMARY KEY  (`ClassSectionGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `complaintsinfo`
--

DROP TABLE IF EXISTS `complaintsinfo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `complaintsinfo` (
  `Guid` char(36) NOT NULL,
  `Complainant` varchar(100) default NULL COMMENT '投诉人',
  `Phone` varchar(50) default NULL COMMENT '投诉人电话',
  `Address` varchar(255) default NULL COMMENT '投诉人地址',
  `TargetOfComplaint` varchar(255) default NULL COMMENT '投诉对象',
  `DetailInfo` text COMMENT '投诉内容',
  `Status` int(11) default NULL COMMENT '0：未处理 ；1：已处理',
  `CreatorGuid` char(36) default NULL COMMENT '创建人Guid',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `OperatTime` datetime default NULL COMMENT '处理时间',
  `OperatContent` text COMMENT '处理意见',
  `OperatorGuid` char(36) default NULL COMMENT '处理人',
  `ComplaintsTime` datetime default NULL COMMENT '投诉时间',
  PRIMARY KEY  (`Guid`),
  UNIQUE KEY `UK_complaintsinfo_Guid` USING BTREE (`Guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contract`
--

DROP TABLE IF EXISTS `contract`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contract` (
  `ContractGuid` char(36) NOT NULL COMMENT '合同Guid',
  `ContractNum` varchar(50) default NULL COMMENT '合同编号',
  `MemberGuid` char(36) default NULL COMMENT '会员Guid',
  `ClassHourName` varchar(50) default NULL COMMENT '课时包名称',
  `ClassHours` decimal(18,2) default NULL,
  `amount` decimal(18,2) default NULL,
  `LeaveDays` int(11) default NULL COMMENT '允许请假天数',
  `StartDate` datetime default NULL COMMENT '合同起始日期',
  `EndDate` datetime default NULL COMMENT '合同截止日期',
  `SignDate` datetime default NULL COMMENT '合同签约日期',
  `Attachment` varchar(200) default NULL COMMENT '合同附件上传',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `Notes` varchar(200) default NULL COMMENT '合同备注',
  `RefundNotes` varchar(200) default NULL COMMENT '退费备注',
  `DiscardNotes` varchar(200) default NULL COMMENT '作废备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `ContractType` int(11) default NULL COMMENT '合同类型：0 新签约，1 续约',
  `LastDoTime` datetime default NULL,
  `SalemanGuid` char(36) default NULL COMMENT '业务员Guid',
  `YAmount` decimal(18,2) default NULL,
  `ComboType` int(11) default NULL,
  `ContractDepositGuid` char(36) default NULL,
  `CheckUserGuid` char(36) default NULL,
  `CheckDate` datetime default NULL,
  `CheckNotes` text,
  `PayTypeName` varchar(200) default NULL,
  `IsPosPay` int(11) default '0',
  `PosPayAmount` decimal(18,2) default '0.00',
  `Discount` decimal(18,2) default '0.00',
  `ChangePoints` int(11) default NULL,
  `Saleman2Guid` char(36) default '00000000-0000-0000-0000-000000000000' COMMENT '业绩所属人2',
  `BuyClassHours` decimal(10,2) NOT NULL default '0.00',
  `GiftClassHours` decimal(10,2) NOT NULL default '0.00',
  `AverageMode` int(11) NOT NULL default '0',
  `IsNewMode` int(11) NOT NULL default '0',
  `CLevel` int(11) default NULL,
  `Duration` int(11) default NULL,
  `Frequency` int(11) default NULL,
  `ClassPeriod` int(11) default NULL,
  `CourseSeries` int(11) default NULL,
  `PayStatus` int(11) default '0',
  `SalemanShare` decimal(18,2) NOT NULL default '1.00' COMMENT '主业绩所属人业绩占比',
  `Saleman2Share` decimal(18,2) NOT NULL default '0.00' COMMENT '次业绩所属人业绩占比',
  PRIMARY KEY  (`ContractGuid`),
  KEY `contract_memberguid` (`MemberGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractcard`
--

DROP TABLE IF EXISTS `contractcard`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractcard` (
  `ContractCardGuid` char(36) NOT NULL COMMENT '合同-会员卡关系表',
  `ContractGuid` char(36) default NULL,
  `CardGuid` char(36) default NULL,
  PRIMARY KEY  (`ContractCardGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractdeposit`
--

DROP TABLE IF EXISTS `contractdeposit`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractdeposit` (
  `ContractDepositGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `Amount` decimal(10,2) default NULL,
  `PayTypeName` varchar(200) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `ContractGuid` char(36) default NULL,
  `Notes` text,
  `IsPosPay` int(11) default '0',
  `PosPayAmount` decimal(18,2) default '0.00',
  `ContractDepositNo` varchar(200) default NULL,
  `PayDate` datetime default NULL,
  PRIMARY KEY  (`ContractDepositGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=199;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractlessonseries`
--

DROP TABLE IF EXISTS `contractlessonseries`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractlessonseries` (
  `ContractLessonSeriesGuid` char(36) NOT NULL,
  `ContractGuid` char(36) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `ClassHours` decimal(10,2) default NULL,
  `ContractLessonSeriesPackageGuid` char(36) default NULL,
  `BuyClassHoursLeft` decimal(10,2) NOT NULL default '0.00',
  `GiftClassHours` decimal(10,2) NOT NULL default '0.00',
  `GiftClassHoursLeft` decimal(10,2) NOT NULL default '0.00',
  `Total` decimal(10,2) NOT NULL default '0.00',
  `TotalLeft` decimal(10,2) NOT NULL default '0.00',
  `Average` decimal(10,2) NOT NULL default '0.00',
  `ClassHoursPrice` decimal(10,2) NOT NULL default '0.00',
  `Yamount` decimal(10,2) NOT NULL default '0.00',
  `LessonSeriesName` varchar(125) default NULL,
  PRIMARY KEY  (`ContractLessonSeriesGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=330;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractmodel`
--

DROP TABLE IF EXISTS `contractmodel`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractmodel` (
  `ContractModelGuid` char(36) NOT NULL,
  `ContractModelContent` text,
  `CreateTime` datetime default NULL,
  `CreatorUserGuid` char(36) default NULL,
  PRIMARY KEY  (`ContractModelGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractrefund`
--

DROP TABLE IF EXISTS `contractrefund`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractrefund` (
  `ContractRefundGuid` char(36) NOT NULL COMMENT '合同退费',
  `ContractGuid` char(36) default NULL COMMENT '合同Guid',
  `ClassHours` decimal(18,2) default NULL,
  `amount` decimal(18,2) default NULL,
  `RefundDate` datetime default NULL COMMENT '退费日期',
  `Notes` varchar(200) default NULL COMMENT '备注',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `LessonSeriesGuid` char(36) default NULL,
  `LessonSeriesAmount` decimal(10,2) NOT NULL default '0.00',
  `ContractRefundLogGuid` char(36) default NULL COMMENT '退费日志GUID',
  PRIMARY KEY  (`ContractRefundGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractrefundlog`
--

DROP TABLE IF EXISTS `contractrefundlog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractrefundlog` (
  `ContractRefundLogGuid` char(36) NOT NULL,
  `ContractGuid` char(36) NOT NULL COMMENT '合同GUID',
  `ClassHours` decimal(18,2) default NULL COMMENT '实退课时数',
  `Amount` decimal(18,2) default NULL COMMENT '合同实退总金额',
  `RefundDate` datetime default NULL COMMENT '退费日期',
  `Remarks` varchar(200) default NULL COMMENT '备注',
  `CreateTime` datetime NOT NULL COMMENT '创建时间',
  `OperationGuid` char(36) default NULL COMMENT '操作人GUID',
  PRIMARY KEY  (`ContractRefundLogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractshare`
--

DROP TABLE IF EXISTS `contractshare`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractshare` (
  `ContractShareGuid` char(36) NOT NULL COMMENT '主键',
  `ContractGuid` char(36) NOT NULL COMMENT '合同表主键，合同唯一标识',
  `MemberGuid` char(36) NOT NULL COMMENT '学员表主键，学员唯一标识',
  `Priority` int(11) default NULL COMMENT '优先级，值越大优先级越高。(这里和学员资料查看—合同查看中的优先级设置规则要保持一致)，默认值为０。',
  PRIMARY KEY  (`ContractShareGuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='合同共享表';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `contractud`
--

DROP TABLE IF EXISTS `contractud`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `contractud` (
  `ContractGuid` char(36) NOT NULL,
  PRIMARY KEY  (`ContractGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=109;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `course` (
  `CourseGuid` char(36) NOT NULL COMMENT '排课Guid',
  `CourseDate` datetime default NULL COMMENT '上课日期',
  `ClassSectionGuid` char(36) default NULL COMMENT '第几节课Guid',
  `ClassroomGuid` char(36) default NULL COMMENT '教室Guid',
  `LessonGuid` char(36) default NULL COMMENT '课程Guid',
  `Teacher` varchar(500) default NULL,
  `Assistant` varchar(500) default NULL,
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `CreatorGuid` char(36) default NULL COMMENT '创建人Guid',
  `ShowColor` varchar(50) default NULL COMMENT '显示颜色',
  `CourseName` varchar(50) default NULL,
  PRIMARY KEY  (`CourseGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `WagesByCourse_Insert` AFTER INSERT ON `course` FOR EACH ROW BEGIN  
  INSERT INTO wxtemp_course (courseguid, coursedate, coursename, classsection, classroom, DoStatus, CreateTime)  SELECT a.courseguid       , a.coursedate       , a.coursename       , b.classsectionname       , c.classroomname       , 1       , now()  FROM    course a  INNER JOIN classsection b  ON a.classsectionguid = b.classsectionguid  INNER JOIN classroom c  ON a.classroomguid = c.classroomguid  WHERE    a.CourseGuid = new.CourseGuid;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `WagesByCourse_Update` AFTER UPDATE ON `course` FOR EACH ROW BEGIN  
  BEGIN    DECLARE P_CourseGuid                                CHAR(36);    DECLARE P_CourseDate                                DATETIME;    DECLARE P_CourseName, P_ClassSection, P_Classroom   VARCHAR(100);    IF old.CourseDate <> new.CourseDate || old.CourseName <> new.CourseName || old.ClassroomGuid <> new.ClassroomGuid || old.ClassroomGuid <> new.ClassroomGuid THEN      SELECT a.courseguid           , a.coursedate           , a.coursename           , b.classsectionname           , c.classroomname      INTO        P_CourseGuid, P_CourseDate, P_CourseName, P_ClassSection, P_Classroom      FROM        course a      INNER JOIN classsection b      ON a.classsectionguid = b.classsectionguid      INNER JOIN classroom c      ON a.classroomguid = c.classroomguid      WHERE        a.CourseGuid = new.CourseGuid;      DELETE      FROM        wxtemp_course      WHERE        courseguid = P_CourseGuid        AND dostatus = 3;      INSERT INTO wxtemp_course (courseguid, coursedate, coursename, classsection, classroom, DoStatus, CreateTime) VALUE (P_CourseGuid, P_CourseDate, P_CourseName, P_ClassSection, P_Classroom, 3, now());    END IF;  END;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `WagesByCourse_Delete` AFTER DELETE ON `course` FOR EACH ROW BEGIN  
  DELETE  FROM    wxtemp_course  WHERE    courseguid = old.CourseGuid;  INSERT INTO wxtemp_course VALUES (old.courseguid, old.coursedate, old.coursename, '', '', 2, now());END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `courseinfo`
--

DROP TABLE IF EXISTS `courseinfo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `courseinfo` (
  `CourseInfoGuid` char(36) NOT NULL,
  `MPUserGuid` char(36) default NULL,
  `CourseGuid` varchar(255) default NULL,
  `CourseDate` datetime default NULL,
  `CourseName` varchar(400) default NULL,
  `ClassSection` varchar(400) default NULL,
  `Classroom` varchar(400) default NULL,
  `OpenId` varchar(400) default NULL,
  `NickName` varchar(400) default NULL,
  `Sex` varchar(100) default NULL,
  `City` varchar(100) default NULL,
  `Province` varchar(100) default NULL,
  `Country` varchar(100) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `Mobile` varchar(100) default NULL,
  `ParentName` varchar(200) default NULL,
  `MemberName` varchar(200) default NULL,
  `InfoStatus` int(11) default NULL,
  `OpGuid` char(36) default NULL,
  `OpNote` varchar(520) default NULL,
  `OpTime` datetime default NULL,
  `MemberGuid` char(36) default NULL,
  PRIMARY KEY  (`CourseInfoGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `courselist`
--

DROP TABLE IF EXISTS `courselist`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `courselist` (
  `CourseListGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `WaitType` int(11) default NULL,
  `WaitCourseGuid` char(36) default NULL,
  `WaitLessonGuid` char(36) default NULL,
  `SortID` int(11) default NULL,
  `CourseGuid` char(36) default NULL,
  `CourseType` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL,
  `Notes` varchar(300) default NULL,
  PRIMARY KEY  (`CourseListGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1576 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `courserolebycardtype`
--

DROP TABLE IF EXISTS `courserolebycardtype`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `courserolebycardtype` (
  `CardTypeGuid` char(36) NOT NULL,
  `Monday` int(11) default NULL,
  `Tuesday` int(11) default NULL,
  `Wednesday` int(11) default NULL,
  `Thursday` int(11) default NULL,
  `Friday` int(11) default NULL,
  `Saturday` int(11) default NULL,
  `Sunday` int(11) default NULL,
  PRIMARY KEY  (`CardTypeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=137;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `courserolebygroup`
--

DROP TABLE IF EXISTS `courserolebygroup`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `courserolebygroup` (
  `GroupGuid` char(37) NOT NULL,
  `CardTypeGuid` char(36) default NULL,
  `Monday` int(11) default NULL,
  `Tuesday` int(11) default NULL,
  `Wednesday` int(11) default NULL,
  `Thursday` int(11) default NULL,
  `Friday` int(11) default NULL,
  `Saturday` int(11) default NULL,
  `Sunday` int(11) default NULL,
  `CourseCount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`GroupGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=261;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `coursescorelog`
--

DROP TABLE IF EXISTS `coursescorelog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `coursescorelog` (
  `CourseScoreLogGuid` char(36) NOT NULL,
  `MemberCourseGuid` char(36) default NULL,
  `ItemGuid` char(36) default NULL,
  `ItemName` varchar(200) default NULL,
  `Score` int(11) default NULL,
  `CourseDate` varchar(250) default NULL,
  `MemberGuid` char(36) default NULL,
  `Notes` varchar(250) default NULL,
  `GiftPoints` int(11) default '0',
  PRIMARY KEY  (`CourseScoreLogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `courseteacher`
--

DROP TABLE IF EXISTS `courseteacher`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `courseteacher` (
  `CourseTeacherGuid` char(36) NOT NULL,
  `CourseGuid` char(36) default NULL,
  `TeacherGuid` char(36) default NULL,
  `TeacherType` int(11) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`CourseTeacherGuid`),
  KEY `courseteacher_index_courseguid` (`CourseGuid`),
  KEY `courseteacher_index_teacherguid` (`TeacherGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=337;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `courseteacher_back`
--

DROP TABLE IF EXISTS `courseteacher_back`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `courseteacher_back` (
  `CourseTeacherGuid` char(36) NOT NULL,
  `CourseGuid` char(36) default NULL,
  `TeacherGuid` char(36) default NULL,
  `TeacherType` int(11) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `coursetemp`
--

DROP TABLE IF EXISTS `coursetemp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `coursetemp` (
  `CourseGuid` char(36) NOT NULL,
  `CourseDate` datetime default NULL,
  `ClassSectionGuid` char(36) default NULL,
  `ClassroomGuid` char(36) default NULL,
  `LessonGuid` char(36) default NULL,
  `Teacher` varchar(500) default NULL,
  `Assistant` varchar(500) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `ShowColor` varchar(50) default NULL,
  `CourseName` varchar(50) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_applycourse`
--

DROP TABLE IF EXISTS `d_applycourse`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_applycourse` (
  `ApplyCourseGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `CourseGuid` char(36) default NULL,
  `CourseName` varchar(200) default NULL,
  `CourseDate` datetime default NULL,
  `ClassroomName` varchar(200) default NULL,
  `ClassSectionName` varchar(200) default NULL,
  `MemberGuid` char(36) default NULL,
  `MemberName` varchar(200) default NULL,
  `Mobile` varchar(50) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `Notes` varchar(1000) default NULL,
  PRIMARY KEY  (`ApplyCourseGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_applydo`
--

DROP TABLE IF EXISTS `d_applydo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_applydo` (
  `ApplyDoGuid` char(36) NOT NULL,
  `DoGuid` char(36) default NULL,
  `DoTitle` varchar(200) default NULL,
  `StartTime` varchar(200) default NULL,
  `EndTime` varchar(200) default NULL,
  `MemberGuid` char(36) default NULL,
  `MemberName` varchar(100) default NULL,
  `Mobile` varchar(50) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `Notes` varchar(1000) default NULL,
  PRIMARY KEY  (`ApplyDoGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_applyleave`
--

DROP TABLE IF EXISTS `d_applyleave`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_applyleave` (
  `ApplyLeaveGuid` char(36) NOT NULL,
  `CourseGuid` char(36) default NULL,
  `CourseName` varchar(200) default NULL,
  `CourseDate` datetime default NULL,
  `ClassroomName` varchar(200) default NULL,
  `ClassSectionName` varchar(200) default NULL,
  `MemberGuid` char(36) default NULL,
  `MemberName` varchar(100) default NULL,
  `Mobile` varchar(50) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `Notes` varchar(1000) default NULL,
  `Source` int(11) default NULL,
  PRIMARY KEY  (`ApplyLeaveGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_bbsnote`
--

DROP TABLE IF EXISTS `d_bbsnote`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_bbsnote` (
  `NoteGuid` char(36) NOT NULL,
  `ClassGuid` char(36) default NULL,
  `SubjectGuid` char(36) default NULL,
  `NoteTitle` varchar(100) default NULL,
  `NoteContent` varchar(1000) default NULL,
  `Pictures` varchar(1000) default NULL,
  `CreateTime` datetime default NULL,
  `LastReturnTime` datetime default NULL,
  `TopEnable` int(11) default NULL,
  `DoStatus` int(11) default NULL,
  `UserGuid` char(36) default NULL,
  `UserName` varchar(50) default NULL,
  `UserIcon` varchar(200) default NULL,
  `UserType` int(11) default NULL,
  `MemberGuid` char(36) default NULL,
  `GoodCount` int(11) default NULL,
  `ClickCount` int(11) default NULL,
  `BBSType` varchar(50) default NULL,
  `UserRelation` varchar(255) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_bbsnotegclick`
--

DROP TABLE IF EXISTS `d_bbsnotegclick`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_bbsnotegclick` (
  `NoteGClickGuid` char(36) NOT NULL,
  `NoteGuid` char(36) default NULL,
  `UserGuid` char(36) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_bbsreturn`
--

DROP TABLE IF EXISTS `d_bbsreturn`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_bbsreturn` (
  `ReturnGuid` char(36) NOT NULL,
  `NoteGuid` char(36) default NULL,
  `ReturnContent` varchar(1000) default NULL,
  `Pictures` varchar(1000) default NULL,
  `UserGuid` char(36) default NULL,
  `UserName` varchar(50) default NULL,
  `UserIcon` varchar(200) default NULL,
  `UserType` int(11) default NULL,
  `MemberGuid` char(36) default NULL,
  `SchoolGuid` char(36) default NULL,
  `ReturnTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `SortID` int(11) default NULL,
  `UserRelation` varchar(100) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=286;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_bbssubject`
--

DROP TABLE IF EXISTS `d_bbssubject`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_bbssubject` (
  `SubjectGuid` char(36) default NULL,
  `SchoolGuid` char(36) default NULL,
  `ItemName` varchar(100) default NULL,
  `Tips` varchar(200) default NULL,
  `Picture` varchar(100) default NULL,
  `CreateTime` datetime default NULL,
  `SortID` int(11) default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_classphoto`
--

DROP TABLE IF EXISTS `d_classphoto`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_classphoto` (
  `ClassPhotoGuid` char(36) default NULL,
  `CourseGuid` char(36) default NULL,
  `CourseDate` datetime default NULL,
  `CourseName` varchar(200) default NULL,
  `SmallPictures` varchar(500) default NULL,
  `LargePictures` varchar(500) default NULL,
  `ClickCount` int(11) default NULL,
  `GoodCount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `PictureCount` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_commentreply`
--

DROP TABLE IF EXISTS `d_commentreply`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_commentreply` (
  `CommentReplyGuid` char(36) default NULL,
  `SourceGuid` char(36) default NULL,
  `ComStartOne` int(11) default NULL,
  `ComStartTwo` int(11) default NULL,
  `ComStartThree` int(11) default NULL,
  `ReplyContent` varchar(8000) default NULL,
  `UserGuid` char(36) default NULL,
  `UserName` varchar(200) default NULL,
  `UserType` int(11) default NULL,
  `MemberGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `StarLevel` int(11) default NULL,
  `SourceType` varchar(100) default NULL,
  `SourceNotes` varchar(100) default NULL,
  `UserRelation` varchar(50) default NULL,
  `UserIcon` varchar(200) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_healthlog`
--

DROP TABLE IF EXISTS `d_healthlog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_healthlog` (
  `HealthLogGuid` char(36) default NULL,
  `SchoolGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `HealthType` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `LogTime` datetime default NULL,
  `FirstValue` decimal(18,2) default NULL,
  `SecondValue` decimal(18,1) default NULL,
  `thirdValue` decimal(18,2) default NULL,
  `Notes` text
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_healthtype`
--

DROP TABLE IF EXISTS `d_healthtype`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_healthtype` (
  `HealthTypeGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `HealthTypeName` varchar(100) default NULL,
  `DoStatus` int(11) default NULL,
  `SortID` int(11) default NULL,
  `Unit` varchar(100) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_lesson`
--

DROP TABLE IF EXISTS `d_lesson`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_lesson` (
  `LessonGuid` char(36) NOT NULL,
  `LessonName` varchar(50) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `LessonSeriesName` varchar(200) default NULL,
  `MemberCount` int(11) default NULL,
  `FreeCount` int(11) default NULL,
  `ClassHours` decimal(18,2) default NULL,
  `SortID` int(11) default NULL,
  `Notes` varchar(100) default NULL,
  `FitAgeFrom` int(11) default NULL,
  `FitAgeTo` int(11) default NULL,
  `Pictures` varchar(500) default NULL,
  `TeachingPurpose` varchar(500) default NULL,
  `TeachingCharact` varchar(500) default NULL,
  `LessonNotes` text,
  `ClickCount` int(11) default NULL,
  `SchoolGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_manager`
--

DROP TABLE IF EXISTS `d_manager`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_manager` (
  `ManagerGuid` char(36) default NULL,
  `SchoolGuid` char(36) default NULL,
  `RealName` varchar(200) default NULL,
  `Education` varchar(200) default NULL,
  `Maxim` varchar(200) default NULL,
  `Aptitude` varchar(200) default NULL,
  `Reward` varchar(200) default NULL,
  `TeachingCharact` varchar(200) default NULL,
  `ManagerNotes` text,
  `Pictures` varchar(500) default NULL,
  `CreateTime` datetime default NULL,
  `ClickCount` int(11) default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_managerlesson`
--

DROP TABLE IF EXISTS `d_managerlesson`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_managerlesson` (
  `ManagerGuid` char(36) default NULL,
  `SchoolGuid` char(36) default NULL,
  `LessonGuid` char(36) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_message`
--

DROP TABLE IF EXISTS `d_message`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_message` (
  `MessageGuid` char(36) NOT NULL,
  `ParentGuid` char(36) default NULL,
  `UserGuid` char(36) default NULL,
  `UserName` varchar(100) default NULL,
  `MemberName` varchar(100) default NULL,
  `MemberGuid` char(36) default NULL,
  `SchoolGuid` char(36) default NULL,
  `SchoolShowName` varchar(100) default NULL,
  `ManagerGuid` char(36) default NULL,
  `ManagerName` varchar(100) default NULL,
  `MessageContent` text,
  `Readed` int(11) default NULL,
  `Author` varchar(50) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_photo`
--

DROP TABLE IF EXISTS `d_photo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_photo` (
  `PhotoGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `SourceFileGuid` char(36) default NULL,
  `PictureLarge` varchar(255) default NULL,
  `PictureSmall` varchar(255) default NULL,
  `CreateTime` datetime default NULL,
  `UserGuid` char(36) default NULL,
  `SourceFiletype` int(11) default NULL,
  PRIMARY KEY  (`PhotoGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_qfbank`
--

DROP TABLE IF EXISTS `d_qfbank`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_qfbank` (
  `QFBankGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `QFNaireGuid` char(36) default NULL,
  `QuestionbankGuid` char(36) default NULL,
  `QuestionTypeGuid` char(36) default NULL,
  `Title` varchar(200) default NULL,
  `Options` varchar(500) default NULL,
  `Anwser` varchar(50) default NULL,
  `Score` int(11) default NULL,
  `SortID` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_qfnaire`
--

DROP TABLE IF EXISTS `d_qfnaire`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_qfnaire` (
  `QFNaireGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `QuestionNaireGuid` char(36) default NULL,
  `Title` varchar(200) default NULL,
  `Tips` text,
  `QuestionCount` int(11) default NULL,
  `Score` int(11) default NULL,
  `MemberGuid` char(36) default NULL,
  `UserGuid` char(36) default NULL,
  `AnswerTime` datetime default NULL,
  `UserMobile` varchar(100) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_qfresult`
--

DROP TABLE IF EXISTS `d_qfresult`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_qfresult` (
  `QFResultGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `QFNaireGuid` char(36) default NULL,
  `Score` int(11) default NULL,
  `ScoreInfo` varchar(500) default NULL,
  `TimeLen` int(11) default NULL,
  `Note` text,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_questionbank`
--

DROP TABLE IF EXISTS `d_questionbank`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_questionbank` (
  `QuestionbankGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `QuestionTypeGuid` char(36) default NULL,
  `Title` varchar(200) default NULL,
  `Options` varchar(500) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreatorName` varchar(50) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_questionnaire`
--

DROP TABLE IF EXISTS `d_questionnaire`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_questionnaire` (
  `QuestionnaireGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `Title` varchar(200) default NULL,
  `Tips` text,
  `QuestionCount` int(11) default NULL,
  `Score` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreatorName` varchar(50) default NULL,
  `Status` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_questionrecord`
--

DROP TABLE IF EXISTS `d_questionrecord`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_questionrecord` (
  `QuestionRecordGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `QuestionnaireGuid` char(36) default NULL,
  `QuestionbankGuid` char(36) default NULL,
  `QuestionTypeGuid` char(36) default NULL,
  `Title` varchar(200) default NULL,
  `Options` varchar(500) default NULL,
  `SortID` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_questiontype`
--

DROP TABLE IF EXISTS `d_questiontype`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_questiontype` (
  `QuestionTypeGuid` char(36) NOT NULL,
  `SchoolGuid` char(36) default NULL,
  `QuestionTypeName` varchar(50) default NULL,
  `SortID` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreatorName` varchar(50) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_schoolnews`
--

DROP TABLE IF EXISTS `d_schoolnews`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_schoolnews` (
  `NewsGuid` char(36) default NULL,
  `Title` varchar(100) default NULL,
  `Picture` varchar(100) default NULL,
  `Tips` varchar(200) default NULL,
  `NewsType` varchar(50) default NULL,
  `Url` varchar(100) default NULL,
  `Content` text,
  `CreateTime` datetime default NULL,
  `ClickCount` int(11) default NULL,
  `GoodCount` int(11) default NULL,
  `CreatorGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_signup`
--

DROP TABLE IF EXISTS `d_signup`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_signup` (
  `SignUpGuid` char(36) NOT NULL,
  `RelationMobile` varchar(50) default NULL,
  `RelationUser` varchar(200) default NULL,
  `LessonGuid` char(36) default NULL,
  `LessonName` varchar(200) default NULL,
  `UserGuid` char(36) default NULL,
  `SchoolGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL,
  `DealWith` text,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`SignUpGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_summary`
--

DROP TABLE IF EXISTS `d_summary`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_summary` (
  `SummaryGuid` char(36) NOT NULL,
  `StartScore` int(11) default NULL,
  `EndScore` int(11) default NULL,
  `Note` text,
  PRIMARY KEY  (`SummaryGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_systemparam`
--

DROP TABLE IF EXISTS `d_systemparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_systemparam` (
  `ParamGuid` char(36) NOT NULL,
  `ParamName` varchar(200) default NULL,
  `ParamValue` varchar(200) default NULL,
  `ParentGuid` char(36) default NULL,
  `SortID` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `d_teachingachievement`
--

DROP TABLE IF EXISTS `d_teachingachievement`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `d_teachingachievement` (
  `AchievementGuid` char(36) NOT NULL,
  `Title` varchar(100) default NULL,
  `Picture` varchar(100) default NULL,
  `Video` varchar(100) default NULL,
  `AchievementType` varchar(50) default NULL,
  `Location` varchar(100) default NULL,
  `CourseDate` datetime default NULL,
  `ClassName` varchar(50) default NULL,
  `ClickCount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `Notes` text,
  `DoStatus` int(11) default '0',
  PRIMARY KEY  (`AchievementGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `daycaresign`
--

DROP TABLE IF EXISTS `daycaresign`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `daycaresign` (
  `DaycareSignGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `SignType` int(11) default NULL,
  `SignDate` varchar(20) default NULL,
  `Notes` varchar(300) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `ChangePoints` int(11) default NULL,
  PRIMARY KEY  (`DaycareSignGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `dc_classrecord`
--

DROP TABLE IF EXISTS `dc_classrecord`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `dc_classrecord` (
  `Id` char(36) NOT NULL,
  `MemberId` char(36) NOT NULL,
  `ContractId` char(36) NOT NULL,
  `CourseId` char(36) NOT NULL,
  `CourseName` varchar(50) default NULL,
  `CourseDate` datetime default NULL,
  `LessonSeriesId` char(36) NOT NULL,
  `RecordType` int(11) NOT NULL,
  `CreateTime` datetime NOT NULL,
  PRIMARY KEY  (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `department` (
  `DepartmentGuid` char(36) NOT NULL,
  `DepartmentName` varchar(50) default NULL,
  `ParentGuid` char(36) default NULL,
  `SortID` int(11) default NULL,
  `Notes` varchar(100) default NULL,
  PRIMARY KEY  (`DepartmentGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `depreciationlog`
--

DROP TABLE IF EXISTS `depreciationlog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `depreciationlog` (
  `DepreciationLogGuid` char(36) NOT NULL,
  `ProductGuid` char(36) default NULL,
  `OldDepreciation` char(36) default NULL,
  `NewDepreciation` char(36) default NULL,
  `ChangeCount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`DepreciationLogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=204;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `docourse`
--

DROP TABLE IF EXISTS `docourse`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `docourse` (
  `DoGuid` char(36) NOT NULL,
  `DoTypeGuid` char(36) default NULL COMMENT '活动类型GUID',
  `DoTitle` varchar(255) default NULL COMMENT '活动主题',
  `DoContent` text COMMENT '活动的内容',
  `StartTime` varchar(50) default NULL COMMENT '活动开始时间eg:2012-01-01 08:00',
  `EndTime` varchar(50) default NULL COMMENT '活动结束时间',
  `DoProperties` int(11) default NULL COMMENT '活动性质 0:免费 1:收费',
  `ReduceHours` decimal(18,2) default NULL,
  `ReduceCost` int(11) default NULL COMMENT '消耗费用',
  `Cost` int(11) default NULL COMMENT '非会员费用',
  `ClassroomGuid` char(36) default NULL COMMENT '教室Guid',
  `Address` varchar(300) default NULL COMMENT '室外活动地点',
  `TeacherGuid` char(36) default NULL COMMENT '主讲Guid',
  `AssistantGuid` char(36) default NULL COMMENT '助教Guid',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `CreatorGuid` char(36) default NULL COMMENT '创建人Guid',
  `Notes` text,
  `Notes1` text,
  `Notes2` text,
  `LessonSeriesGuids` char(36) default NULL,
  `MemberCount` int(11) default NULL,
  `DoBudget` decimal(18,2) default NULL,
  `DoIncome` decimal(18,2) default NULL,
  `ManagerGuids` varchar(300) default NULL,
  `ManagerNames` varchar(100) default NULL,
  `pictures` varchar(500) default NULL,
  `WxLimit` int(11) default NULL COMMENT '微信活动  0 会员； 1 不限',
  `PayType` int(11) default NULL,
  `ChargeRule` int(11) default NULL COMMENT '收费规则:1表示或，2表示且'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `domanager`
--

DROP TABLE IF EXISTS `domanager`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `domanager` (
  `DoManagerGuid` char(36) NOT NULL,
  `DoGuid` char(36) default NULL,
  `ManagerGuid` char(36) default NULL,
  PRIMARY KEY  (`DoManagerGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `domsglog`
--

DROP TABLE IF EXISTS `domsglog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `domsglog` (
  `Guid` char(36) NOT NULL,
  `TemplateGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `SendTime` datetime default NULL COMMENT '发送次数',
  `OperatorGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL,
  `Reason` varchar(150) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=180;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `domsgtemplate`
--

DROP TABLE IF EXISTS `domsgtemplate`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `domsgtemplate` (
  `Guid` char(36) NOT NULL,
  `TemplateName` varchar(50) default NULL,
  `TemplateContent` text,
  `TemplateParams` text,
  `TemplateTypeGuid` char(36) default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `DoGuid` char(255) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=218;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `dotype`
--

DROP TABLE IF EXISTS `dotype`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `dotype` (
  `DoTypeGuid` char(36) NOT NULL COMMENT '活动类别Guid',
  `DoTypeName` varchar(50) default NULL COMMENT '类别名',
  `SortID` int(11) default NULL COMMENT '排序ID',
  `Notes` varchar(100) default NULL COMMENT '备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  PRIMARY KEY  (`DoTypeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `dtproperties`
--

DROP TABLE IF EXISTS `dtproperties`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `dtproperties` (
  `id` int(11) NOT NULL,
  `objectid` int(11) default NULL,
  `property` varchar(64) NOT NULL,
  `value` varchar(255) default NULL,
  `uvalue` varchar(255) default NULL,
  `lvalue` longblob,
  `version` int(11) NOT NULL,
  PRIMARY KEY  (`id`,`property`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `exchange`
--

DROP TABLE IF EXISTS `exchange`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `exchange` (
  `ExchangeGuid` char(36) NOT NULL COMMENT '积分兑换商品',
  `MemberGuid` char(36) default NULL COMMENT '会员Guid',
  `CostPoints` int(11) default NULL COMMENT '花费积分数目',
  `ProductGuid` char(36) default NULL COMMENT '兑换商品Guid',
  `ExchangeAmount` int(11) default NULL COMMENT '兑换数量',
  `ExchangeDate` datetime default NULL COMMENT '兑换日期',
  `Notes` varchar(200) default NULL COMMENT '备注',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `DoStatus` int(11) default NULL,
  `StorehouseGuid` char(36) default NULL,
  `DepreciationGuid` char(36) default NULL,
  `Channel` varchar(50) default NULL,
  `status` int(11) default NULL,
  PRIMARY KEY  (`ExchangeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `faq`
--

DROP TABLE IF EXISTS `faq`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `faq` (
  `FaqGuid` char(36) NOT NULL,
  `FaqType` int(11) default NULL,
  `ApplyScene` varchar(50) default NULL,
  `FaqContent` text,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  PRIMARY KEY  (`FaqGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `filedownload`
--

DROP TABLE IF EXISTS `filedownload`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `filedownload` (
  `FileDownloadGuid` char(36) NOT NULL,
  `ManagerGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`FileDownloadGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fileinfo`
--

DROP TABLE IF EXISTS `fileinfo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fileinfo` (
  `FileInfoGuid` char(36) NOT NULL,
  `FileName` text COMMENT '显示的文件名',
  `FilePath` text COMMENT '文件站点相当路径',
  `FileRealName` text COMMENT '文件存储名称',
  `FileSize` int(11) default NULL COMMENT '文件大小 单位为kb',
  `FileSuffix` varchar(50) default NULL COMMENT '文件后缀',
  `FileDescription` text COMMENT '文件描述',
  `FolderInfoGuid` char(36) default NULL COMMENT '所属文件夹',
  `IsShare` tinyint(4) default NULL COMMENT '是否共享文件',
  `CreatorGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `EndShareTime` datetime default NULL COMMENT '自动结束共享的时间',
  `DownloadCount` int(11) default NULL COMMENT '下载次数',
  `ViewCount` int(11) default NULL COMMENT '查看次数',
  `MaxCountForDownload` int(11) default NULL COMMENT '每个人最多下载几次',
  `MultiplefilesName` varchar(50) default NULL,
  PRIMARY KEY  (`FileInfoGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=250;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fileshare`
--

DROP TABLE IF EXISTS `fileshare`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fileshare` (
  `FileShareGuid` char(36) NOT NULL,
  `FileInfoGuid` char(36) default NULL,
  `ManagerGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`FileShareGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=333;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `folderinfo`
--

DROP TABLE IF EXISTS `folderinfo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `folderinfo` (
  `FolderInfoGuid` char(36) NOT NULL,
  `FolderName` text COMMENT '文件夹名称',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `CreatorGuid` char(36) default NULL,
  `ParentFolderInfoGuid` char(36) default NULL COMMENT '父文件夹',
  PRIMARY KEY  (`FolderInfoGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=135;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_bindmember`
--

DROP TABLE IF EXISTS `fstemp_bindmember`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_bindmember` (
  `MemberGuid` char(36) default NULL,
  `ManagerGuid` char(36) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=217;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_card`
--

DROP TABLE IF EXISTS `fstemp_card`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_card` (
  `CardGuid` char(36) default '',
  `MemberGuid` char(36) default NULL,
  `CardNo` varchar(200) default NULL,
  `CardTypeName` varchar(100) default NULL,
  `StatusName` varchar(50) default NULL,
  `MainCardGuid` char(36) default NULL,
  `StopDate` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=180;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_cardpackage`
--

DROP TABLE IF EXISTS `fstemp_cardpackage`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_cardpackage` (
  `CardPackageGuid` char(36) default NULL,
  `CardGuid` char(36) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `LessonSeriesName` varchar(100) default NULL,
  `CurrentClassHours` decimal(18,2) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=152;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_classphoto`
--

DROP TABLE IF EXISTS `fstemp_classphoto`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_classphoto` (
  `ClassPhotoGuid` char(36) default NULL,
  `CourseGuid` char(36) default NULL,
  `CourseDate` datetime default NULL,
  `CourseName` varchar(200) default NULL,
  `PictureCount` int(11) default NULL,
  `SmallPictures` varchar(500) default NULL,
  `LargePictures` varchar(500) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=472;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_classroom`
--

DROP TABLE IF EXISTS `fstemp_classroom`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_classroom` (
  `ClassroomGuid` char(36) NOT NULL COMMENT '教室Guid',
  `ClassroomName` varchar(50) default NULL COMMENT '教室名称',
  `Capacity` int(11) default NULL COMMENT '容纳人数',
  `SortID` int(11) default NULL COMMENT '排序ID',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `Notes` varchar(50) default NULL COMMENT '备注',
  `MonitorName` varchar(255) default NULL,
  `MonitorUrl` varchar(255) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_classsection`
--

DROP TABLE IF EXISTS `fstemp_classsection`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_classsection` (
  `ClassSectionGuid` char(36) NOT NULL COMMENT '第几节课Guid',
  `ClassSectionName` varchar(50) default NULL COMMENT '描述',
  `SortID` int(11) default NULL COMMENT '排序ID',
  `TimeLen` varchar(50) default NULL COMMENT '时间长度，分钟为单位(45)',
  `StartTime` varchar(50) default NULL COMMENT '上课时间(09:00)',
  `EndTime` varchar(50) default NULL COMMENT '下课时间(09:45)',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `Notes` varchar(50) default NULL COMMENT '备注'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_contractlessonseries`
--

DROP TABLE IF EXISTS `fstemp_contractlessonseries`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_contractlessonseries` (
  `ContractLessonSeriesGuid` char(36) NOT NULL COMMENT 'ID',
  `ContractGuid` char(36) default NULL COMMENT '合同Guid',
  `LessonSeriesGuid` char(36) default NULL COMMENT '课程系列Guid',
  `ClassHours` decimal(10,2) default NULL COMMENT '课时数',
  `BuyClassHoursLeft` decimal(10,2) default '0.00' COMMENT '购买课时剩余',
  `GiftClassHours` decimal(10,2) default '0.00' COMMENT '赠送课时',
  `GiftClassHoursLeft` decimal(10,2) default '0.00' COMMENT '赠送课时剩余',
  `Total` decimal(10,2) default '0.00' COMMENT '总价',
  `TotalLeft` decimal(10,2) default '0.00' COMMENT '剩余总价',
  `Average` decimal(10,2) default '0.00' COMMENT '均价',
  `MemberGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`ContractLessonSeriesGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_course`
--

DROP TABLE IF EXISTS `fstemp_course`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_course` (
  `CourseGuid` char(36) NOT NULL,
  `CourseName` varchar(200) default NULL,
  `CourseDate` datetime default NULL,
  `ClassroomName` varchar(200) default NULL,
  `ClassroomGuid` char(36) default NULL,
  `ClassSectionName` varchar(200) default NULL,
  `ClassSectionGuid` char(36) default NULL,
  `TeacherNames` varchar(500) default NULL,
  `AssistantNames` varchar(500) default NULL,
  `MemberLimitCount` int(11) default NULL,
  `FreeLimitCount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL COMMENT '增1删2改3',
  `ReduceHours` decimal(10,2) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_coursescorelog`
--

DROP TABLE IF EXISTS `fstemp_coursescorelog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_coursescorelog` (
  `CourseScoreLogGuid` char(36) NOT NULL,
  `MemberCourseGuid` char(36) default NULL,
  `ItemGuid` char(36) default NULL,
  `ItemName` varchar(200) default NULL,
  `Score` int(11) default NULL,
  `CourseDate` varchar(250) default NULL,
  `MemberGuid` char(36) default NULL,
  `Notes` varchar(250) default NULL,
  `SortID` int(11) default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=206;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_do`
--

DROP TABLE IF EXISTS `fstemp_do`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_do` (
  `DoGuid` char(36) NOT NULL,
  `DoTitle` varchar(200) default NULL,
  `DoContent` text,
  `StartTime` varchar(200) default NULL,
  `EndTime` varchar(200) default NULL,
  `DoPropertiesInfo` varchar(200) default NULL,
  `Address` varchar(200) default NULL,
  `MemberCount` int(255) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL COMMENT '增1、删2、改3',
  `pictures` varchar(500) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_lesson`
--

DROP TABLE IF EXISTS `fstemp_lesson`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_lesson` (
  `LessonGuid` char(36) default NULL,
  `Pictures` varchar(500) default NULL,
  `TeachingPurpose` varchar(500) default NULL,
  `TeachingCharact` varchar(500) default NULL,
  `LessonNotes` text,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1474;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_manager`
--

DROP TABLE IF EXISTS `fstemp_manager`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_manager` (
  `ManagerGuid` char(36) default NULL,
  `Maxim` varchar(200) default NULL,
  `Aptitude` varchar(200) default NULL,
  `Reward` varchar(200) default NULL,
  `TeachingCharact` varchar(200) default NULL,
  `ManagerNotes` text,
  `Pictures` varchar(500) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1349;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_managerlesson`
--

DROP TABLE IF EXISTS `fstemp_managerlesson`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_managerlesson` (
  `ManagerGuid` char(36) default NULL,
  `LessonGuid` char(36) default NULL,
  `LessonName` varchar(100) default NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_member`
--

DROP TABLE IF EXISTS `fstemp_member`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_member` (
  `ID` bigint(20) default NULL,
  `MemberGuid` char(36) NOT NULL,
  `RealName` varchar(200) default NULL,
  `Nickname` varchar(200) default NULL,
  `Guardianship` varchar(200) default NULL,
  `Guardian` varchar(200) default NULL,
  `Sex` varchar(10) default NULL,
  `BirthDate` datetime default NULL,
  `Address` text,
  `Phone` varchar(100) default NULL,
  `Mobile` varchar(100) default NULL,
  `Mobile1` varchar(100) default NULL,
  `QQ` varchar(100) default NULL,
  `Email` varchar(100) default NULL,
  `MemberStatus` varchar(100) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `Scope` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=228;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_membercourse`
--

DROP TABLE IF EXISTS `fstemp_membercourse`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_membercourse` (
  `MemberCourseGuid` char(36) NOT NULL,
  `CourseGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `SignStatus` varchar(50) default NULL,
  `CourseType` int(11) default NULL,
  `FeedBackInfo` text,
  `ReduceHours` decimal(10,2) default NULL,
  `ChangePoints` int(11) default NULL,
  `MakeUp` int(11) default NULL,
  `DoStatus` int(11) default NULL,
  `pictures` varchar(500) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_memberdocourse`
--

DROP TABLE IF EXISTS `fstemp_memberdocourse`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_memberdocourse` (
  `MemberDoCourseGuid` char(36) NOT NULL,
  `DoGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `SignStatus` varchar(255) default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_photo`
--

DROP TABLE IF EXISTS `fstemp_photo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_photo` (
  `PhotoGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `SourceFileGuid` char(36) default NULL,
  `PictureLarge` varchar(200) default NULL,
  `PictureSmall` varchar(200) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`PhotoGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_schoolnews`
--

DROP TABLE IF EXISTS `fstemp_schoolnews`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_schoolnews` (
  `NewsGuid` char(36) NOT NULL,
  `Title` varchar(100) default NULL,
  `Picture` varchar(100) default NULL,
  `Tips` varchar(200) default NULL,
  `NewsType` varchar(50) default NULL,
  `Url` varchar(100) default NULL,
  `Content` text,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`NewsGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=727;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `fstemp_teachingachievement`
--

DROP TABLE IF EXISTS `fstemp_teachingachievement`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `fstemp_teachingachievement` (
  `AchievementGuid` char(36) NOT NULL,
  `Title` varchar(100) default NULL,
  `Picture` varchar(100) default NULL,
  `Video` varchar(100) default NULL,
  `AchievementType` varchar(50) default NULL,
  `Location` varchar(100) default NULL,
  `CourseDate` datetime default NULL,
  `ClassName` varchar(50) NOT NULL,
  `Notes` text,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=212;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `importbatch`
--

DROP TABLE IF EXISTS `importbatch`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `importbatch` (
  `BatchGuid` char(36) NOT NULL,
  `BatchTitle` varchar(50) default NULL,
  `BatchSource` varchar(50) default NULL,
  `ImportTime` datetime default NULL,
  `Notes` varchar(200) default NULL,
  `MemberCount` int(11) default NULL,
  `SuccCount` int(11) default NULL,
  `RepeatCount` int(11) default NULL,
  `OtherCount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  PRIMARY KEY  (`BatchGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=123;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `importbatchfollow`
--

DROP TABLE IF EXISTS `importbatchfollow`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `importbatchfollow` (
  `Id` char(36) NOT NULL COMMENT '批次Guid',
  `Name` text COMMENT '批次名称',
  `Notes` text COMMENT '备注',
  `Count` int(11) NOT NULL COMMENT '导入名单总数',
  `CountSuccess` int(11) NOT NULL COMMENT '导入成功的数量',
  `CountFail` int(11) NOT NULL COMMENT '导入失败的数量',
  `CreateTime` datetime NOT NULL COMMENT '创建时间',
  `CreatorId` char(36) NOT NULL COMMENT '创建人Id',
  PRIMARY KEY  (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=123 COMMENT='学员跟进记录导入批次表';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `importdatafollow`
--

DROP TABLE IF EXISTS `importdatafollow`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `importdatafollow` (
  `Id` char(36) NOT NULL,
  `Name` text COMMENT '学员姓名',
  `Mobile` text COMMENT '手机号码',
  `FollowType` text COMMENT '跟进方式',
  `FollowContent` text COMMENT '跟进内容',
  `FollowTime` text COMMENT '跟进时间',
  `FollowTimeNext` text COMMENT '下次跟进时间',
  `FollowPerson` text COMMENT '跟进人',
  `ErrorMessage` text COMMENT '错误信息',
  `ErrorType` int(11) NOT NULL COMMENT '错误类型',
  `IsSuccess` tinyint(1) NOT NULL COMMENT '是否成功',
  `BatchId` char(50) NOT NULL COMMENT '导入批次ID',
  PRIMARY KEY  (`Id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='导入学员跟进记录';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `importfail_47be3304_c8e8_4edb_a836_0bf4c6d2c584`
--

DROP TABLE IF EXISTS `importfail_47be3304_c8e8_4edb_a836_0bf4c6d2c584`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `importfail_47be3304_c8e8_4edb_a836_0bf4c6d2c584` (
  `ID` int(11) NOT NULL auto_increment,
  `学员姓名` varchar(200) default NULL,
  `学员昵称` varchar(200) default NULL,
  `家长姓名` varchar(200) default NULL,
  `家长关系` varchar(200) default NULL,
  `手机号码` varchar(200) default NULL,
  `导入失败原因` varchar(200) default NULL,
  `ReasonIndex` int(11) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `importfailmember`
--

DROP TABLE IF EXISTS `importfailmember`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `importfailmember` (
  `FailGuid` char(36) NOT NULL,
  `RealName` varchar(255) default NULL,
  `NickName` varchar(255) default NULL,
  `Guardian` varchar(255) default NULL,
  `Mobile` varchar(255) default NULL,
  `Birthdate` varchar(255) default NULL,
  `Sex` varchar(255) default NULL,
  `Address` varchar(255) default NULL,
  `QQ` varchar(255) default NULL,
  `EMail` varchar(255) default NULL,
  `Mobile1` varchar(255) default NULL,
  `Phone` varchar(255) default NULL,
  `BirthMode` varchar(255) default NULL,
  `SourceGuid` varchar(255) default NULL,
  `ConsultingGuid` varchar(255) default NULL,
  `CurrentLevel` varchar(255) default NULL,
  `IntentionLesson` varchar(255) default NULL,
  `ImportantLevel` varchar(255) default NULL,
  `BasicInfo` varchar(255) default NULL,
  `ContractNum` varchar(255) default NULL,
  `Amount` varchar(255) default NULL,
  `ClassHours` varchar(255) default NULL,
  `GiftClassHours` varchar(255) default NULL,
  `SignDate` varchar(255) default NULL,
  `StartDate` varchar(255) default NULL,
  `EndDate` varchar(255) default NULL,
  `CardNo` varchar(255) default NULL,
  `CurrentClassHours` varchar(255) default NULL,
  `Reason` varchar(255) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `intentiondate` varchar(200) default NULL,
  PRIMARY KEY  (`FailGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `importfollowfail`
--

DROP TABLE IF EXISTS `importfollowfail`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `importfollowfail` (
  `importFollowFailGuid` char(36) NOT NULL,
  `errorNum` int(11) default NULL,
  `memberName` varchar(50) default NULL,
  `phone` varchar(20) default NULL,
  `followType` varchar(20) default NULL,
  `followBody` varchar(200) default NULL,
  `followTime` varchar(20) default NULL,
  `nextFollowTime` varchar(20) default NULL,
  `salesPhase` varchar(20) default NULL,
  `memberState` varchar(20) default NULL,
  `important` varchar(20) default NULL,
  `errorWhat` varchar(50) default NULL,
  PRIMARY KEY  (`importFollowFailGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `interfaceinfo`
--

DROP TABLE IF EXISTS `interfaceinfo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `interfaceinfo` (
  `InterfaceName` varchar(255) default NULL,
  `InterfaceUrl` varchar(255) default NULL,
  `Notes` varchar(255) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=61;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `inventory` (
  `InventoryGuid` char(36) NOT NULL,
  `ProductGuid` char(36) default NULL,
  `StorehouseGuid` char(36) default NULL,
  `InventoryCount` int(11) default '0',
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `LastInStoreTime` datetime default NULL,
  `LastInStoreUser` char(36) default NULL,
  `Depreciation` char(36) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`InventoryGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=251;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `inventorychange`
--

DROP TABLE IF EXISTS `inventorychange`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `inventorychange` (
  `InventoryChangeGuid` char(36) NOT NULL COMMENT '库存变动',
  `ProductGuid` char(36) default NULL COMMENT '商品Guid',
  `ChangeAmount` int(11) default NULL COMMENT '变动数量',
  `ChangeCost` decimal(18,2) default NULL COMMENT '费用',
  `ChangeDate` datetime default NULL COMMENT '变动日期',
  `Notes` varchar(200) default NULL COMMENT '备注',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `StorehouseGuid` char(36) default NULL,
  `DepreciationGuid` char(36) default NULL,
  `ChangeType` char(36) default NULL,
  PRIMARY KEY  (`InventoryChangeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_func`
--

DROP TABLE IF EXISTS `k_func`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_func` (
  `FuncGuid` char(36) NOT NULL,
  `MenuGuid` char(36) default NULL,
  `FuncCode` varchar(255) default NULL,
  `FuncName` varchar(255) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`FuncGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_infocategory`
--

DROP TABLE IF EXISTS `k_infocategory`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_infocategory` (
  `CategoryGUID` char(36) NOT NULL COMMENT '自增GUID',
  `CategoryName` varchar(50) default NULL COMMENT '类别名',
  `ParentGuid` char(36) default NULL COMMENT '父类GUID',
  `SortID` int(11) default NULL COMMENT '排序ID',
  PRIMARY KEY  (`CategoryGUID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_infocontent`
--

DROP TABLE IF EXISTS `k_infocontent`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_infocontent` (
  `ID` int(11) NOT NULL auto_increment COMMENT '信息内容表',
  `InfoGUID` char(36) default NULL COMMENT '自增GUID',
  `CategoryGUID` char(36) default NULL COMMENT '类别GUID',
  `Title` varchar(50) default NULL COMMENT '标题',
  `Caption` varchar(50) default NULL COMMENT '副标题',
  `Skip` int(11) default NULL COMMENT '跳转标记，0，不跳转到链接地址，1，跳转',
  `Tags` text COMMENT '标签(每个标签用|@|间隔)',
  `Summary` text COMMENT '扼要简介',
  `Content` longtext COMMENT '全部内容',
  `ClickNum` bigint(20) default NULL COMMENT '点击数',
  `ReadNum` bigint(20) default NULL COMMENT '阅读数',
  `OpposeNum` bigint(20) default NULL COMMENT '反对次数',
  `SupportNum` bigint(20) default NULL COMMENT '支持次数',
  `ReviewNum` bigint(20) default NULL COMMENT '评论次数',
  `CreateDate` datetime default NULL COMMENT '创建日期',
  `CreateUser` varchar(50) default NULL COMMENT '创建人',
  `ModifyDate` datetime default NULL COMMENT '修改日期',
  `ModifyUser` varchar(50) default NULL COMMENT '修改人',
  `AuditUser` varchar(50) default NULL COMMENT '审核人',
  `AuditDate` datetime default NULL COMMENT '审核日期',
  `Offer` int(11) default NULL COMMENT '推荐状态（1：）',
  `OfferReason` text COMMENT '推荐理由',
  `OfferTime` datetime default NULL COMMENT '推荐时间',
  `ModifyNotes` text COMMENT '更新备注',
  `Audit` int(11) default NULL COMMENT '审核状态（0：未审核 1：已审核',
  `State` int(11) default NULL COMMENT '状态',
  `ReceiverGuidList` text,
  `ReceiverNameList` text,
  `IsTop` int(11) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_infocontentmanager`
--

DROP TABLE IF EXISTS `k_infocontentmanager`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_infocontentmanager` (
  `InfoManagerGuid` varchar(36) NOT NULL,
  `InfoGuid` varchar(36) NOT NULL,
  `ManagerGuid` varchar(36) default NULL,
  `Status` int(11) default NULL COMMENT '是否阅读 1:已阅，0:未阅读',
  PRIMARY KEY  (`InfoManagerGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=332 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_log`
--

DROP TABLE IF EXISTS `k_log`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_log` (
  `LogGUID` char(36) NOT NULL COMMENT '自增GUID',
  `OperatorGuid` char(36) default NULL COMMENT '操作人员',
  `OperateContent` text,
  `OperateTime` datetime default NULL COMMENT '操作时间',
  `OperateModule` varchar(50) default NULL COMMENT '操作模块',
  `OperateIP` varchar(50) default NULL COMMENT '操作IP',
  `Description` text,
  PRIMARY KEY  (`LogGUID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_mailparam`
--

DROP TABLE IF EXISTS `k_mailparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_mailparam` (
  `ID` int(11) NOT NULL,
  `SmtpHost` varchar(100) default NULL,
  `Port` int(11) default NULL,
  `LoginAcount` varchar(50) default NULL,
  `LoginPwd` varchar(50) default NULL,
  `MailFrom` varchar(50) default NULL,
  `ShowName` varchar(50) default NULL,
  `MailReplyTo` varchar(50) default NULL,
  `ReplyName` varchar(50) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_mailtemplate`
--

DROP TABLE IF EXISTS `k_mailtemplate`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_mailtemplate` (
  `id` int(11) NOT NULL auto_increment,
  `Flow` varchar(50) default NULL,
  `Subject` varchar(100) default NULL,
  `body` text,
  `Note` varchar(200) default NULL,
  `MailTypeGuid` char(36) default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_mailtype`
--

DROP TABLE IF EXISTS `k_mailtype`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_mailtype` (
  `MailTypeGuid` char(36) NOT NULL,
  `MailTypeName` varchar(255) default NULL,
  `ParentGuid` char(36) default NULL,
  `SortID` int(11) default '0',
  PRIMARY KEY  (`MailTypeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_manager`
--

DROP TABLE IF EXISTS `k_manager`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_manager` (
  `ManagerGUID` char(36) NOT NULL COMMENT '自增GUID',
  `DepartmentGuid` char(36) default NULL COMMENT '部门GUID',
  `PositionGuid` char(36) default NULL,
  `UserName` varchar(50) default NULL COMMENT '用户名',
  `LoginPwd` varchar(50) default NULL COMMENT '密码MD5',
  `RealName` varchar(50) default NULL COMMENT '真实姓名',
  `Idcard` varchar(50) default NULL COMMENT '身份证号码',
  `JobDate` datetime default NULL COMMENT '入职时间',
  `DepartDate` datetime default NULL COMMENT '离职时间',
  `Education` varchar(50) default NULL COMMENT '学历',
  `Profession` varchar(50) default NULL COMMENT '专业',
  `Phone` varchar(50) default NULL COMMENT '联系电话',
  `Mobile` varchar(50) default NULL COMMENT '手机',
  `Email` varchar(50) default NULL COMMENT '邮箱',
  `QQ` varchar(50) default NULL,
  `MSN` varchar(50) default NULL,
  `WorkPhone` varchar(50) default NULL COMMENT '工作电话',
  `WorkMobile` varchar(50) default NULL COMMENT '工作手机',
  `WorkEmail` varchar(50) default NULL COMMENT '工作邮箱',
  `CreateTime` datetime default NULL COMMENT '创建日期',
  `CreatorGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL COMMENT '停用状态（0：正常1：停用）',
  `Notes` text,
  `IsAdvisor` bit(1) default NULL,
  `IsTeacher` bit(1) default NULL,
  `MemberStatus` varchar(1000) default NULL,
  `IsMktStaff` bit(1) default NULL,
  `LevelGuid` char(36) default NULL,
  `Sex` varchar(10) default NULL,
  `BirthDate` datetime default NULL,
  `IsLunar` bit(1) default NULL,
  `GraduateDate` datetime default NULL,
  `GraduateSchool` varchar(100) default NULL,
  `Hometown` varchar(100) default NULL,
  `Specialty` varchar(500) default NULL,
  `Photo` varchar(200) default NULL,
  `Marriage` varchar(10) default NULL,
  `LoginEnable` bit(1) default NULL,
  `Attachment` varchar(500) default NULL,
  `ContractStartDate` datetime default NULL,
  `ContractEndDate` datetime default NULL,
  `PhonePWExpireDate` datetime default NULL,
  `PhonePassword` varchar(200) default NULL,
  `IsFloatMenu` bit(1) default NULL,
  PRIMARY KEY  (`ManagerGUID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_managerrole`
--

DROP TABLE IF EXISTS `k_managerrole`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_managerrole` (
  `ManagerRoleGuid` char(36) NOT NULL,
  `ManagerGuid` char(36) default NULL,
  `RoleGuid` char(36) default NULL,
  PRIMARY KEY  (`ManagerRoleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_menu`
--

DROP TABLE IF EXISTS `k_menu`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_menu` (
  `MenuGuid` char(36) NOT NULL COMMENT '菜单栏目Guid',
  `ParentGuid` char(36) default NULL COMMENT '上级栏目Guid',
  `MenuName` varchar(50) default NULL COMMENT '栏目名称',
  `MenuUrl` varchar(100) default NULL COMMENT '链接地址',
  `MenuType` int(11) default NULL COMMENT '功能类型：0 可更名菜单，1 系统菜单',
  `Depth` int(11) default NULL COMMENT '栏目层级',
  `SortID` int(11) default NULL COMMENT '排序号',
  `UrlParam` varchar(150) default NULL COMMENT 'url传递参数',
  `MenuIcon` varchar(100) default NULL,
  `SubPages` varchar(300) default NULL,
  `IsTab` int(11) default '0',
  PRIMARY KEY  (`MenuGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_msglog`
--

DROP TABLE IF EXISTS `k_msglog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_msglog` (
  `MsgGuid` char(36) NOT NULL,
  `OriginalMobiles` longtext,
  `SuccMobiles` longtext,
  `FailMobiles` longtext,
  `MsgContent` text,
  `SuccCount` int(11) default NULL,
  `MsgWordCount` int(11) default NULL,
  `Price` decimal(18,2) default NULL,
  `Cost` decimal(18,2) default NULL,
  `SetSendTime` varchar(50) default NULL,
  `SendTime` datetime default NULL,
  `SendUserGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL,
  `Reason` varchar(200) default NULL,
  `TemplateType` int(11) default NULL,
  `TotalCount` int(11) default NULL,
  `FailCount` int(11) default NULL,
  `limitwordcount` int(11) default NULL,
  `singlecount` int(11) default NULL,
  `BillCount` int(11) default NULL,
  PRIMARY KEY  (`MsgGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_msgparam`
--

DROP TABLE IF EXISTS `k_msgparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_msgparam` (
  `ID` int(11) NOT NULL,
  `WebServerUrl` varchar(100) default NULL,
  `UserKey` varchar(50) default NULL,
  `UserName` varchar(50) default NULL,
  `Password` varchar(50) default NULL,
  `Action` varchar(50) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_msgtemplate`
--

DROP TABLE IF EXISTS `k_msgtemplate`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_msgtemplate` (
  `ID` int(11) NOT NULL,
  `TemplateName` varchar(50) default NULL,
  `TemplateType` int(11) default NULL COMMENT '0:流程模版 1:自动发送',
  `Contents` text,
  `Notes` varchar(200) default NULL,
  PRIMARY KEY  (`ID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_paylog`
--

DROP TABLE IF EXISTS `k_paylog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_paylog` (
  `LogGuid` char(36) NOT NULL,
  `Cost` decimal(10,2) default NULL COMMENT '金额',
  `RGuid` char(36) default NULL COMMENT '关联Guid',
  `DoStatus` int(11) default NULL COMMENT '状态 0 未支付 1已支付',
  `LogType` int(11) default NULL COMMENT '类型 0 活动支付',
  `CreateTime` datetime default NULL COMMENT '创建日期',
  `PayTime` datetime default NULL COMMENT '支付时间',
  `MemberGuid` char(36) default NULL COMMENT '学员GUid',
  `OpenId` varchar(255) default NULL COMMENT 'OpenId',
  PRIMARY KEY  (`LogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_rightgroup`
--

DROP TABLE IF EXISTS `k_rightgroup`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_rightgroup` (
  `RightGroupGuid` char(36) NOT NULL,
  `RightGroupName` varchar(50) default NULL,
  `SortID` int(11) default NULL,
  `Note` varchar(200) default NULL,
  PRIMARY KEY  (`RightGroupGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_role`
--

DROP TABLE IF EXISTS `k_role`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_role` (
  `RoleGuid` char(36) NOT NULL,
  `RoleName` varchar(50) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`RoleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_rolefunc`
--

DROP TABLE IF EXISTS `k_rolefunc`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_rolefunc` (
  `RoleFuncGuid` char(36) NOT NULL,
  `RoleGuid` char(36) default NULL,
  `FuncGuid` char(36) default NULL,
  PRIMARY KEY  (`RoleFuncGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_rolemenu`
--

DROP TABLE IF EXISTS `k_rolemenu`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_rolemenu` (
  `RoleMenuGuid` char(36) NOT NULL,
  `RoleGuid` char(36) default NULL,
  `MenuGuid` char(36) default NULL,
  PRIMARY KEY  (`RoleMenuGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_systemconfig`
--

DROP TABLE IF EXISTS `k_systemconfig`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_systemconfig` (
  `SystemConfigGuid` char(36) NOT NULL COMMENT '系统配置表',
  `CompanyName` varchar(150) default NULL COMMENT '公司名称',
  `LogoImg` varchar(150) default NULL COMMENT '内页logo',
  `LoginImg` varchar(150) default NULL COMMENT '登录的图片',
  `IndexContent` varchar(50) default NULL COMMENT '首页显示的内容的ID',
  `CardSwitch` char(1) default NULL COMMENT '会员卡功能启用关闭开关',
  `LateMinute` int(11) default NULL COMMENT '晚来超过多少分钟算迟到',
  `AbsentMinute` int(11) default NULL COMMENT '晚来超过多少分钟算旷课',
  `AbsentTimes` int(11) default NULL COMMENT '旷课次数达到多少次，开始扣课',
  `CourseAutoSend` char(1) default NULL COMMENT '上课自动短信提醒：N不发送，Y发送',
  `CourseTimeSetting` int(11) default NULL COMMENT '提前分钟数',
  `DoCourseAutoSend` char(1) default NULL COMMENT '活动自动短信提醒：N不发送，Y发送',
  `DoCourseTimeSetting` int(11) default NULL COMMENT '提前分钟数',
  `BirthDayAutoSend` char(1) default NULL,
  `BirthDayTimeSetting` varchar(50) default NULL,
  `SMSSerialNo` varchar(50) default NULL COMMENT '短信序列号',
  `VersionNo` varchar(50) default NULL COMMENT '软件版本号',
  `Notes1` varchar(50) default NULL,
  `Notes2` varchar(50) default NULL,
  `Notes3` varchar(50) default NULL,
  `IsCsRuning` datetime default NULL COMMENT 'cs小程序是的正在运行',
  `Print_CompanyName` varchar(50) default NULL,
  `Print_Phone` varchar(50) default NULL,
  `Print_Notes` varchar(250) default NULL,
  `BackUp_BinPath` varchar(200) default NULL COMMENT 'Mysql备份 bin路径',
  `BackUp_DBUserName` varchar(50) default NULL COMMENT 'Mysql备份 用户名',
  `Backup_Pwd` varchar(50) default NULL COMMENT 'Mysql备份 密码',
  `ScanSwitch` bit(1) default NULL,
  `FashionLogoImg` varchar(100) default NULL,
  `FashionLoginImg` varchar(100) default NULL,
  `VoipShowPhone` varchar(100) default NULL,
  `MakeUpLessonConsume` char(1) default NULL,
  `LeaveCount` int(11) default NULL,
  `CourseAutoSendWx` char(1) default NULL,
  `CourseTimeSettingWx` int(11) default NULL,
  `ClassHourWarn` decimal(10,2) default NULL,
  PRIMARY KEY  (`SystemConfigGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_systemparam`
--

DROP TABLE IF EXISTS `k_systemparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_systemparam` (
  `ID` int(11) NOT NULL auto_increment COMMENT '统一编码表',
  `ParamName` varchar(50) default NULL COMMENT '参数名称',
  `ParamValue` varchar(50) default NULL COMMENT '参数值',
  `ParentID` int(11) default NULL COMMENT '上级ID',
  `ParamType` int(11) default NULL COMMENT '参数类型：0 自定义参数，1 系统参数',
  `SortID` int(11) default NULL COMMENT '排序',
  PRIMARY KEY  (`ID`),
  UNIQUE KEY `ID` USING BTREE (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=288 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `k_wxlog`
--

DROP TABLE IF EXISTS `k_wxlog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `k_wxlog` (
  `wxlogGuid` char(36) NOT NULL,
  `memberCourseGuid` char(36) default NULL COMMENT '排课主键',
  `SendType` int(11) default NULL COMMENT '1 上课自动发微信提醒',
  `SendTime` datetime default NULL COMMENT '发送时间',
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`wxlogGuid`),
  UNIQUE KEY `memberCourseGuid` (`memberCourseGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `leave`
--

DROP TABLE IF EXISTS `leave`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `leave` (
  `LeaveGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `CourseGuid` char(36) default NULL,
  `CourseType` int(11) default NULL,
  `LeaveType` int(11) default NULL,
  `Reason` text,
  `StartTime` datetime default NULL,
  `EndTime` datetime default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Note` varchar(100) default NULL,
  PRIMARY KEY  (`LeaveGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `lesson`
--

DROP TABLE IF EXISTS `lesson`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lesson` (
  `LessonGuid` char(36) NOT NULL COMMENT '课程Guid',
  `LessonName` varchar(50) default NULL COMMENT '课程名称',
  `LessonSeriesGuid` char(36) default NULL COMMENT '课程系列Guid',
  `MemberCount` int(11) default NULL COMMENT '会员容量',
  `FreeCount` int(11) default NULL COMMENT '体验容量',
  `ClassHours` decimal(18,2) default NULL,
  `Price` decimal(18,2) default NULL,
  `SortID` int(11) default NULL COMMENT '排序ID',
  `Notes` varchar(100) default NULL COMMENT '备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `FitAgeFrom` int(11) default NULL,
  `FitAgeTo` int(11) default NULL,
  `IsGeneralClassHour` int(11) default NULL,
  `GeneralClassHour` decimal(18,2) default NULL,
  PRIMARY KEY  (`LessonGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `lessonorder`
--

DROP TABLE IF EXISTS `lessonorder`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lessonorder` (
  `OrderGuid` char(36) NOT NULL COMMENT '订单Guid，主键',
  `OrderNumber` varchar(50) NOT NULL COMMENT '订单编号',
  `IsLessonPackage` int(11) NOT NULL COMMENT '是否套餐包：0-否，1-是',
  `ClassHourGuid` char(36) default NULL COMMENT '套餐Guid',
  `ClassHourName` varchar(50) default NULL COMMENT '课时包名称',
  `LessonPackageType` int(11) NOT NULL COMMENT '课时包类型:0课时套餐，1托班套餐，2时长',
  `Amount` decimal(10,2) NOT NULL COMMENT '订单总价',
  `MemberGuid` char(36) default NULL COMMENT '订单所属学员Guid',
  `MemberName` varchar(50) default NULL COMMENT '订单所属学员名称',
  `Mobile` varchar(15) default NULL COMMENT '学员手机号',
  `BirthDate` datetime default NULL COMMENT '出生日期',
  `Address` varchar(200) default NULL COMMENT '学员居住地址',
  `CreateTime` datetime NOT NULL COMMENT '订单创建时间',
  `PayTime` datetime default NULL COMMENT '订单支付时间',
  `DoStatus` int(11) NOT NULL COMMENT '订单状态：0-未支付，1-已支付，2-已作废',
  `Channel` int(11) NOT NULL COMMENT '订单来源渠道：1：微信',
  `Expire` int(11) default NULL COMMENT '时长',
  `CourseSeries` int(11) default NULL COMMENT '课程系列：0-部分，1-全部',
  `IsCreateContract` int(11) default NULL COMMENT '是否创建过合同：0-否，1-是',
  `Frequency` int(11) default NULL COMMENT '频次',
  `ClassPeriod` int(11) default NULL COMMENT '频次周期',
  `Remark` varchar(200) default NULL COMMENT '备注',
  `WXOpenID` varchar(200) default NULL COMMENT '微信openid',
  `ContractGuid` char(36) default NULL COMMENT '合同Guid',
  PRIMARY KEY  (`OrderGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='订单表';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `lessonorderitem`
--

DROP TABLE IF EXISTS `lessonorderitem`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lessonorderitem` (
  `OrderItemGuid` char(36) NOT NULL COMMENT '订单明细Guid，主键',
  `OrderGuid` char(36) NOT NULL COMMENT '订单表主键(外键)',
  `ItemGuid` char(36) NOT NULL COMMENT '课程系列Guid',
  `ItemName` varchar(50) default NULL COMMENT '课程系列名称',
  `ItemPrice` decimal(18,2) NOT NULL COMMENT '课程系列单价',
  `ItemAmount` decimal(18,2) NOT NULL COMMENT '课程系列总价',
  `BuyClassHours` decimal(10,2) default NULL COMMENT '购买课时',
  `GiftClassHours` decimal(10,2) default NULL COMMENT '赠送课时',
  `Remark` varchar(200) default NULL COMMENT '备注',
  PRIMARY KEY  (`OrderItemGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='订单明细表';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `lessonseries`
--

DROP TABLE IF EXISTS `lessonseries`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `lessonseries` (
  `LessonSeriesGuid` char(36) NOT NULL COMMENT '课程系列Guid',
  `LessonSeriesName` varchar(50) default NULL COMMENT '课程系列名称',
  `SortID` int(11) default NULL COMMENT '排序ID',
  `Notes` varchar(50) default NULL COMMENT '备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `Price` decimal(18,2) default NULL,
  PRIMARY KEY  (`LessonSeriesGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `liftlog`
--

DROP TABLE IF EXISTS `liftlog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `liftlog` (
  `LiftLogGuid` char(36) NOT NULL,
  `LiftLogType` varchar(255) default NULL,
  `DataGuid` char(36) default NULL,
  `DataTitle` varchar(255) default NULL,
  `DataContent` text,
  `CreateTime` datetime default NULL,
  `MemberGuid` char(36) default NULL,
  PRIMARY KEY  (`LiftLogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=222;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `maillog`
--

DROP TABLE IF EXISTS `maillog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `maillog` (
  `MailLogGuid` char(36) NOT NULL,
  `MailSubject` text COMMENT '标题',
  `MailBody` mediumtext COMMENT '内容',
  `MailToAddress` text COMMENT '接收地址',
  `MailFromAddress` varchar(100) default NULL COMMENT '发送地址',
  `MailSendTime` datetime default NULL COMMENT '发送时间',
  `MailAttachments` text COMMENT '附件',
  `OperatorGuid` char(36) default NULL,
  `Status` int(11) default NULL,
  `SendStatus` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `mallparam`
--

DROP TABLE IF EXISTS `mallparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `mallparam` (
  `MallParamGuid` char(36) default NULL,
  `ParamValue` varchar(50) default NULL,
  `SortID` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managerconfig`
--

DROP TABLE IF EXISTS `managerconfig`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managerconfig` (
  `ManagerGuid` char(36) NOT NULL COMMENT '工作人员Guid',
  `ShowCourseDays` int(11) default NULL COMMENT '课表显示天数设置',
  `ShowTeacher` int(11) default NULL COMMENT '课表中是否显示主教老师',
  `ShowAssistant` int(11) default NULL COMMENT '课表中是否显示助教',
  `ShowMemberCount` int(11) default NULL COMMENT '课表中是否显示选课人数',
  `DesktopUrl` text COMMENT '系统背景图片路径',
  `SysSkinGuid` char(36) default NULL COMMENT '皮肤',
  `ShowWeek` varchar(50) default NULL,
  `Lang` int(11) default NULL COMMENT '0：简体中文；1：繁体中文；2：英文',
  `GuidingLayer` int(11) default NULL,
  PRIMARY KEY  (`ManagerGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managerquickapp`
--

DROP TABLE IF EXISTS `managerquickapp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managerquickapp` (
  `ManagerQuickAppGuid` char(36) NOT NULL,
  `ManagerGuid` char(36) default NULL,
  `MenuGuid` char(36) default NULL,
  PRIMARY KEY  (`ManagerQuickAppGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managertask`
--

DROP TABLE IF EXISTS `managertask`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managertask` (
  `TaskID` bigint(20) NOT NULL auto_increment,
  `TaskContent` text,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `ReceiverGuid` char(36) default NULL,
  `Notes` text,
  `TaskType` int(11) default NULL,
  `ParentTaskID` bigint(20) default NULL,
  `DoStatus` int(11) default NULL,
  `ReadTime` datetime default NULL,
  `ReadUserGuid` char(36) default NULL,
  PRIMARY KEY  (`TaskID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managervoip`
--

DROP TABLE IF EXISTS `managervoip`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managervoip` (
  `ManagerGuid` char(36) NOT NULL,
  `EnableVoip` int(11) default NULL,
  `MainAccount` varchar(255) default NULL,
  `MainPwd` varchar(255) default NULL,
  `AccountSID` varchar(200) default NULL,
  `AccountToken` varchar(200) default NULL,
  `VoipAccount` varchar(200) default NULL,
  `VoipPwd` varchar(200) default NULL,
  `ShowPhone` varchar(200) default NULL,
  PRIMARY KEY  (`ManagerGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=216;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managervoip_bak`
--

DROP TABLE IF EXISTS `managervoip_bak`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managervoip_bak` (
  `ManagerGuid` char(36) NOT NULL,
  `EnableVoip` int(11) default NULL,
  `MainAccount` varchar(255) default NULL,
  `MainPwd` varchar(255) default NULL,
  `AccountSID` varchar(200) default NULL,
  `AccountToken` varchar(200) default NULL,
  `VoipAccount` varchar(200) default NULL,
  `VoipPwd` varchar(200) default NULL,
  `ShowPhone` varchar(200) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managerwages`
--

DROP TABLE IF EXISTS `managerwages`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managerwages` (
  `WagesGuid` char(36) NOT NULL,
  `WagesDate` varchar(7) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `CheckTime` datetime default NULL,
  `CheckUserGuid` varchar(255) default NULL,
  `PayOffTime` datetime default NULL,
  `PayOffUserGuid` char(36) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`WagesGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=188;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managerwagesconfig`
--

DROP TABLE IF EXISTS `managerwagesconfig`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managerwagesconfig` (
  `ManagerGuid` char(36) NOT NULL,
  `BasicWages` decimal(10,2) default NULL,
  `Bonus` decimal(10,2) default NULL,
  `OtherIn` decimal(10,2) default NULL,
  `OtherOut` decimal(10,2) default NULL,
  PRIMARY KEY  (`ManagerGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=129;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `managerwageslist`
--

DROP TABLE IF EXISTS `managerwageslist`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `managerwageslist` (
  `ManagerGuid` char(36) NOT NULL,
  `WagesGuid` char(36) NOT NULL,
  `BasicWages` decimal(10,2) default NULL,
  `Bonus` decimal(10,2) default NULL,
  `Achievement` decimal(10,2) default NULL,
  `OtherIn` decimal(10,2) default NULL,
  `OtherOut` decimal(10,2) default NULL,
  `SumWages` decimal(10,2) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`ManagerGuid`,`WagesGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=112;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `marketnode`
--

DROP TABLE IF EXISTS `marketnode`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `marketnode` (
  `NodeGuid` char(36) NOT NULL,
  `NodeName` varchar(50) default NULL,
  `SortID` int(11) default NULL,
  `Notes` varchar(200) default NULL,
  `MemberStatus` int(11) default NULL,
  PRIMARY KEY  (`NodeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member` (
  `ID` bigint(20) NOT NULL auto_increment COMMENT '会员表',
  `MemberGuid` char(36) NOT NULL COMMENT '会员Guid',
  `RealName` varchar(50) default NULL COMMENT '真实姓名',
  `Nickname` varchar(50) default NULL COMMENT '小名',
  `Guardianship` int(11) default NULL COMMENT '监护关系',
  `Guardian` varchar(50) default NULL COMMENT '监护人',
  `Sex` varchar(10) default NULL,
  `BirthDate` datetime default NULL COMMENT '出生日期',
  `Address` text COMMENT '地址',
  `Phone` varchar(50) default NULL COMMENT '联系电话',
  `Mobile` varchar(50) default NULL COMMENT '移动电话',
  `Mobile1` varchar(50) default NULL COMMENT '移动电话1',
  `Msn` varchar(50) default NULL COMMENT 'MSN',
  `QQ` varchar(50) default NULL,
  `Email` varchar(50) default NULL,
  `photo` text,
  `basicinfo` text,
  `CurrentLevel` varchar(50) default NULL,
  `Scope` decimal(18,0) default '0' COMMENT '会员积分',
  `IsVisited` int(11) default NULL COMMENT '是否到访过',
  `VisitDate` datetime default NULL COMMENT '到访日期',
  `VisitInfo` text COMMENT '到访情况',
  `IsExperienced` int(11) default NULL COMMENT '是否体验',
  `ExperienceDate` datetime default NULL COMMENT '体验日期',
  `ExperienceInfo` text COMMENT '体验情况',
  `SignDate` datetime default NULL COMMENT '签约日期',
  `CreateTime` datetime default NULL COMMENT '创建日期',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `Notes` text COMMENT '备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `SourceGuid` char(36) default NULL,
  `BirthMode` int(11) default NULL,
  `ConsultingGuid` char(36) default NULL,
  `ImportBatchGuid` char(36) default NULL,
  `MktStaffGuid` char(36) default NULL,
  `IntentionLesson` varchar(100) default NULL,
  `ImportantLevel` char(36) default NULL,
  `LastFollowTime` datetime default NULL,
  `LastCourseDate` datetime default NULL,
  `AreaGuid` char(36) default NULL,
  `intentiondate` datetime default NULL,
  `MarketNodeGuid` char(36) default NULL,
  `Marks` varchar(2000) default NULL,
  `WXUserName` varchar(200) default NULL,
  `WXOpenID` varchar(200) default NULL,
  `mobileLocation` varchar(200) default NULL,
  `MemberType` int(11) default NULL,
  `courseDoneTime` datetime default NULL,
  `FacePhoto` varchar(2000) default NULL COMMENT '人脸识别照片',
  `UnRecognizeFacePhoto` int(11) default NULL COMMENT '标识为未识别的人脸识别照片',
  `FaceCharacteristics` text,
  PRIMARY KEY  (`ID`),
  KEY `MemberGuid` (`MemberGuid`),
  KEY `UK_member_WXOpenID` (`WXOpenID`),
  KEY `mktstaffguid_index_member` (`MktStaffGuid`),
  KEY `INDEX_mobile` USING BTREE (`Mobile`)
) ENGINE=MyISAM AUTO_INCREMENT=5373 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member_courselog`
--

DROP TABLE IF EXISTS `member_courselog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member_courselog` (
  `CourseLogGuid` char(36) NOT NULL,
  `CourseGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `LogType` int(11) default NULL,
  `Notes` text,
  PRIMARY KEY  (`CourseLogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=242 COMMENT='0:预约上课，1：请假，2：预约活动';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member_log`
--

DROP TABLE IF EXISTS `member_log`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member_log` (
  `LogGuid` char(36) NOT NULL,
  `OperatorGuid` char(36) default NULL,
  `OperateContent` text,
  `OperateTime` datetime default NULL,
  `OperateModule` text,
  `OperateIP` varchar(200) default NULL,
  `Description` text,
  PRIMARY KEY  (`LogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=189;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member_menurole`
--

DROP TABLE IF EXISTS `member_menurole`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member_menurole` (
  `MenuGuid` char(36) NOT NULL,
  `MenuName` varchar(200) default NULL,
  `Role` int(11) default NULL,
  `PageName` varchar(200) default NULL,
  PRIMARY KEY  (`MenuGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=89;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member_message`
--

DROP TABLE IF EXISTS `member_message`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member_message` (
  `MessageGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `MessageContent` text,
  `CreateTime` datetime default NULL,
  `MessageType` int(11) default NULL,
  `Notes` text,
  PRIMARY KEY  (`MessageGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member_param`
--

DROP TABLE IF EXISTS `member_param`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member_param` (
  `ParamGuid` char(36) NOT NULL,
  `ParamName` varchar(200) default NULL,
  `ParamValue` varchar(200) default NULL,
  `ParentGuid` char(36) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`ParamGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=111;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member_setting`
--

DROP TABLE IF EXISTS `member_setting`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member_setting` (
  `SettingGuid` char(36) NOT NULL,
  `MenuRole` varchar(200) default NULL,
  `CourseWeeks` varchar(200) default NULL,
  `DelayCourseDays` int(11) default NULL,
  `DelayLeaveHours` int(11) default NULL,
  PRIMARY KEY  (`SettingGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=60;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `member_userlist`
--

DROP TABLE IF EXISTS `member_userlist`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `member_userlist` (
  `UserGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `UserName` varchar(100) default NULL,
  `LoginPwd` varchar(200) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `Notes` text,
  PRIMARY KEY  (`UserGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=139;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberappoint`
--

DROP TABLE IF EXISTS `memberappoint`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberappoint` (
  `MemberAppointGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `AppointTime` datetime default NULL,
  `AppointContent` varchar(500) default NULL,
  `AppointWay` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` varchar(200) default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`MemberAppointGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberAppoint_Insert` AFTER INSERT ON `memberappoint` FOR EACH ROW BEGIN  
  INSERT INTO liftlog  SELECT uuid()       , 4       , a.MemberAppointGuid       , '客户预约'       , concat('跟进人：', b.UserName, '，预约时间', a.AppointTime, '，预约方式：', ifnull(c.ParamName, ''), '，内容：', a.AppointContent)       , now()       , new.MemberGuid  FROM    memberappoint a  LEFT JOIN k_manager b  ON a.CreatorGuid = b.ManagerGUID  LEFT JOIN k_systemparam c  ON a.AppointWay = c.ID  WHERE    a.MemberAppointGuid = new.MemberAppointGuid;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberAppoint_Update` AFTER UPDATE ON `memberappoint` FOR EACH ROW BEGIN  
  IF old.DoStatus <> new.DoStatus THEN    INSERT INTO liftlog    SELECT uuid()         , 4         , new.MemberAppointGuid         , '预约确认'         , concat('跟进人：', b.UserName, '，预约方式：', ifnull(c.ParamName, ''), '，内容：', a.AppointContent)         , now()         , a.MemberGuid    FROM      memberappoint a    LEFT JOIN k_manager b    ON a.CreatorGuid = b.ManagerGUID    LEFT JOIN k_systemparam c    ON a.AppointWay = c.ID    WHERE      a.MemberAppointGuid = new.MemberAppointGuid;  END IF;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberAppoint_Delete` AFTER DELETE ON `memberappoint` FOR EACH ROW BEGIN  DELETE  FROM    LiftLog  WHERE    DataGuid = old.MemberAppointGuid;END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `memberassess`
--

DROP TABLE IF EXISTS `memberassess`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberassess` (
  `MemberGuid` char(36) NOT NULL COMMENT '会员Guid',
  `IncomeID` int(11) default NULL,
  `HouseID` int(11) default NULL,
  `TransportID` int(11) default NULL,
  `DistanceID` int(11) default NULL,
  `AwarenessID` int(11) default NULL,
  `BrandAcceptID` int(11) default NULL,
  `FamilyAcceptID` int(11) default NULL,
  `IntentionID` int(11) default NULL,
  `AssessGradeID` int(11) default NULL,
  `AssignTime` datetime default NULL,
  PRIMARY KEY  (`MemberGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberassign`
--

DROP TABLE IF EXISTS `memberassign`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberassign` (
  `MemberAssignGuid` char(36) NOT NULL COMMENT '会员分配记录Guid',
  `MemberGuid` char(36) default NULL COMMENT '会员Guid',
  `RelationType` int(11) default NULL COMMENT '关系类型',
  `OperatorGuid` char(36) default NULL COMMENT '操作人Guid',
  `OperateTime` datetime default NULL COMMENT '操作时间',
  `Notes` varchar(200) default NULL COMMENT '备注',
  `OldManagerNames` varchar(200) default NULL,
  `newManagerNames` varchar(200) default NULL,
  `MemberAssignBatchGuid` varchar(36) default NULL COMMENT '学员分配批次关联Guid',
  PRIMARY KEY  (`MemberAssignGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `MemberAssign_Insert` AFTER INSERT ON `memberassign` FOR EACH ROW BEGIN  DECLARE P_MemberGuid     CHAR(36);  DECLARE P_CheckGuid      CHAR(36);  DECLARE P_Count          INT;  DECLARE P_LastAssignTime DATETIME;  SET P_MemberGuid = '';  SET P_CheckGuid = '';  SET P_Count = 0;  SELECT count(*)       , MemberGuid  INTO    P_Count, P_MemberGuid  FROM    memberassign  WHERE    MemberGuid = new.MemberGuid  GROUP BY    memberguid;  SELECT max(operateTime)  INTO    P_LastAssignTime  FROM    memberassign  WHERE    MemberGuid = new.MemberGuid;  IF P_MemberGuid <> '' THEN    SELECT MemberGuid    INTO      P_CheckGuid    FROM      membertemp    WHERE      MemberGuid = P_MemberGuid;    IF P_CheckGuid = '' THEN      INSERT INTO membertemp (MemberGuid, AssignCount, LastAssignTime, FirstFollowTime, LastFollowTime, LastFollowContent, FollowCount, CijinFollowTime, CijinFollowContent) VALUES (P_MemberGuid, P_Count, P_LastAssignTime, '1900-01-01', '1900-01-01', '', 0, '1900-01-01', '');    ELSE      UPDATE membertemp      SET        AssignCount = P_Count, LastAssignTime = P_LastAssignTime      WHERE        MemberGuid = P_MemberGuid;    END IF;  END IF;END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `memberassignbatch`
--

DROP TABLE IF EXISTS `memberassignbatch`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberassignbatch` (
  `MemberAssignBatchGuid` char(36) default NULL,
  `BatchNo` varchar(50) default NULL COMMENT '批次编号',
  `OperatorGuid` char(36) default NULL COMMENT '操作人Guid',
  `OperateTime` datetime default NULL COMMENT '操作时间',
  UNIQUE KEY `BatchNo` (`BatchNo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='学员分配批次表';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `membercard`
--

DROP TABLE IF EXISTS `membercard`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membercard` (
  `MemberCardGuid` char(36) NOT NULL COMMENT '会员-会员卡关系表',
  `MemberGuid` char(36) default NULL,
  `CardGuid` char(36) default NULL,
  PRIMARY KEY  (`MemberCardGuid`),
  KEY `uk_cardguid` (`CardGuid`),
  KEY `uk_memberguid` (`MemberGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `membercourse`
--

DROP TABLE IF EXISTS `membercourse`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membercourse` (
  `MemberCourseGuid` char(36) NOT NULL COMMENT '会员约课Guid',
  `MemberGuid` char(36) default NULL COMMENT '会员Guid',
  `CourseGuid` char(36) default NULL COMMENT '排课Guid',
  `CourseType` int(11) default NULL COMMENT '课程类型：0会员课，1体验课',
  `DoStatus` int(11) default NULL COMMENT '上课状态',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `CreatorGuid` char(36) default NULL COMMENT '创建人Guid',
  `ReduceHours` decimal(18,2) default NULL,
  `Cost` decimal(18,0) default NULL COMMENT '消费金额',
  `IsFixed` int(11) default NULL COMMENT '是否是固定上课',
  `SignTime` datetime default NULL COMMENT '签到时间',
  `CardGuid` char(36) default NULL COMMENT '刷卡扣课',
  `ChangePoints` int(11) default NULL COMMENT '积分增减数目',
  `MakeUp` int(11) default '0',
  `FeedBackInfo` text,
  `SortID` int(11) default NULL,
  `LessonSeriesGuid` char(36) default NULL,
  `pictures` varchar(500) default NULL,
  `ContractNos` varchar(255) default NULL,
  `ReduceGiftClassHours` decimal(6,2) default NULL,
  `ReduceBuyClassHours` decimal(6,2) default NULL,
  `ClassHourType` int(11) default NULL,
  `SumAppointClassHours` decimal(18,2) default NULL,
  `HomeworkStatus` int(11) default NULL,
  PRIMARY KEY  (`MemberCourseGuid`),
  KEY `UK_membercourse` (`CourseGuid`,`MemberGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `WagesByMemberCourse_Insert` AFTER INSERT ON `membercourse` FOR EACH ROW BEGIN  
  INSERT INTO liftlog  SELECT uuid()       , 1       , membercourseguid       , '预约上课'       , concat('预约课程[', ' ', coursedate, ' ', ClassSectionName, ' ', ClassroomName, ']', '班级：', CourseName)       , now()       , MemberGuid  FROM    q_membercourse  WHERE    memberCourseGuid = new.MemberCourseGuid;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `WagesByMemberCourse_Update` AFTER UPDATE ON `membercourse` FOR EACH ROW BEGIN  
  IF old.DoStatus <> new.DoStatus AND new.DoStatus <> 0 THEN    INSERT INTO liftlog    SELECT uuid()         , 1         , MemberCourseGuid         , '上课签到'         , concat('课程[', ' ', CourseDate, ' ', ClassSectionName, ' ', ClassroomName, ']', '班级：', CourseName, '签到', SignStatus)         , now()         , MemberGuid    FROM      q_membercourse    WHERE      MemberCourseGuid = new.MemberCourseGuid;  END IF;  
  IF old.FeedBackInfo <> new.FeedBackInfo THEN    BEGIN      DECLARE P_OpenID, P_CourseName  VARCHAR(100);      DECLARE P_CourseDate            DATETIME;      DECLARE P_MemberGuid            CHAR(36);      SET P_OpenID = '';      SELECT b.CourseDate           , b.CourseName           , c.WXOpenID      INTO        P_CourseDate, P_CourseName, P_OpenID      FROM        memberCourse a      INNER JOIN course b      ON a.CourseGuid = b.CourseGuid      INNER JOIN Member c      ON a.MemberGuid = c.MemberGuid      WHERE        a.MemberCourseGuid = new.MemberCourseGuid;      IF P_OpenID <> '' THEN        DELETE        FROM          wxtemp_feedback        WHERE          MemberCourseGuid = new.MemberCourseGuid          AND DoStatus = 3;        INSERT INTO wxtemp_feedback (MemberCourseGuid, OPenID, CourseDate, CourseName, FeedBackInfo, DoStatus, CreateTime) VALUES (old.MemberCourseGuid, P_OpenID, P_CourseDate, P_CourseName, new.FeedBackInfo, 3, now());      END IF;    END;  END IF;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `WagesByMemberCourse_Delete` AFTER DELETE ON `membercourse` FOR EACH ROW BEGIN  
  DELETE  FROM    liftlog  WHERE    DataGuid = old.memberCourseGuid;  
  DELETE  FROM    wxtemp_feedback  WHERE    membercourseguid = old.MemberCourseGuid;  INSERT INTO wxtemp_feedback (MemberCourseGuid, OPenID, CourseDate, CourseName, FeedBackInfo, DoStatus, CreateTime) VALUES (old.MemberCourseGuid, '', '1900-01-01', '', '', 2, now());END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `membercoursetemp`
--

DROP TABLE IF EXISTS `membercoursetemp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membercoursetemp` (
  `membercoursetempguid` char(36) NOT NULL,
  `membercourseguid` char(36) NOT NULL,
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberdocourse`
--

DROP TABLE IF EXISTS `memberdocourse`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberdocourse` (
  `MemberDoCourseGuid` char(36) NOT NULL COMMENT '会员活动课Guid',
  `MemberGuid` char(36) default NULL COMMENT '会员Guid',
  `DoCourseGuid` char(36) default NULL COMMENT '活动课Guid',
  `DoCourseType` int(11) default NULL COMMENT '课程类型：0会员，1体验',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `ReduceHours` decimal(18,2) default NULL,
  `ReduceCost` int(11) default NULL COMMENT '扣费用',
  `Cost` decimal(18,0) default NULL COMMENT '非会员扣费',
  `ReduceType` int(11) default '0' COMMENT '1:刷卡扣课 2:刷卡扣费',
  `CardGuid` char(36) default NULL COMMENT '刷卡扣课/费',
  `SignTime` datetime default NULL,
  `ChangePoints` int(11) default NULL COMMENT '积分增减数目',
  `LessonSeriesGuid` char(36) default NULL,
  `ContractNos` varchar(255) default NULL,
  `ReduceGiftClassHours` decimal(6,2) default NULL,
  `ReduceBuyClassHours` decimal(6,2) default NULL,
  `WasteBookGuid` char(36) default NULL,
  `PayStatus` int(11) default NULL,
  PRIMARY KEY  (`MemberDoCourseGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberDoCourse_Insert` AFTER INSERT ON `memberdocourse` FOR EACH ROW BEGIN  
  INSERT INTO liftlog  SELECT uuid()       , 2       , new.MemberDoCourseGuid       , '预约活动'       , concat('预约活动主题：', DoTitle, "，活动时间：", StartTime, " - ", EndTime)       , now()       , new.MemberGuid  FROM    docourse  WHERE    DoGuid = new.DoCourseGuid;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`localhost` */ /*!50003 TRIGGER `LiftLogByMemberDoCourse_Update` AFTER UPDATE ON `memberdocourse` FOR EACH ROW BEGIN  
  IF old.DoStatus <> new.DoStatus THEN    INSERT INTO liftlog    SELECT uuid()         , 2         , new.MemberDoCourseGuid         , '活动签到'         , concat('预约活动主题：', DoTitle, "，活动时间：", StartTime, " - ", EndTime)         , now()         , new.MemberGuid    FROM      docourse    WHERE      DoGuid = new.DoCourseGuid;  END IF;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberDoCourse_Delete` AFTER DELETE ON `memberdocourse` FOR EACH ROW BEGIN  DELETE  FROM    liftlog  WHERE    dataguid = old.memberdocourseGuid;END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `memberfamily`
--

DROP TABLE IF EXISTS `memberfamily`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberfamily` (
  `MemberFamilyGuid` char(36) NOT NULL,
  `MemberFamilyCode` varchar(20) NOT NULL COMMENT '学员家庭码',
  `Guardianship` int(11) default NULL COMMENT '监护关系',
  `Guardian` varchar(50) default NULL COMMENT '监护人',
  `MobileLocation` varchar(50) default NULL COMMENT '手机归属',
  `Mobile` varchar(20) NOT NULL COMMENT '手机号',
  PRIMARY KEY  (`MemberFamilyGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberfeedback`
--

DROP TABLE IF EXISTS `memberfeedback`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberfeedback` (
  `FeedbackGuid` char(36) NOT NULL,
  `MemberCourseGuid` char(36) NOT NULL,
  `FeedbackContent` varchar(255) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `MemberGuid` char(36) NOT NULL,
  PRIMARY KEY  (`FeedbackGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberfeedbackpicture`
--

DROP TABLE IF EXISTS `memberfeedbackpicture`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberfeedbackpicture` (
  `PictureGuid` char(36) NOT NULL,
  `FeedbackGuid` char(36) NOT NULL,
  `PictureName` varchar(255) default NULL,
  `OriginalPictureName` varchar(255) default NULL,
  `PicSize` int(11) default NULL,
  `PicPath` varchar(255) default NULL,
  `Remark` varchar(255) default NULL,
  `MemberGuid` char(36) NOT NULL,
  PRIMARY KEY  (`PictureGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberfollow`
--

DROP TABLE IF EXISTS `memberfollow`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberfollow` (
  `MemberFollowGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `FollowContent` varchar(500) default NULL,
  `FollowWay` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` varchar(200) default NULL,
  `DoStatus` int(11) default NULL,
  `MarketNodeGuid` char(36) default NULL,
  `NextFollowTime` datetime default NULL,
  `OperationTime` datetime default NULL COMMENT '操作时间',
  `BatchId` char(36) default NULL COMMENT '导入批次ID',
  PRIMARY KEY  (`MemberFollowGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberhomework`
--

DROP TABLE IF EXISTS `memberhomework`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberhomework` (
  `HomeworkGuid` char(36) NOT NULL,
  `Title` varchar(100) default NULL,
  `MemberCourseGuid` char(36) default NULL,
  `Requirement` longtext,
  `TeacherComment` varchar(500) default NULL,
  `HomeworkResults` longtext,
  `RequirementAttach` varchar(200) default NULL,
  `Deachline` datetime default NULL,
  `HandInTime` datetime default NULL,
  PRIMARY KEY  (`HomeworkGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberlesson`
--

DROP TABLE IF EXISTS `memberlesson`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberlesson` (
  `MemberLessonGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `LessonGuid` char(36) default NULL,
  PRIMARY KEY  (`MemberLessonGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `membermanager`
--

DROP TABLE IF EXISTS `membermanager`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membermanager` (
  `MemberManagerGuid` char(36) NOT NULL,
  `MemberGuid` char(36) NOT NULL,
  `ManagerGuid` char(36) NOT NULL,
  `ManagerType` int(11) default '0' COMMENT '0:顾问 1：老师',
  `Readed` varchar(100) default NULL,
  `ReadTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`MemberManagerGuid`),
  UNIQUE KEY `UK_membermanager_MemberManagerGuid` (`MemberManagerGuid`),
  KEY `IX_membermanager` (`MemberGuid`,`ManagerGuid`),
  KEY `IX_membermanager_ManagerGuid` (`ManagerGuid`),
  KEY `IX_membermanager_MemberGuid` (`MemberGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=172;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `MemberManagerTemp_Insert` AFTER INSERT ON `membermanager` FOR EACH ROW BEGIN  DECLARE P_TempMemberGuid                                 CHAR(36);  DECLARE P_ManagerGuids                                   NVARCHAR(1000);  DECLARE P_ManagerNames, P_AdvisorNames, P_TeacherNames   VARCHAR(1000);  DELETE  FROM    membermanagertemp  WHERE    memberguid = new.memberguid;  SELECT group_concat(a.ManagerGuid)       , group_concat(b.username)  INTO    P_ManagerGuids, P_ManagerNames  FROM    membermanager a  LEFT JOIN k_manager b  ON a.managerguid = b.managerguid  WHERE    a.MemberGuid = new.MemberGuid  GROUP BY    a.memberguid;  SELECT group_concat(b.username)  INTO    P_AdvisorNames  FROM    membermanager a  LEFT JOIN k_manager b  ON a.managerguid = b.managerguid  WHERE    a.managertype = 0    AND a.MemberGuid = new.MemberGuid  GROUP BY    a.memberguid;  SELECT group_concat(b.username)  INTO    P_Teachernames  FROM    membermanager a  LEFT JOIN k_manager b  ON a.managerguid = b.managerguid  WHERE    a.managertype = 1    AND a.MemberGuid = new.MemberGuid  GROUP BY    a.memberguid;  INSERT INTO membermanagertemp VALUES (new.MemberGuid, P_ManagerGuids, P_ManagerNames, P_AdvisorNames, P_TeacherNames);END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `MemberManagerTemp_Delete` AFTER DELETE ON `membermanager` FOR EACH ROW BEGIN  DECLARE P_TempMemberGuid                                 CHAR(36);  DECLARE P_ManagerGuids                                   NVARCHAR(1000);  DECLARE P_ManagerNames, P_AdvisorNames, P_TeacherNames   VARCHAR(1000);  SET P_ManagerGuids = '';  DELETE  FROM    membermanagertemp  WHERE    memberguid = old.memberguid;  SELECT group_concat(a.ManagerGuid)       , group_concat(b.username)  INTO    P_ManagerGuids, P_ManagerNames  FROM    membermanager a  LEFT JOIN k_manager b  ON a.managerguid = b.managerguid  WHERE    a.MemberGuid = old.MemberGuid  GROUP BY    a.memberguid;  SELECT group_concat(b.username)  INTO    P_AdvisorNames  FROM    membermanager a  LEFT JOIN k_manager b  ON a.managerguid = b.managerguid  WHERE    a.managertype = 0    AND a.MemberGuid = old.MemberGuid  GROUP BY    a.memberguid;  SELECT group_concat(b.username)  INTO    P_Teachernames  FROM    membermanager a  LEFT JOIN k_manager b  ON a.managerguid = b.managerguid  WHERE    a.managertype = 1    AND a.MemberGuid = old.MemberGuid  GROUP BY    a.memberguid;  IF P_ManagerGuids <> '' THEN    INSERT INTO membermanagertemp VALUES (old.MemberGuid, P_ManagerGuids, P_ManagerNames, P_AdvisorNames, P_TeacherNames);  END IF;END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `membermanagertemp`
--

DROP TABLE IF EXISTS `membermanagertemp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membermanagertemp` (
  `MemberGuid` char(36) NOT NULL,
  `ManagerGuids` varchar(1000) default NULL,
  `ManagerNames` varchar(200) default NULL,
  `AdvisorNames` varchar(200) default NULL,
  `TeacherNames` varchar(200) default NULL,
  PRIMARY KEY  (`MemberGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=92;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberrecycle`
--

DROP TABLE IF EXISTS `memberrecycle`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberrecycle` (
  `MemberRecycleGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `RecycleTime` datetime default NULL,
  `ClaimTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `Notes` varchar(255) default NULL,
  `OldManagerNames` varchar(200) default NULL,
  `newManagerNames` varchar(200) default NULL,
  PRIMARY KEY  (`MemberRecycleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1220 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberrecyclesetting`
--

DROP TABLE IF EXISTS `memberrecyclesetting`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberrecyclesetting` (
  `SettingGuid` char(36) NOT NULL,
  `Switch` int(11) default '0',
  `MemberDoStatus` varchar(255) default NULL,
  `DayLen` int(11) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`SettingGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1651 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `membersource`
--

DROP TABLE IF EXISTS `membersource`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membersource` (
  `MemberSourceGuid` char(36) NOT NULL,
  `ParentGuid` char(36) default NULL,
  `SourceName` varchar(50) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`MemberSourceGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `membertemp`
--

DROP TABLE IF EXISTS `membertemp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membertemp` (
  `MemberGuid` char(36) NOT NULL,
  `AssignCount` int(11) default NULL,
  `LastAssignTime` datetime default NULL,
  `FirstFollowTime` datetime default NULL,
  `LastFollowTime` datetime default NULL,
  `LastFollowContent` text,
  `FollowCount` int(11) default NULL,
  `CijinFollowTime` datetime default NULL,
  `CijinFollowContent` text,
  `NextFollowTime` datetime default NULL,
  `NowLessonNames` varchar(500) default NULL,
  `NowLessonGuids` varchar(500) default NULL,
  `FirstFollowContent` text,
  `InPublicPool` int(11) default NULL COMMENT '公海状态:0不在公海 ，1-主动放弃进入公海，2-回收进入公海,默认值是0',
  `InPoolTime` datetime default NULL COMMENT '进入公海时间',
  `LastManagerGuid` char(36) default NULL COMMENT '最后放弃人,LastManagerGuid=k_manager.ManagerGUID',
  PRIMARY KEY  (`MemberGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=114;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `memberud`
--

DROP TABLE IF EXISTS `memberud`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `memberud` (
  `MemberGuid_UD` char(36) NOT NULL,
  PRIMARY KEY  (`MemberGuid_UD`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=109;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `membervisit`
--

DROP TABLE IF EXISTS `membervisit`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `membervisit` (
  `MemberVisitGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `VisitTime` datetime default NULL,
  `ConfirmVisitTime` datetime default NULL,
  `VisitContent` varchar(500) default NULL,
  `VisitWay` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` varchar(200) default NULL,
  `DoStatus` int(11) default NULL,
  `MemberCourseGuid` char(36) default NULL,
  `MemberDoCourseGuid` char(36) default NULL,
  PRIMARY KEY  (`MemberVisitGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

/*!50003 SET @SAVE_SQL_MODE=@@SQL_MODE*/;

DELIMITER ;;
/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberVisit_Insert` AFTER INSERT ON `membervisit` FOR EACH ROW BEGIN  
  INSERT INTO liftlog  SELECT uuid()       , 5       , a.MemberVisitGuid       , '客户预约到访'       , concat('跟进人：', b.username, '，预约时间', a.VisitTime)       , now()       , a.MemberGuid  FROM    membervisit a  LEFT JOIN k_manager b  ON a.CreatorGuid = b.ManagerGUID  WHERE    a.MemberVisitGuid = new.MemberVisitGuid;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberVisit_Update` AFTER UPDATE ON `membervisit` FOR EACH ROW BEGIN  IF old.DoStatus <> new.DoStatus THEN    
    INSERT INTO liftlog    SELECT uuid()         , 5         , a.MemberVisitGuid         , '客户预约确认'         , concat('跟进人：', b.UserName, '，预约时间', a.VisitTime, '，到访情况：', a.VisitContent)         , now()         , new.MemberGuid    FROM      membervisit a    LEFT JOIN k_manager b    ON a.CreatorGuid = b.ManagerGUID    WHERE      a.MemberVisitGuid = new.MemberVisitGuid;  END IF;END */;;

/*!50003 SET SESSION SQL_MODE="STRICT_TRANS_TABLES,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION" */;;
/*!50003 CREATE */ /*!50017 DEFINER=`root`@`%` */ /*!50003 TRIGGER `LiftLogByMemberVisit_Delete` AFTER DELETE ON `membervisit` FOR EACH ROW BEGIN  DELETE  FROM    LiftLog  WHERE    DataGuid = old.MemberVisitGuid;END */;;

DELIMITER ;
/*!50003 SET SESSION SQL_MODE=@SAVE_SQL_MODE*/;

--
-- Table structure for table `news`
--

DROP TABLE IF EXISTS `news`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `news` (
  `NewsGuid` char(36) NOT NULL,
  `ServerGuid` char(36) default NULL COMMENT '服务器上保存的记录Guid 用于发送旧信息',
  `Title` varchar(200) default NULL,
  `Description` text,
  `PicUrl` varchar(200) default NULL,
  `Contents` text,
  `CreateTime` datetime default NULL,
  `ManagerGuid` char(36) default NULL,
  `LastTime` datetime default NULL,
  PRIMARY KEY  (`NewsGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=230;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `outstorebill`
--

DROP TABLE IF EXISTS `outstorebill`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `outstorebill` (
  `OutStoreBillGuid` char(36) NOT NULL COMMENT '销售（出库）单据号',
  `MemberGuid` char(36) default NULL COMMENT '会员Guid',
  `BillNo` varchar(50) default NULL COMMENT '单据号',
  `BillAmount` decimal(18,2) default NULL COMMENT '单据金额',
  `OutStoreDate` datetime default NULL COMMENT '出库日期',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `Notes` varchar(200) default NULL COMMENT '备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `CardGuid` char(36) default NULL,
  `RefundAmount` decimal(18,2) default NULL,
  `IsExpres` bit(1) default NULL,
  `ExpressDate` datetime default NULL,
  `PackForMemberGuid` varchar(36) default NULL,
  `ExpressName` varchar(230) default NULL,
  `ExpressNo` varchar(230) default NULL,
  `ExpressSender` varchar(330) default NULL,
  `ExpressSenderMobile` varchar(330) default NULL,
  `ExpressSenderAddress` varchar(330) default NULL,
  `ExpressSenderPhone` varchar(330) default NULL,
  `ExpressReceiver` varchar(330) default NULL,
  `ExpressReceiverMobile` varchar(330) default NULL,
  `ExpressReceiverAddress` varchar(330) default NULL,
  `ExpressReceiverPhone` varchar(330) default NULL,
  `ExpressNote` varchar(430) default NULL,
  `ExpressOperator` varchar(36) default NULL,
  `NeedExpress` bit(1) default NULL,
  `IsPosPay` int(11) default '0',
  `PosPayAmount` decimal(18,2) default '0.00',
  `ChangePoints` int(11) default NULL,
  `PayStatus` int(11) default '1',
  `OpenId` varchar(200) default NULL,
  PRIMARY KEY  (`OutStoreBillGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `outstorebilllist`
--

DROP TABLE IF EXISTS `outstorebilllist`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `outstorebilllist` (
  `BillItemGuid` char(36) NOT NULL COMMENT '销售（出库）单据清单项',
  `OutStoreBillGuid` char(36) default NULL COMMENT '出库单Guid',
  `ProductGuid` char(36) default NULL COMMENT '商品Guid',
  `SalePrice` decimal(18,2) default NULL COMMENT '销售单价',
  `Amount` int(11) default NULL COMMENT '数量',
  `StorehouseGuid` char(36) default NULL,
  `DepreciationGuid` char(36) default NULL,
  `Discount` decimal(10,2) default NULL,
  `IsPack` bit(1) default NULL,
  `IsExpres` bit(1) default NULL,
  `ExpressDate` datetime default NULL,
  `PackForMemberGuid` varchar(36) default NULL,
  `ExpressName` varchar(230) default NULL,
  `ExpressNo` varchar(230) default NULL,
  `ExpressSender` varchar(330) default NULL,
  `ExpressSenderMobile` varchar(330) default NULL,
  `ExpressSenderAddress` varchar(330) default NULL,
  `ExpressSenderPhone` varchar(330) default NULL,
  `ExpressReceiver` varchar(330) default NULL,
  `ExpressReceiverMobile` varchar(330) default NULL,
  `ExpressReceiverAddress` varchar(330) default NULL,
  `ExpressReceiverPhone` varchar(330) default NULL,
  `ExpressNote` varchar(430) default NULL,
  `ExpressOperator` varchar(36) default NULL,
  PRIMARY KEY  (`BillItemGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `outstoreproductpackitem`
--

DROP TABLE IF EXISTS `outstoreproductpackitem`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `outstoreproductpackitem` (
  `ProductPackItemGuid` varchar(36) NOT NULL,
  `ProductPackGuid` varchar(36) default NULL,
  `ProductGuid` varchar(36) default NULL,
  `ProductCount` int(11) default NULL,
  `ProductPackItemIndex` int(11) default NULL,
  `ProductPackItemInterval` int(11) default NULL,
  `ProductPackItemDate` datetime default NULL,
  `IsExpres` bit(1) default NULL,
  `ExpressDate` datetime default NULL,
  `PackForMemberGuid` varchar(36) default NULL,
  `ExpressName` varchar(230) default NULL,
  `ExpressNo` varchar(230) default NULL,
  `ExpressSender` varchar(330) default NULL,
  `ExpressSenderMobile` varchar(330) default NULL,
  `ExpressSenderAddress` varchar(330) default NULL,
  `ExpressSenderPhone` varchar(330) default NULL,
  `ExpressReceiver` varchar(330) default NULL,
  `ExpressReceiverMobile` varchar(330) default NULL,
  `ExpressReceiverAddress` varchar(330) default NULL,
  `ExpressReceiverPhone` varchar(330) default NULL,
  `ExpressNote` varchar(430) default NULL,
  `ExpressOperator` varchar(36) default NULL,
  `OutStoreBillGuid` varchar(36) default NULL,
  PRIMARY KEY  (`ProductPackItemGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `pageusercolumn`
--

DROP TABLE IF EXISTS `pageusercolumn`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `pageusercolumn` (
  `PageUserColumnGuid` char(36) NOT NULL,
  `ColumnS` text,
  `PageName` varchar(150) default NULL,
  `ManagerGUID` char(36) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=1170;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `paramconfig`
--

DROP TABLE IF EXISTS `paramconfig`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `paramconfig` (
  `ParamGuid` char(36) NOT NULL COMMENT '参数表[新]',
  `ParamName` varchar(50) default NULL COMMENT '参数名称',
  `ParamValue` varchar(50) default NULL COMMENT '参数值',
  `ParentGuid` char(36) NOT NULL COMMENT '上级ID',
  `ParamType` int(11) default NULL COMMENT '参数类型：0 自定义参数，1 系统参数',
  `SortID` int(11) default NULL COMMENT '排序',
  PRIMARY KEY  (`ParamGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `paymentrecord`
--

DROP TABLE IF EXISTS `paymentrecord`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `paymentrecord` (
  `PaymentRecordGuid` char(36) NOT NULL,
  `OrderGuid` char(255) default NULL,
  `OrderNum` varchar(50) default NULL,
  `OrderType` int(50) default NULL,
  `Amount` decimal(10,2) default NULL,
  `PayAccountName` varchar(50) NOT NULL,
  `PaymentPlatformOrderNum` varchar(50) default NULL,
  `PaymentChannelID` int(11) default NULL,
  `PaymentChannelName` varchar(50) default NULL,
  `PayTime` datetime default NULL,
  `PayStatus` int(11) default NULL,
  PRIMARY KEY  (`PaymentRecordGuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `pointchange`
--

DROP TABLE IF EXISTS `pointchange`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `pointchange` (
  `PointChangeGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `ChangeAmount` int(11) default NULL,
  `ChangeScope` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` varchar(255) default NULL,
  `Notes` text,
  `ChangeType` int(11) default NULL,
  `RealTime` datetime default NULL,
  `RGuid` char(36) default '00000000-0000-0000-0000-000000000000',
  PRIMARY KEY  (`PointChangeGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=132;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `pointrule`
--

DROP TABLE IF EXISTS `pointrule`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `pointrule` (
  `PointRuleGuid` char(36) NOT NULL COMMENT '积分规则表',
  `WhichDayOfWeek` varchar(50) default NULL COMMENT '周几',
  `WhichPeriod` varchar(50) default NULL COMMENT '时段：上午am、下午pm',
  `GivePoints` int(11) default NULL COMMENT '赠送积分数',
  `ReducePoints` int(11) default NULL COMMENT '扣减积分数',
  PRIMARY KEY  (`PointRuleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `pointrule_d`
--

DROP TABLE IF EXISTS `pointrule_d`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `pointrule_d` (
  `PointRuleGuid` char(36) NOT NULL,
  `PointRuleName` varchar(200) default NULL,
  `Amount` int(11) default NULL,
  `Points` int(11) default NULL,
  `SortID` int(11) default NULL,
  `CategoryGuid` char(36) default NULL,
  `Notes` text,
  PRIMARY KEY  (`PointRuleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `pointuserule`
--

DROP TABLE IF EXISTS `pointuserule`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `pointuserule` (
  `CourseStatus` int(11) NOT NULL COMMENT '上课状态',
  `UseSetting` int(11) default NULL COMMENT '使用设定：0积分不变，1赠送积分，2扣减积分',
  PRIMARY KEY  (`CourseStatus`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `posdatatemp`
--

DROP TABLE IF EXISTS `posdatatemp`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `posdatatemp` (
  `PosGuid` char(36) default NULL,
  `RelateItemGuid` char(36) NOT NULL,
  `RelateItemNo` varchar(100) default NULL,
  `TransType` varchar(100) default NULL,
  `TransAmount` decimal(10,2) default NULL,
  `Notes` varchar(200) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`RelateItemGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=124;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `posflow`
--

DROP TABLE IF EXISTS `posflow`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `posflow` (
  `PosFlowGuid` char(36) NOT NULL,
  `RelatedItemGuid` char(36) default NULL,
  `RelateItemNo` varchar(200) default NULL,
  `TransType` varchar(100) default NULL,
  `TransAmount` decimal(10,2) default NULL,
  `TransTime` datetime default NULL,
  `Notes` varchar(200) default NULL,
  `CreatorName` varchar(100) default NULL,
  `CreateGuid` char(36) default NULL,
  PRIMARY KEY  (`PosFlowGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=158;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `position`
--

DROP TABLE IF EXISTS `position`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `position` (
  `PositionGuid` char(36) NOT NULL,
  `PositionName` varchar(50) NOT NULL,
  `ParentGuid` char(36) default NULL,
  `SortID` int(11) default NULL,
  `Notes` varchar(100) default NULL,
  PRIMARY KEY  (`PositionGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `poslicence`
--

DROP TABLE IF EXISTS `poslicence`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `poslicence` (
  `PosLicenceGuid` char(36) NOT NULL,
  `ManagerGuid` char(36) default NULL,
  `Licence` varchar(255) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`PosLicenceGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=120;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `printmodel`
--

DROP TABLE IF EXISTS `printmodel`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `printmodel` (
  `PrintModelGuid` char(36) NOT NULL,
  `PrintModelName` varchar(255) default NULL,
  `DefaultContent` text,
  `PrintContent` text,
  `printparam` varchar(1000) default NULL,
  `ModifyUserGuid` char(36) default NULL,
  `ModifyTime` datetime default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`PrintModelGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=6940;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `product` (
  `ProductGuid` char(36) NOT NULL,
  `ProductName` varchar(50) default NULL COMMENT '商品名称',
  `ProductCode` varchar(50) default NULL COMMENT '商品编码',
  `ProductCategoryGuid` char(36) default NULL COMMENT '商品分类Guid',
  `PurchasePrice` decimal(18,2) default NULL COMMENT '采购价',
  `SalePrice` decimal(18,2) default NULL COMMENT '零售价',
  `InventoryAmount` int(11) default NULL COMMENT '库存量',
  `CanExchangePoint` int(11) default NULL COMMENT '是否可兑换积分',
  `ExchangePoints` int(11) default NULL COMMENT '兑换积分数目',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `Notes` longtext COMMENT '商品备注',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `ImgPath` varchar(200) default NULL,
  `Discount` varchar(500) default NULL,
  `ISMallProduct` int(11) default NULL,
  `ImportBatchGuid` char(36) default NULL,
  `IsPack` bit(1) default NULL,
  PRIMARY KEY  (`ProductGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productapply`
--

DROP TABLE IF EXISTS `productapply`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productapply` (
  `ProductApplyGuid` char(36) NOT NULL default '',
  `ApplicantGuid` char(36) default NULL,
  `ApplyTime` datetime default NULL,
  `AuditorGuid` char(36) default NULL,
  `AuditTime` datetime default NULL,
  `ReceiverGuid` char(36) default NULL,
  `ReceiveTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  `Notes` varchar(500) default NULL,
  PRIMARY KEY  (`ProductApplyGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=232;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productapplylist`
--

DROP TABLE IF EXISTS `productapplylist`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productapplylist` (
  `ProductApplyListGuid` char(36) NOT NULL default '',
  `ProductApplyGuid` char(36) default NULL,
  `ProductGuid` char(36) default NULL,
  `NeedNum` int(11) default NULL,
  PRIMARY KEY  (`ProductApplyListGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=329;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productcategory`
--

DROP TABLE IF EXISTS `productcategory`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productcategory` (
  `ProductCategoryGuid` char(36) NOT NULL,
  `CategoryName` varchar(50) default NULL COMMENT '商品分类名称',
  `CategoryCode` varchar(50) default NULL COMMENT '商品分类编码',
  `ParentGuid` char(36) default NULL,
  `SortID` int(11) default NULL COMMENT '排序',
  `DoStatus` int(11) default NULL COMMENT '状态',
  PRIMARY KEY  (`ProductCategoryGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productimg`
--

DROP TABLE IF EXISTS `productimg`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productimg` (
  `ImgGuid` char(36) NOT NULL,
  `ProductGuid` char(36) default NULL,
  `ImgPath` varchar(300) default NULL,
  `ImgTitle` varchar(50) default NULL,
  `ImgType` int(11) default NULL,
  `SortId` int(11) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`ImgGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productimport`
--

DROP TABLE IF EXISTS `productimport`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productimport` (
  `BatchGuid` char(36) NOT NULL,
  `BatchTitle` varchar(50) default NULL,
  `ImportFrom` int(11) default NULL,
  `ImportTime` datetime default NULL,
  `ImportCount` int(11) default NULL,
  `SuccCount` int(11) default NULL,
  `RepeatCount` int(11) default NULL,
  `OtherCount` int(11) default NULL,
  `CreatorGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`BatchGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productimportfail`
--

DROP TABLE IF EXISTS `productimportfail`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productimportfail` (
  `FailGuid` char(36) NOT NULL,
  `ProductCode` varchar(50) default NULL,
  `ProductName` varchar(50) default NULL,
  `ProductCategory` varchar(50) default NULL,
  `InventoryAmount` varchar(50) default NULL,
  `PurchasePrice` varchar(50) default NULL,
  `SalePrice` varchar(50) default NULL,
  `Discount` varchar(50) default NULL,
  `CanExchangePoint` varchar(50) default NULL,
  `ExchangePoints` varchar(50) default NULL,
  `Notes` varchar(2000) default NULL,
  `IsMall` int(11) default NULL,
  `Reason` varchar(255) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  PRIMARY KEY  (`FailGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productinstore`
--

DROP TABLE IF EXISTS `productinstore`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productinstore` (
  `InStoreGuid` char(36) NOT NULL,
  `ProductGuid` char(36) default NULL,
  `PurchasePrice` decimal(18,2) default NULL,
  `Amount` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Notes` varchar(200) default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`InStoreGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productpackitem`
--

DROP TABLE IF EXISTS `productpackitem`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productpackitem` (
  `ProductPackItemGuid` varchar(36) NOT NULL,
  `ProductPackGuid` varchar(36) default NULL,
  `ProductGuid` varchar(36) default NULL,
  `ProductCount` int(11) default NULL,
  `ProductPackItemIndex` int(11) default NULL,
  `ProductPackItemInterval` int(11) default NULL,
  PRIMARY KEY  (`ProductPackItemGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `productrent`
--

DROP TABLE IF EXISTS `productrent`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `productrent` (
  `RentGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `RentBillNo` varchar(50) default NULL,
  `ProductGuid` char(36) default NULL,
  `StorehouseGuid` char(36) default NULL,
  `DepreciationGuid` char(36) default NULL,
  `StartTime` datetime default NULL,
  `EndTime` datetime default NULL,
  `RentCount` int(11) default NULL,
  `RentAmount` decimal(18,2) default NULL,
  `DepositAmount` decimal(18,2) default NULL,
  `ReturnAmount` decimal(18,2) default NULL,
  `ReturnTime` datetime default NULL,
  `Notes` varchar(300) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`RentGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `prorefdexch`
--

DROP TABLE IF EXISTS `prorefdexch`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `prorefdexch` (
  `RefdExchGuid` char(36) NOT NULL,
  `MemberGuid` char(36) default NULL,
  `OutStoreBillGuid` char(36) default NULL,
  `ProductGuid` char(36) default NULL,
  `StorehouseGuid` char(36) default NULL,
  `DepreciationGuid` char(36) default NULL,
  `RefundCount` int(11) default NULL,
  `RefundAmount` decimal(18,2) default NULL,
  `ExchangeCount` int(11) default NULL,
  `Notes` varchar(200) default NULL,
  `DoStatus` int(11) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  PRIMARY KEY  (`RefdExchGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `publicpoollog`
--

DROP TABLE IF EXISTS `publicpoollog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `publicpoollog` (
  `LogGuid` char(36) NOT NULL COMMENT '公海操作ID',
  `OperateType` int(11) NOT NULL COMMENT '操作类:0放弃，1领取，2回收',
  `Operator` char(36) NOT NULL COMMENT '操作人(回收的操作人标记为系统回收)',
  `OperateTime` datetime NOT NULL COMMENT '操作时间',
  `MemberGuid` char(36) NOT NULL COMMENT '会员Guid',
  PRIMARY KEY  (`LogGuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `purchasebill`
--

DROP TABLE IF EXISTS `purchasebill`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `purchasebill` (
  `PurchaseBillGuid` char(36) NOT NULL,
  `BillNo` varchar(255) default NULL,
  `Amount` decimal(10,2) default '0.00',
  `Department` char(36) default NULL,
  `BuyDate` datetime default NULL,
  `BuyUserGuid` char(36) default NULL,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `InStoreBillGuid` char(36) default NULL,
  `InStoreTime` datetime default NULL,
  `InStoreUserGuid` char(36) default NULL,
  `CheckUserGuid` char(36) default NULL,
  `CheckTime` datetime default NULL,
  `DoStatus` int(11) default '0',
  `Reason` varchar(255) default NULL,
  `Notes` varchar(255) default NULL,
  PRIMARY KEY  (`PurchaseBillGuid`),
  UNIQUE KEY `BillNo` (`BillNo`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=320;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `purchasebilllist`
--

DROP TABLE IF EXISTS `purchasebilllist`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `purchasebilllist` (
  `PurchaseBillListGuid` char(36) NOT NULL,
  `PurchaseBillGuid` char(36) default NULL,
  `ProductGuid` char(36) default NULL,
  `Price` decimal(10,2) default '0.00',
  `ProductCount` int(11) default '0',
  `Amount` decimal(10,2) default '0.00',
  `StoreHouseGuid` char(36) default NULL,
  `Notes` varchar(255) default NULL,
  `Notes1` varchar(255) default NULL,
  PRIMARY KEY  (`PurchaseBillListGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=172;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `q_card`
--

DROP TABLE IF EXISTS `q_card`;
/*!50001 DROP VIEW IF EXISTS `q_card`*/;
/*!50001 CREATE TABLE `q_card` (
  `CardGuid` char(36),
  `CardNo` varchar(50),
  `Amount` decimal(18,2),
  `CardTypeGuid` char(36),
  `LeaveDays` int(11),
  `EffectiveDuration` int(11),
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `DoStatus` int(11),
  `Notes` varchar(200),
  `MainCardGuid` char(36),
  `UseType` int(11),
  `StopDate` datetime,
  `CardTypeName` varchar(50),
  `malldiscount` decimal(10,2),
  `MemberGuid` char(36),
  `RealName` varchar(50),
  `Nickname` varchar(50),
  `Guardian` varchar(50),
  `Sex` varchar(10),
  `BirthDate` datetime,
  `Mobile` varchar(50),
  `MemberStatus` int(11),
  `CreatorName` varchar(50),
  `CardType` varchar(7)
) */;

--
-- Temporary table structure for view `q_cardclasshours`
--

DROP TABLE IF EXISTS `q_cardclasshours`;
/*!50001 DROP VIEW IF EXISTS `q_cardclasshours`*/;
/*!50001 CREATE TABLE `q_cardclasshours` (
  `CardGuid` char(36),
  `CurrentClassHours` decimal(10,2)
) */;

--
-- Temporary table structure for view `q_cardflow`
--

DROP TABLE IF EXISTS `q_cardflow`;
/*!50001 DROP VIEW IF EXISTS `q_cardflow`*/;
/*!50001 CREATE TABLE `q_cardflow` (
  `CardGuid` char(36),
  `CardNo` varchar(50),
  `MemberGuid` char(36),
  `RealName` varchar(50),
  `Mobile` varchar(50),
  `CostContent` varchar(255),
  `CostType` varchar(4),
  `ChangeClassHours` varchar(8),
  `CardType` varchar(7),
  `CostTime` datetime,
  `MemberStatus` int(11)
) */;

--
-- Temporary table structure for view `q_cardpackage`
--

DROP TABLE IF EXISTS `q_cardpackage`;
/*!50001 DROP VIEW IF EXISTS `q_cardpackage`*/;
/*!50001 CREATE TABLE `q_cardpackage` (
  `CardGuid` char(36),
  `LessonSeriesGuid` char(36),
  `CurrentClassHours` decimal(10,2),
  `Notes` varchar(255),
  `CardNo` varchar(50),
  `CardType` varchar(7),
  `LessonSeriesName` varchar(50)
) */;

--
-- Temporary table structure for view `q_cardpackage_154`
--

DROP TABLE IF EXISTS `q_cardpackage_154`;
/*!50001 DROP VIEW IF EXISTS `q_cardpackage_154`*/;
/*!50001 CREATE TABLE `q_cardpackage_154` (
  `CardGuid` char(36),
  `LessonSeriesGuid` char(36),
  `CurrentClassHours` decimal(10,2),
  `LessonSeriesName` varchar(50)
) */;

--
-- Temporary table structure for view `q_cardtransform`
--

DROP TABLE IF EXISTS `q_cardtransform`;
/*!50001 DROP VIEW IF EXISTS `q_cardtransform`*/;
/*!50001 CREATE TABLE `q_cardtransform` (
  `CardGuid` char(36),
  `CreateTime` datetime,
  `Flow` varchar(19),
  `CardNo` varchar(50),
  `CardType` varchar(7),
  `RealName` varchar(50),
  `Nickname` varchar(50),
  `Amount` decimal(18,2),
  `Guardian` varchar(50),
  `CreatorName` varchar(50),
  `CardTypeName` varchar(50),
  `MemberGuid` char(36),
  `Mobile` varchar(50),
  `MemberStatus` int(11)
) */;

--
-- Temporary table structure for view `q_contract`
--

DROP TABLE IF EXISTS `q_contract`;
/*!50001 DROP VIEW IF EXISTS `q_contract`*/;
/*!50001 CREATE TABLE `q_contract` (
  `ContractGuid` char(36),
  `ContractNum` varchar(50),
  `MemberGuid` char(36),
  `ClassHourName` varchar(50),
  `ClassHours` decimal(18,2),
  `amount` decimal(18,2),
  `LeaveDays` int(11),
  `StartDate` datetime,
  `EndDate` datetime,
  `SignDate` datetime,
  `Attachment` varchar(200),
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `Notes` varchar(200),
  `RefundNotes` varchar(200),
  `DiscardNotes` varchar(200),
  `DoStatus` int(11),
  `ContractType` int(11),
  `LastDoTime` datetime,
  `SalemanGuid` char(36),
  `YAmount` decimal(18,2),
  `ComboType` int(11),
  `ContractDepositGuid` char(36),
  `CheckUserGuid` char(36),
  `CheckDate` datetime,
  `CheckNotes` text,
  `PayTypeName` varchar(200),
  `IsPosPay` int(11),
  `PosPayAmount` decimal(18,2),
  `Discount` decimal(18,2),
  `ChangePoints` int(11),
  `Saleman2Guid` char(36),
  `BuyClassHours` decimal(10,2),
  `GiftClassHours` decimal(10,2),
  `AverageMode` int(11),
  `IsNewMode` int(11),
  `PayStatus` int(11),
  `CLevel` int(11),
  `Duration` int(11),
  `Frequency` int(11),
  `ClassPeriod` int(11),
  `CourseSeries` int(11),
  `SalemanShare` decimal(18,2),
  `Saleman2Share` decimal(18,2),
  `SalemanName` varchar(50),
  `Saleman2Name` varchar(50),
  `CreatorName` varchar(50),
  `BabyName` varchar(50),
  `Mobile` varchar(50),
  `ManagerGuids` varchar(1000),
  `ManagerNames` varchar(200),
  `advisornames` varchar(200),
  `teachernames` varchar(200),
  `ContractStatus` varchar(50),
  `ContractTypeName` varchar(50),
  `MemberStatus` int(11),
  `CheckUserName` varchar(50),
  `DepositAmount` decimal(10,2),
  `DepositPayType` varchar(200),
  `ContractLeftDays` int(8)
) */;

--
-- Temporary table structure for view `q_course`
--

DROP TABLE IF EXISTS `q_course`;
/*!50001 DROP VIEW IF EXISTS `q_course`*/;
/*!50001 CREATE TABLE `q_course` (
  `CourseGuid` char(36),
  `CourseName` varchar(50),
  `CourseDate` datetime,
  `ClassSectionGuid` char(36),
  `ClassroomGuid` char(36),
  `LessonGuid` char(36),
  `Teacher` varchar(500),
  `Assistant` varchar(500),
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `ShowColor` varchar(50),
  `ClassroomName` varchar(50),
  `ClassSectionName` varchar(50),
  `StartTime` varchar(50),
  `EndTime` varchar(50),
  `ClassSectionTime` varchar(101),
  `MemberCount` int(11),
  `FreeCount` int(11),
  `ClassHours` decimal(18,2),
  `Price` decimal(18,2),
  `LessonName` varchar(50),
  `FitAgeFrom` int(11),
  `FitAgeTo` int(11),
  `LessonSeriesName` varchar(50)
) */;

--
-- Temporary table structure for view `q_courseanddocourseautosendmsg`
--

DROP TABLE IF EXISTS `q_courseanddocourseautosendmsg`;
/*!50001 DROP VIEW IF EXISTS `q_courseanddocourseautosendmsg`*/;
/*!50001 CREATE TABLE `q_courseanddocourseautosendmsg` (
  `CourseDate` datetime,
  `StartTime` varchar(50),
  `Mobile` varchar(50),
  `LessonName` varchar(50),
  `ClassSectionName` varchar(50),
  `ClassroomName` varchar(50),
  `RealName` varchar(50),
  `Nickname` varchar(50),
  `Guardian` varchar(50),
  `TimeLen` varchar(50),
  `Type` varchar(6),
  `CourseStartTime` datetime
) */;

--
-- Temporary table structure for view `q_coursedayreport`
--

DROP TABLE IF EXISTS `q_coursedayreport`;
/*!50001 DROP VIEW IF EXISTS `q_coursedayreport`*/;
/*!50001 CREATE TABLE `q_coursedayreport` (
  `CourseGuid` char(36),
  `CourseDate` varchar(10),
  `weekDay` varchar(3),
  `TimeSpan` varchar(101),
  `ClassroomName` varchar(50),
  `CourseName` varchar(50),
  `LessonName` varchar(50),
  `TeacherName` varchar(500),
  `AssistantName` varchar(500),
  `ClassHours` decimal(18,2),
  `YYHY` bigint(21),
  `SJSKHY` bigint(21),
  `YYTY` bigint(21),
  `SJTY` bigint(21),
  `QingJia` bigint(21),
  `KuangKe` bigint(21),
  `cql` varchar(21),
  `hycql` varchar(21)
) */;

--
-- Temporary table structure for view `q_coursedayreport_sub`
--

DROP TABLE IF EXISTS `q_coursedayreport_sub`;
/*!50001 DROP VIEW IF EXISTS `q_coursedayreport_sub`*/;
/*!50001 CREATE TABLE `q_coursedayreport_sub` (
  `CourseGuid` char(36),
  `c` bigint(21),
  `seltype` varchar(7)
) */;

--
-- Temporary table structure for view `q_courselist`
--

DROP TABLE IF EXISTS `q_courselist`;
/*!50001 DROP VIEW IF EXISTS `q_courselist`*/;
/*!50001 CREATE TABLE `q_courselist` (
  `CourseListGuid` char(36),
  `MemberGuid` char(36),
  `WaitType` int(11),
  `WaitCourseGuid` char(36),
  `WaitLessonGuid` char(36),
  `sortid` int(11),
  `coursetype` int(11),
  `CourseGuid` char(36),
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `DoStatus` int(11),
  `Notes` varchar(300),
  `membername` varchar(50),
  `Nickname` varchar(50),
  `BirthDate` datetime,
  `Guardian` varchar(50),
  `Mobile` varchar(50),
  `MemberDoStatus` int(11),
  `WCourseDate` datetime,
  `WClassSectionTime` varchar(101),
  `WClassroomName` varchar(50),
  `WLessonName` varchar(50),
  `WaitLessonName` varchar(50),
  `RCourseDate` datetime,
  `RClassSectionTime` varchar(101),
  `RClassroomName` varchar(50),
  `RLessonName` varchar(50),
  `CreatorName` varchar(50)
) */;

--
-- Temporary table structure for view `q_docourse`
--

DROP TABLE IF EXISTS `q_docourse`;
/*!50001 DROP VIEW IF EXISTS `q_docourse`*/;
/*!50001 CREATE TABLE `q_docourse` (
  `DoGuid` char(36),
  `DoTypeGuid` char(36),
  `DoTitle` varchar(255),
  `DoContent` text,
  `StartTime` varchar(50),
  `EndTime` varchar(50),
  `DoProperties` int(11),
  `ReduceHours` decimal(18,2),
  `ReduceCost` int(11),
  `Cost` int(11),
  `ClassroomGuid` char(36),
  `Address` varchar(300),
  `TeacherGuid` char(36),
  `AssistantGuid` char(36),
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `LessonSeriesGuids` char(36),
  `MemberCount` int(11),
  `Notes` text,
  `Notes1` text,
  `Notes2` text,
  `Pictures` varchar(500),
  `WxLimit` int(11),
  `PayType` int(11),
  `dotypename` varchar(50),
  `ClassroomName` varchar(50),
  `TeacherName` varchar(50),
  `AssistantName` varchar(50),
  `CreatorName` varchar(50),
  `DoBudget` decimal(18,2),
  `DoIncome` decimal(18,2),
  `ManagerGuids` varchar(300),
  `ManagerNames` varchar(100),
  `membernum` bigint(21),
  `sign` decimal(32,0),
  `charge` decimal(41,0),
  `ReduceHoursCount` decimal(40,2)
) */;

--
-- Temporary table structure for view `q_docoursemember`
--

DROP TABLE IF EXISTS `q_docoursemember`;
/*!50001 DROP VIEW IF EXISTS `q_docoursemember`*/;
/*!50001 CREATE TABLE `q_docoursemember` (
  `DoCourseGuid` char(36),
  `membernum` bigint(21),
  `sign` decimal(32,0),
  `charge` decimal(41,0),
  `ReduceHoursCount` decimal(40,2)
) */;

--
-- Temporary table structure for view `q_leave`
--

DROP TABLE IF EXISTS `q_leave`;
/*!50001 DROP VIEW IF EXISTS `q_leave`*/;
/*!50001 CREATE TABLE `q_leave` (
  `LeaveGuid` char(36),
  `MemberGuid` char(36),
  `CourseGuid` char(36),
  `LeaveType` int(11),
  `Reason` text,
  `StartTime` datetime,
  `EndTime` datetime,
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `Note` varchar(100),
  `CreatorName` varchar(50),
  `RealName` varchar(50),
  `Nickname` varchar(50),
  `Guardian` varchar(50),
  `Sex` varchar(10),
  `BirthDate` datetime,
  `Mobile` varchar(50),
  `CourseName` varchar(50),
  `CourseDate` datetime,
  `LessonName` varchar(50),
  `ClassSectionTime` varchar(101),
  `ClassroomName` varchar(50),
  `LessonGuid` char(36),
  `ReduceHours` decimal(18,2),
  `CourseType` int(11),
  `DoStatus` int(11),
  `SignStatus` varchar(50),
  `MemberStatus` varchar(50)
) */;

--
-- Temporary table structure for view `q_member`
--

DROP TABLE IF EXISTS `q_member`;
/*!50001 DROP VIEW IF EXISTS `q_member`*/;
/*!50001 CREATE TABLE `q_member` (
  `ID` bigint(20),
  `MemberGuid` char(36),
  `RealName` varchar(50),
  `NickName` varchar(50),
  `Guardianship` int(11),
  `Guardian` varchar(50),
  `Sex` varchar(10),
  `BirthDate` datetime,
  `Address` text,
  `Phone` varchar(50),
  `Mobile` varchar(50),
  `Mobile1` varchar(50),
  `Msn` varchar(50),
  `QQ` varchar(50),
  `Email` varchar(50),
  `Photo` text,
  `FacePhoto` varchar(2000),
  `UnRecognizeFacePhoto` int(11),
  `BasicInfo` text,
  `VisitInfo` text,
  `ExperienceInfo` text,
  `CurrentLevel` varchar(50),
  `Scope` decimal(18,0),
  `IsVisited` int(11),
  `SignDate` datetime,
  `AreaGuid` char(36),
  `intentiondate` datetime,
  `MemberType` int(11),
  `ConvertCycle` int(7),
  `Notes` text,
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `DoStatus` int(11),
  `SourceGuid` char(36),
  `BirthMode` int(11),
  `consultingGuid` char(36),
  `ImportBatchGuid` char(36),
  `MktStaffGuid` char(36),
  `IntentionLesson` varchar(100),
  `ImportantLevel` char(36),
  `LastCourseDate` datetime,
  `MarketNodeGuid` char(36),
  `Marks` varchar(2000),
  `managerguids` varchar(1000),
  `managernames` varchar(200),
  `advisornames` varchar(200),
  `teachernames` varchar(200),
  `ExperienceDate` datetime,
  `VisitDate` datetime,
  `IsExperienced` int(11),
  `WXUserName` varchar(200),
  `WXOpenID` varchar(200),
  `MobileLocation` varchar(200),
  `NodeName` varchar(50),
  `MemberStatus` varchar(50),
  `SourceName` varchar(50),
  `ImportantLevelName` varchar(50),
  `MktStaffName` varchar(50),
  `BatchTitle` varchar(50),
  `AssignCount` int(11),
  `LastAssignTime` datetime,
  `FirstFollowTime` datetime,
  `LastFollowTime` datetime,
  `LastFollowContent` text,
  `FollowCount` int(11),
  `CijinFollowTime` datetime,
  `CijinFollowContent` text,
  `NextFollowTime` datetime,
  `NowLessonNames` varchar(500),
  `NowLessonGuids` varchar(500),
  `FirstFollowContent` text
) */;

--
-- Temporary table structure for view `q_memberassign`
--

DROP TABLE IF EXISTS `q_memberassign`;
/*!50001 DROP VIEW IF EXISTS `q_memberassign`*/;
/*!50001 CREATE TABLE `q_memberassign` (
  `MemberAssignGuid` char(36),
  `MemberGuid` char(36),
  `ID` bigint(20),
  `RelationType` int(11),
  `OperatorGuid` char(36),
  `OperateTime` datetime,
  `Notes` varchar(200),
  `RealName` varchar(50),
  `Guardian` varchar(50),
  `Mobile` varchar(50),
  `OperatorName` varchar(50),
  `OldManagerNames` varchar(200),
  `NewManagerNames` varchar(200),
  `Sex` varchar(10),
  `MemberAssignBatchGuid` varchar(36)
) */;

--
-- Temporary table structure for view `q_memberclasshours`
--

DROP TABLE IF EXISTS `q_memberclasshours`;
/*!50001 DROP VIEW IF EXISTS `q_memberclasshours`*/;
/*!50001 CREATE TABLE `q_memberclasshours` (
  `MemberGuid` char(36),
  `CurrentClassHours` decimal(32,2)
) */;

--
-- Temporary table structure for view `q_membercourse`
--

DROP TABLE IF EXISTS `q_membercourse`;
/*!50001 DROP VIEW IF EXISTS `q_membercourse`*/;
/*!50001 CREATE TABLE `q_membercourse` (
  `MemberCourseGuid` char(36),
  `MemberGuid` char(36),
  `CourseGuid` char(36),
  `CourseType` int(11),
  `DoStatus` int(11),
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `ReduceHours` decimal(18,2),
  `ClassHourType` int(11),
  `Cost` decimal(18,0),
  `IsFixed` int(11),
  `SignTime` datetime,
  `CardGuid` char(36),
  `LessonSeriesGuid` char(36),
  `ChangePoints` int(11),
  `MakeUp` int(11),
  `FeedbackInfo` text,
  `SortID` int(11),
  `Pictures` varchar(500),
  `Nickname` varchar(50),
  `RealName` varchar(50),
  `Guardian` varchar(50),
  `Mobile` varchar(50),
  `WXOpenID` varchar(200),
  `BirthDate` datetime,
  `Sex` varchar(10),
  `AdvisorNames` varchar(200),
  `TeacherNames` varchar(200),
  `ManagerNames` varchar(200),
  `Scope` decimal(18,0),
  `CourseName` varchar(50),
  `CourseDate` datetime,
  `ClassroomName` varchar(50),
  `classroomguid` char(36),
  `ClassSectionGuid` char(36),
  `ClassSectionName` varchar(50),
  `StartTime` varchar(50),
  `EndTime` varchar(50),
  `ClassSectionTime` varchar(101),
  `LessonGuid` char(36),
  `LessonName` varchar(50),
  `MemberCount` int(11),
  `FreeCount` int(11),
  `ClassHours` decimal(18,2),
  `Teacher` varchar(500),
  `Assistant` varchar(500),
  `LessonSeriesName` varchar(50),
  `SignStatus` varchar(50),
  `MemberStatus` int(11),
  `CreatorName` varchar(50),
  `ContractNos` varchar(255),
  `ReduceGiftClassHours` decimal(6,2),
  `ReduceBuyClassHours` decimal(6,2),
  `HomeworkStatus` int(11)
) */;

--
-- Temporary table structure for view `q_memberdocourse`
--

DROP TABLE IF EXISTS `q_memberdocourse`;
/*!50001 DROP VIEW IF EXISTS `q_memberdocourse`*/;
/*!50001 CREATE TABLE `q_memberdocourse` (
  `MemberDoCourseGuid` char(36),
  `MemberGuid` char(36),
  `DoCourseGuid` char(36),
  `DoCourseType` int(11),
  `DoStatus` int(11),
  `CreateTime` datetime,
  `CreatorGuid` char(36),
  `ReduceHours` decimal(18,2),
  `ReduceCost` int(11),
  `Cost` decimal(18,0),
  `ReduceType` int(11),
  `CardGuid` char(36),
  `LessonSeriesGuid` char(36),
  `SignTime` datetime,
  `ChangePoints` int(11),
  `WasteBookGuid` char(36),
  `Nickname` varchar(50),
  `RealName` varchar(50),
  `Guardian` varchar(50),
  `Mobile` varchar(50),
  `BirthDate` datetime,
  `Sex` varchar(10),
  `SourceName` varchar(50),
  `docoursetime` varchar(103),
  `ClassroomName` varchar(50),
  `DoTitle` varchar(255),
  `DoProperties` int(11),
  `ParamName` varchar(50),
  `MemberStatus` int(11),
  `AdvisorNames` varchar(200),
  `ManagerNames` varchar(200),
  `TeacherNames` varchar(200),
  `MainTeacher` varchar(50),
  `StartTime` varchar(50),
  `EndTime` varchar(50),
  `Address` varchar(300),
  `ContractNos` varchar(255),
  `ReduceGiftClassHours` decimal(6,2),
  `ReduceBuyClassHours` decimal(6,2),
  `PayStatus` int(11)
) */;

--
-- Temporary table structure for view `q_product`
--

DROP TABLE IF EXISTS `q_product`;
/*!50001 DROP VIEW IF EXISTS `q_product`*/;
/*!50001 CREATE TABLE `q_product` (
  `ProductName` varchar(50),
  `ProductCode` varchar(50),
  `ProductGuid` char(36),
  `PurchasePrice` decimal(18,2),
  `SalePrice` decimal(18,2),
  `InventoryAmount` int(11),
  `CanExchangePoint` varchar(1),
  `ExchangePoints` int(11),
  `CreateTime` datetime,
  `Notes` longtext,
  `CategoryName` varchar(50),
  `CreatorName` varchar(50),
  `ProductCategoryGuid` char(36),
  `DoStatus` int(11),
  `ISMallProduct` int(11),
  `Discount` varchar(500)
) */;

--
-- Temporary table structure for view `q_productinstore`
--

DROP TABLE IF EXISTS `q_productinstore`;
/*!50001 DROP VIEW IF EXISTS `q_productinstore`*/;
/*!50001 CREATE TABLE `q_productinstore` (
  `Amount` int(11),
  `CreateTime` datetime,
  `InStoreGuid` char(36),
  `ProductGuid` char(36),
  `DoStatus` int(11),
  `Notes` varchar(200),
  `PurchasePrice` decimal(18,2),
  `CanExchangePoint` int(11),
  `ImgPath` varchar(200),
  `InventoryAmount` int(11),
  `ProductName` varchar(50),
  `SalePrice` decimal(18,2),
  `ProductCode` varchar(50),
  `ProductCategoryGuid` char(36),
  `CreatorName` varchar(50),
  `CategoryName` varchar(50)
) */;

--
-- Temporary table structure for view `r_course_week`
--

DROP TABLE IF EXISTS `r_course_week`;
/*!50001 DROP VIEW IF EXISTS `r_course_week`*/;
/*!50001 CREATE TABLE `r_course_week` (
  `weedNum` bigint(20),
  `weedName` varchar(3)
) */;

--
-- Table structure for table `recordsetting`
--

DROP TABLE IF EXISTS `recordsetting`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `recordsetting` (
  `Guid` varchar(36) NOT NULL,
  `RecordLength` int(11) default NULL,
  `RecordFormat` int(11) default NULL,
  `EchoCancellation` bit(1) default NULL,
  `AutomaticGain` bit(1) default NULL,
  PRIMARY KEY  (`Guid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `recvmsg`
--

DROP TABLE IF EXISTS `recvmsg`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `recvmsg` (
  `MsgGuid` char(36) NOT NULL,
  `MsgID` int(11) default NULL,
  `MemberGuid` char(36) default NULL,
  `Mobile` varchar(50) default NULL,
  `MsgContent` varchar(500) default NULL,
  `PushTime` varchar(50) default NULL,
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`MsgGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `reportparam`
--

DROP TABLE IF EXISTS `reportparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `reportparam` (
  `ParamGuid` char(36) NOT NULL,
  `ProcedureGuid` char(36) default NULL,
  `ControlName` varchar(50) default NULL,
  `ParamName` varchar(50) default NULL,
  `ParamValue` varchar(50) default NULL,
  `SortID` int(11) default NULL,
  `Notes` varchar(250) default NULL,
  PRIMARY KEY  (`ParamGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `reportsetting`
--

DROP TABLE IF EXISTS `reportsetting`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `reportsetting` (
  `ProcedureGuid` char(36) NOT NULL,
  `ProcedureName` varchar(50) default NULL,
  `ProcedureValue` varchar(50) default NULL,
  `SearchHtml` longtext,
  `IsPage` char(1) default NULL,
  `Notes` varchar(250) default NULL,
  PRIMARY KEY  (`ProcedureGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `review` (
  `ReviewGuid` char(36) NOT NULL,
  `ReviewContent` text,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Status` int(11) default NULL COMMENT '1:很不满意;2:不满意;3:不太满意;4:一般;5:较满意;6:满意;7:很满意',
  `ContractGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `riseclass`
--

DROP TABLE IF EXISTS `riseclass`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `riseclass` (
  `RiseClassGuid` char(36) NOT NULL COMMENT '升班Guid',
  `MemberGuid` char(36) default NULL COMMENT '会员Guid',
  `AppointDate` datetime default NULL COMMENT '预约日期',
  `TestDate` datetime default NULL COMMENT '测试日期',
  `TestTeacherGuid` char(36) default NULL COMMENT '测试老师Guid',
  `PassState` int(11) default NULL COMMENT '是否通过',
  `Notes` varchar(200) default NULL COMMENT '备注',
  `CreateTime` datetime default NULL COMMENT '登记时间',
  `CreatorGuid` char(36) default NULL COMMENT '登记人',
  `OldLesson` varchar(500) default NULL,
  `NewLesson` varchar(500) default NULL,
  PRIMARY KEY  (`RiseClassGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `screeninfo`
--

DROP TABLE IF EXISTS `screeninfo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `screeninfo` (
  `ManagerGuid` char(36) NOT NULL,
  `MainScreen` int(11) default NULL COMMENT '哪个是主屏幕',
  `Screen1` longtext,
  `Screen2` longtext,
  `Screen3` longtext,
  `Screen4` longtext,
  `Screen5` longtext,
  `Screen6` longtext,
  `Screen7` longtext,
  `Screen8` longtext,
  `Screen9` longtext,
  `BgImg` text COMMENT '背景',
  `LoginBgImg` text COMMENT '登录页面背景',
  `Dock` longtext
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=13264;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `searchparam`
--

DROP TABLE IF EXISTS `searchparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `searchparam` (
  `SearchParamGuid` char(36) NOT NULL,
  `ParentGuid` char(36) default NULL,
  `SearchParamName` varchar(250) default NULL COMMENT '创建时间...',
  `SearchParamValue` varchar(250) default NULL COMMENT 'createtime,creatorname',
  `ParamType` varchar(50) default NULL COMMENT 'datetime,string,int',
  `SearchType` varchar(250) default NULL COMMENT '=,<,>,<=,>=,like',
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`SearchParamGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2628 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `shoppingcart`
--

DROP TABLE IF EXISTS `shoppingcart`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `shoppingcart` (
  `CartGuid` char(36) NOT NULL COMMENT '购物车guid',
  `OpenId` char(100) NOT NULL COMMENT 'OpenId',
  `ProductGuid` char(36) NOT NULL COMMENT '商品Id',
  `Number` int(11) NOT NULL COMMENT '商品数量',
  `Remark` varchar(100) default '' COMMENT '备注',
  `UpdateTime` datetime default NULL COMMENT '最后一次更新时间',
  `CreateTime` datetime NOT NULL COMMENT '创建时间'
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `staffleave`
--

DROP TABLE IF EXISTS `staffleave`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `staffleave` (
  `StaffLeaveGuid` char(36) NOT NULL,
  `StaffGuid` char(36) default NULL,
  `StartTime` varchar(20) default NULL,
  `EndTime` varchar(20) default NULL,
  `LeaveDays` int(11) default NULL,
  `LeaveReason` text,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `AuditTime` datetime default NULL,
  `AuditorGuid` char(36) default NULL,
  `Notes` text,
  `DoStatus` int(11) default NULL,
  `LeaveTime` decimal(10,2) default NULL,
  `LeaveCategory` char(36) default NULL,
  `CourseTeacherGuids` varchar(4000) default NULL,
  PRIMARY KEY  (`StaffLeaveGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=270;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `subscribeuser`
--

DROP TABLE IF EXISTS `subscribeuser`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `subscribeuser` (
  `ID` int(11) NOT NULL auto_increment,
  `OpenId` varchar(200) NOT NULL,
  `NickName` varchar(200) default NULL,
  `Sex` varchar(50) default NULL,
  `Language` varchar(50) default NULL,
  `City` varchar(50) default NULL,
  `Province` varchar(50) default NULL,
  `Country` varchar(50) default NULL,
  `Headimgurl` longtext,
  `SubscribeTime` varchar(50) default NULL,
  `ActiveTime` datetime default NULL,
  `FilePath` varchar(230) default NULL,
  `Location` varchar(400) default NULL,
  PRIMARY KEY  (`ID`),
  KEY `UK_subscribeuser_OpenId` (`OpenId`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=41;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `supplier` (
  `SupplierGuid` char(36) NOT NULL COMMENT '供应商Guid',
  `SupplierName` varchar(100) default NULL COMMENT '供应商名称',
  `Contact` varchar(50) default NULL COMMENT '联系方式',
  `Notes` varchar(200) default NULL COMMENT '备注',
  PRIMARY KEY  (`SupplierGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `sysskin`
--

DROP TABLE IF EXISTS `sysskin`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `sysskin` (
  `SysSkinGuid` char(36) NOT NULL,
  `SysSkinName` varchar(50) default NULL,
  `Path` varchar(100) default NULL,
  `Picture` varchar(100) default NULL,
  `Note` varchar(200) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`SysSkinGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `udfmanage`
--

DROP TABLE IF EXISTS `udfmanage`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `udfmanage` (
  `FieldDbName` varchar(50) NOT NULL,
  `FieldName` varchar(50) default NULL,
  `FieldType` varchar(50) default NULL,
  `CtrlType` varchar(50) default NULL,
  `CtrlParamGuid` char(36) default NULL,
  `RequiredField` int(11) default NULL,
  `SysField` int(11) default NULL,
  `DefaultFieldName` varchar(50) default NULL,
  `IsShow` int(11) default NULL,
  `TableName` varchar(50) default NULL,
  `FieldID` int(11) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`FieldDbName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `udfparam`
--

DROP TABLE IF EXISTS `udfparam`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `udfparam` (
  `ParamGuid` char(36) NOT NULL,
  `ParentGuid` char(36) default NULL,
  `ParamName` varchar(50) default NULL,
  `ParamValue` varchar(50) default NULL,
  `ParamType` int(11) default NULL,
  `SortID` int(11) default NULL,
  PRIMARY KEY  (`ParamGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `versionupdatetip`
--

DROP TABLE IF EXISTS `versionupdatetip`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `versionupdatetip` (
  `VersionUpdateTipGuid` char(36) NOT NULL COMMENT '版本更新提示Guid',
  `ManagerGuid` char(36) NOT NULL COMMENT '管理人员Guid',
  `IsRead` int(11) default NULL COMMENT '是否下次不再显示,1为下次不再显示，0为下次继续显示',
  PRIMARY KEY  (`VersionUpdateTipGuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `w_applydo`
--

DROP TABLE IF EXISTS `w_applydo`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `w_applydo` (
  `ApplyDoGuid` char(36) NOT NULL COMMENT '申请活动ID',
  `DoGuid` char(36) default NULL COMMENT '活动ID',
  `DoTitle` varchar(200) default NULL COMMENT '活动名称',
  `StartTime` varchar(200) default NULL COMMENT '开始时间',
  `EndTime` varchar(200) default NULL COMMENT '结束时间',
  `MemberGuid` char(36) default NULL COMMENT '学员ID',
  `MemberName` varchar(100) default NULL COMMENT '学员名字',
  `Mobile` varchar(50) default NULL COMMENT '手机号码',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `DoStatus` int(11) default NULL COMMENT '状态',
  `Notes` varchar(1000) default NULL COMMENT '备注',
  PRIMARY KEY  (`ApplyDoGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wagesconfig`
--

DROP TABLE IF EXISTS `wagesconfig`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wagesconfig` (
  `LevelGuid` char(36) NOT NULL,
  `LessonCost` decimal(10,2) default NULL,
  `MemberCost` decimal(10,2) default NULL,
  `UserCost` decimal(10,2) default NULL,
  `TeacherOrAssistant` int(11) default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=124;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wagesdetial`
--

DROP TABLE IF EXISTS `wagesdetial`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wagesdetial` (
  `WagesDetialGuid` char(36) NOT NULL,
  `CourseGuid` char(36) default NULL,
  `CourseDate` datetime default NULL,
  `TeacherGuid` char(36) default NULL,
  `TeacherType` int(11) default NULL,
  `MemberCount` int(11) default NULL,
  `UserCount` int(11) default NULL,
  `RealMemberCount` int(11) default NULL,
  `RealUserCount` int(11) default NULL,
  `LeaveCount` int(11) default NULL,
  `LostCount` int(11) default NULL,
  `Achievement` decimal(10,2) default NULL,
  PRIMARY KEY  (`WagesDetialGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=367;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wastebook`
--

DROP TABLE IF EXISTS `wastebook`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wastebook` (
  `WasteBookGuid` char(36) NOT NULL,
  `InOutTypeGuid` char(36) default NULL COMMENT '支出/收入的类型',
  `InOutType` int(11) default NULL COMMENT '支出/收入',
  `WasteProjectGuid` char(36) default NULL COMMENT '支出/收入 项目',
  `Amount` decimal(10,2) default '0.00' COMMENT '金额',
  `ActiveTime` datetime default NULL COMMENT '支出/收入的时间',
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `CheckTime` datetime default NULL,
  `CheckUserGuid` char(36) default NULL,
  `DoStatus` int(11) default '0',
  `Notes` varchar(255) default NULL,
  `DepartmentGuid` char(36) default NULL,
  `MemberGuid` char(36) default NULL,
  `PayTypeName` varchar(200) default NULL,
  `Attachment` varchar(200) default NULL,
  `RelatedItemGuid` char(36) default NULL,
  `SourceGuid` char(36) default NULL COMMENT '来源GUID',
  `SourceType` int(11) default NULL COMMENT '来源类型',
  PRIMARY KEY  (`WasteBookGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=231;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `webim_group`
--

DROP TABLE IF EXISTS `webim_group`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `webim_group` (
  `GroupGuid` varchar(36) NOT NULL,
  `GroupName` varchar(255) default NULL,
  `InviteCode` varchar(255) default NULL,
  `CreateGuid` varchar(36) default NULL,
  PRIMARY KEY  (`GroupGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=88;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `webim_groupuser`
--

DROP TABLE IF EXISTS `webim_groupuser`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `webim_groupuser` (
  `GroupUserGuid` varchar(36) NOT NULL,
  `UserGuid` varchar(36) default NULL,
  `GroupGuid` varchar(36) default NULL,
  PRIMARY KEY  (`GroupUserGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `webim_message`
--

DROP TABLE IF EXISTS `webim_message`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `webim_message` (
  `MessageGuid` varchar(36) NOT NULL,
  `CreatedTime` datetime default NULL,
  `ReceiverGuid` varchar(36) default NULL,
  `SenderGuid` varchar(36) default NULL,
  `MessageContent` text,
  `GroupGuid` varchar(36) default NULL,
  PRIMARY KEY  (`MessageGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `workattendance`
--

DROP TABLE IF EXISTS `workattendance`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `workattendance` (
  `WorkAttendanceGuid` char(36) NOT NULL default '',
  `ManagerGuid` char(36) default NULL,
  `AttendanceType` varchar(10) default NULL,
  `RuleTime` varchar(10) default NULL,
  `AttendanceTime` datetime default NULL,
  `AttendanceInfo` varchar(100) default NULL,
  PRIMARY KEY  (`WorkAttendanceGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=108;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `worklog`
--

DROP TABLE IF EXISTS `worklog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `worklog` (
  `WorkLogGuid` char(36) NOT NULL,
  `LogDate` datetime default NULL,
  `Title` varchar(255) default NULL,
  `LogContent` text,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  `Attachment` varchar(500) default NULL,
  PRIMARY KEY  (`WorkLogGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2417;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `worklogreviews`
--

DROP TABLE IF EXISTS `worklogreviews`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `worklogreviews` (
  `WorkLogReviewsGuid` char(36) NOT NULL,
  `WorkLogGuid` char(36) default NULL,
  `ReviewsContent` text,
  `CreateTime` datetime default NULL,
  `CreatorGuid` char(36) default NULL,
  PRIMARY KEY  (`WorkLogReviewsGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `workrule`
--

DROP TABLE IF EXISTS `workrule`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `workrule` (
  `WorkRuleGuid` char(36) NOT NULL default '',
  `WorkStartTime` varchar(10) default NULL,
  `StartOpenAhead` int(4) default NULL,
  `StartStopDelay` int(4) default NULL,
  `WorkEndTime` varchar(10) default NULL,
  `EndOpenAhead` int(4) default NULL,
  `EndStopDelay` int(4) default NULL,
  `SignTime` varchar(10) default NULL,
  `SignType` varchar(10) default NULL,
  `OpenAhead` int(11) default NULL,
  `StopDelay` int(11) default NULL,
  PRIMARY KEY  (`WorkRuleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=16384;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wx_content`
--

DROP TABLE IF EXISTS `wx_content`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wx_content` (
  `ContentGuid` char(36) NOT NULL COMMENT '内容Guid',
  `WebSiteGuid` char(36) NOT NULL,
  `Type` int(11) NOT NULL COMMENT '标题',
  `Img` varchar(500) default NULL COMMENT '图片',
  `Introduce` text COMMENT '介绍',
  `Content1` text COMMENT '备用字段',
  `Content2` text COMMENT '备用字段',
  `Content3` text COMMENT '备用字段',
  `CreateTime` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`ContentGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wx_signup`
--

DROP TABLE IF EXISTS `wx_signup`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wx_signup` (
  `SignUpGuid` char(36) NOT NULL COMMENT '报名ID',
  `MemberGuid` char(36) NOT NULL,
  `Channel` int(11) NOT NULL COMMENT '渠道',
  `Name` varchar(50) NOT NULL COMMENT '姓名',
  `Mobile` varchar(50) NOT NULL COMMENT '手机号码',
  `Age` datetime default NULL COMMENT '生日',
  `Address` varchar(200) default NULL COMMENT '地址',
  `IsImport` int(11) NOT NULL COMMENT '是否已导入到我的学员列表',
  `CreateTime` timestamp NOT NULL default CURRENT_TIMESTAMP COMMENT '添加日期',
  `CreatorGuid` char(36) NOT NULL default '00000000-0000-0000-0000-000000000000' COMMENT '添加人',
  `DoGuid` char(36) default NULL,
  `Openid` varchar(100) default NULL,
  `Guardian` varchar(50) default NULL,
  PRIMARY KEY  (`SignUpGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wx_systemplate`
--

DROP TABLE IF EXISTS `wx_systemplate`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wx_systemplate` (
  `SysTempGuid` char(36) NOT NULL COMMENT '系统通知模板',
  `TempType` int(11) default NULL COMMENT '模板类型 1:签到 2:约课 3:托班签到',
  `Title` varchar(255) default NULL COMMENT '模板标题',
  `Content` varchar(500) default NULL COMMENT '模板内容',
  `Example` varchar(500) default NULL COMMENT '模板示例',
  `FirstData` varchar(255) default NULL COMMENT '模板开始内容',
  `RemarkData` varchar(255) default NULL COMMENT '模板结束内容',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `MiddleData` varchar(255) default NULL COMMENT '模板中间内容',
  PRIMARY KEY  (`SysTempGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2498 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wx_template`
--

DROP TABLE IF EXISTS `wx_template`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wx_template` (
  `WxTempGuid` char(36) NOT NULL COMMENT '微信模板',
  `WxTemplateid` varchar(255) default NULL COMMENT '微信模板ID',
  `TempType` int(11) default NULL COMMENT '模板类型 1:签到 2:约课',
  `Title` varchar(255) default NULL COMMENT '模板标题',
  `Content` varchar(500) default NULL COMMENT '模板内容',
  `Example` varchar(500) default NULL COMMENT '模板示例',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  PRIMARY KEY  (`WxTempGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=2498 ROW_FORMAT=FIXED;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wx_website`
--

DROP TABLE IF EXISTS `wx_website`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wx_website` (
  `WebSiteGuid` char(36) NOT NULL COMMENT 'ID',
  `CompanyName` varchar(100) default NULL,
  `SMSSerialNo` char(36) NOT NULL COMMENT 'AppId',
  `BGMusic` varchar(100) default NULL COMMENT '背景音乐地址',
  `CreateTime` datetime default NULL COMMENT '创建时间',
  `CreatorGuid` char(36) NOT NULL default '00000000-0000-0000-0000-000000000000' COMMENT '创建人',
  PRIMARY KEY  (`WebSiteGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wx_website_signupfield`
--

DROP TABLE IF EXISTS `wx_website_signupfield`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wx_website_signupfield` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(255) default NULL COMMENT '名称',
  `displayName` varchar(255) default NULL COMMENT '显示名称',
  `isMustDisplay` bit(1) default NULL COMMENT '是否必须显示',
  `isDisplay` bit(1) default NULL COMMENT '是否显示',
  `isRequire` bit(1) default NULL COMMENT '是否必填',
  `sort` int(11) default NULL COMMENT '排序',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wx_websitemodule`
--

DROP TABLE IF EXISTS `wx_websitemodule`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wx_websitemodule` (
  `ModuleGuid` char(36) NOT NULL COMMENT '栏目ID',
  `WebSiteGuid` char(36) NOT NULL COMMENT 'ID',
  `Name` varchar(100) NOT NULL COMMENT '栏目名称',
  `IsShow` bit(1) default NULL COMMENT '是否显示',
  `Type` int(11) default NULL COMMENT '栏目类型',
  `Introduce` text COMMENT '栏目介绍',
  `SortId` int(11) default NULL COMMENT '栏目排序',
  `CreateTime` timestamp NOT NULL default CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY  (`ModuleGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wxbulkmsglog`
--

DROP TABLE IF EXISTS `wxbulkmsglog`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wxbulkmsglog` (
  `BulkMsgGuid` char(36) NOT NULL,
  `BulkMsgType` int(11) default NULL COMMENT '0:文字信息  1：图文信息',
  `ManagerGuid` char(36) default NULL,
  `ManagerName` varchar(255) default NULL,
  `CreateTime` datetime default NULL,
  `TextMsgContent` text COMMENT '文本信息 内容',
  `NewsTitle` text COMMENT '图文信息 标题',
  `NewsImgUrl` text COMMENT '图文信息 图片地址',
  `NewsDescription` text COMMENT '图文信息描述',
  `NewsContent` text COMMENT '图文信息详细内容',
  `NewsGuid` char(36) default NULL COMMENT '本地保存的图文信息guid',
  `NewsServerGuid` char(36) default NULL COMMENT '图文信息服务器上保存的guid',
  `OpenIdList` text COMMENT '发送的openid   已“，”分隔',
  `NickNameList` text COMMENT '微信昵称  已“，”分隔',
  `OpenIdCount` int(11) default NULL COMMENT '发送人数',
  `BulkMsgNotes` text,
  PRIMARY KEY  (`BulkMsgGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 AVG_ROW_LENGTH=703;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wxtemp_classhour`
--

DROP TABLE IF EXISTS `wxtemp_classhour`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wxtemp_classhour` (
  `OpenID` varchar(200) NOT NULL,
  `ClasshourNotes` varchar(300) default NULL,
  `RealName` varchar(200) default NULL,
  `Mobile` varchar(100) default NULL,
  `CreateTime` datetime default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`OpenID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wxtemp_course`
--

DROP TABLE IF EXISTS `wxtemp_course`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wxtemp_course` (
  `CourseGuid` char(36) default NULL,
  `CourseDate` datetime default NULL,
  `CourseName` varchar(200) default NULL,
  `ClassSection` varchar(200) default NULL,
  `Classroom` varchar(200) default NULL,
  `DoStatus` int(11) default NULL COMMENT '增:1,删:2,改:3',
  `CreateTime` datetime default NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wxtemp_feedback`
--

DROP TABLE IF EXISTS `wxtemp_feedback`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wxtemp_feedback` (
  `MemberCourseGuid` char(36) NOT NULL,
  `OpenID` varchar(200) default NULL,
  `CourseDate` datetime default NULL,
  `CourseName` varchar(200) default NULL,
  `FeedBackInfo` text,
  `DoStatus` int(11) default NULL COMMENT '增1 删2 改3 ',
  `CreateTime` datetime default NULL,
  PRIMARY KEY  (`MemberCourseGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `wxvcode`
--

DROP TABLE IF EXISTS `wxvcode`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `wxvcode` (
  `MsgGuid` char(36) NOT NULL,
  `OpenId` varchar(200) default NULL,
  `Mobile` varchar(50) default NULL,
  `Code` varchar(50) default NULL,
  `CreateTime` datetime default NULL,
  `CodeType` int(11) default NULL,
  `DoStatus` int(11) default NULL,
  PRIMARY KEY  (`MsgGuid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
SET character_set_client = @saved_cs_client;

--
-- Current Database: `mysql`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `mysql` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `mysql`;

--
-- Table structure for table `columns_priv`
--

DROP TABLE IF EXISTS `columns_priv`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `columns_priv` (
  `Host` char(60) NOT NULL default '',
  `Db` char(64) NOT NULL default '',
  `User` char(16) NOT NULL default '',
  `Table_name` char(64) NOT NULL default '',
  `Column_name` char(64) NOT NULL default '',
  `Timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `Column_priv` set('Select','Insert','Update','References') NOT NULL default '',
  PRIMARY KEY  (`Host`,`Db`,`User`,`Table_name`,`Column_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Column privileges';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `db`
--

DROP TABLE IF EXISTS `db`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `db` (
  `Host` char(60) NOT NULL default '',
  `Db` char(64) NOT NULL default '',
  `User` char(16) NOT NULL default '',
  `Select_priv` enum('N','Y') NOT NULL default 'N',
  `Insert_priv` enum('N','Y') NOT NULL default 'N',
  `Update_priv` enum('N','Y') NOT NULL default 'N',
  `Delete_priv` enum('N','Y') NOT NULL default 'N',
  `Create_priv` enum('N','Y') NOT NULL default 'N',
  `Drop_priv` enum('N','Y') NOT NULL default 'N',
  `Grant_priv` enum('N','Y') NOT NULL default 'N',
  `References_priv` enum('N','Y') NOT NULL default 'N',
  `Index_priv` enum('N','Y') NOT NULL default 'N',
  `Alter_priv` enum('N','Y') NOT NULL default 'N',
  `Create_tmp_table_priv` enum('N','Y') NOT NULL default 'N',
  `Lock_tables_priv` enum('N','Y') NOT NULL default 'N',
  `Create_view_priv` enum('N','Y') NOT NULL default 'N',
  `Show_view_priv` enum('N','Y') NOT NULL default 'N',
  `Create_routine_priv` enum('N','Y') NOT NULL default 'N',
  `Alter_routine_priv` enum('N','Y') NOT NULL default 'N',
  `Execute_priv` enum('N','Y') NOT NULL default 'N',
  PRIMARY KEY  (`Host`,`Db`,`User`),
  KEY `User` (`User`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Database privileges';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `func`
--

DROP TABLE IF EXISTS `func`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `func` (
  `name` char(64) NOT NULL default '',
  `ret` tinyint(1) NOT NULL default '0',
  `dl` char(128) NOT NULL default '',
  `type` enum('function','aggregate') NOT NULL,
  PRIMARY KEY  (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='User defined functions';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `help_category`
--

DROP TABLE IF EXISTS `help_category`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `help_category` (
  `help_category_id` smallint(5) unsigned NOT NULL,
  `name` char(64) NOT NULL,
  `parent_category_id` smallint(5) unsigned default NULL,
  `url` char(128) NOT NULL,
  PRIMARY KEY  (`help_category_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='help categories';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `help_keyword`
--

DROP TABLE IF EXISTS `help_keyword`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `help_keyword` (
  `help_keyword_id` int(10) unsigned NOT NULL,
  `name` char(64) NOT NULL,
  PRIMARY KEY  (`help_keyword_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='help keywords';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `help_relation`
--

DROP TABLE IF EXISTS `help_relation`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `help_relation` (
  `help_topic_id` int(10) unsigned NOT NULL,
  `help_keyword_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`help_keyword_id`,`help_topic_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='keyword-topic relation';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `help_topic`
--

DROP TABLE IF EXISTS `help_topic`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `help_topic` (
  `help_topic_id` int(10) unsigned NOT NULL,
  `name` char(64) NOT NULL,
  `help_category_id` smallint(5) unsigned NOT NULL,
  `description` text NOT NULL,
  `example` text NOT NULL,
  `url` char(128) NOT NULL,
  PRIMARY KEY  (`help_topic_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='help topics';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `host`
--

DROP TABLE IF EXISTS `host`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `host` (
  `Host` char(60) NOT NULL default '',
  `Db` char(64) NOT NULL default '',
  `Select_priv` enum('N','Y') NOT NULL default 'N',
  `Insert_priv` enum('N','Y') NOT NULL default 'N',
  `Update_priv` enum('N','Y') NOT NULL default 'N',
  `Delete_priv` enum('N','Y') NOT NULL default 'N',
  `Create_priv` enum('N','Y') NOT NULL default 'N',
  `Drop_priv` enum('N','Y') NOT NULL default 'N',
  `Grant_priv` enum('N','Y') NOT NULL default 'N',
  `References_priv` enum('N','Y') NOT NULL default 'N',
  `Index_priv` enum('N','Y') NOT NULL default 'N',
  `Alter_priv` enum('N','Y') NOT NULL default 'N',
  `Create_tmp_table_priv` enum('N','Y') NOT NULL default 'N',
  `Lock_tables_priv` enum('N','Y') NOT NULL default 'N',
  `Create_view_priv` enum('N','Y') NOT NULL default 'N',
  `Show_view_priv` enum('N','Y') NOT NULL default 'N',
  `Create_routine_priv` enum('N','Y') NOT NULL default 'N',
  `Alter_routine_priv` enum('N','Y') NOT NULL default 'N',
  `Execute_priv` enum('N','Y') NOT NULL default 'N',
  PRIMARY KEY  (`Host`,`Db`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Host privileges;  Merged with database privileges';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `proc`
--

DROP TABLE IF EXISTS `proc`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `proc` (
  `db` char(64) character set utf8 collate utf8_bin NOT NULL default '',
  `name` char(64) NOT NULL default '',
  `type` enum('FUNCTION','PROCEDURE') NOT NULL,
  `specific_name` char(64) NOT NULL default '',
  `language` enum('SQL') NOT NULL default 'SQL',
  `sql_data_access` enum('CONTAINS_SQL','NO_SQL','READS_SQL_DATA','MODIFIES_SQL_DATA') NOT NULL default 'CONTAINS_SQL',
  `is_deterministic` enum('YES','NO') NOT NULL default 'NO',
  `security_type` enum('INVOKER','DEFINER') NOT NULL default 'DEFINER',
  `param_list` blob NOT NULL,
  `returns` char(64) NOT NULL default '',
  `body` longblob NOT NULL,
  `definer` char(77) character set utf8 collate utf8_bin NOT NULL default '',
  `created` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `modified` timestamp NOT NULL default '0000-00-00 00:00:00',
  `sql_mode` set('REAL_AS_FLOAT','PIPES_AS_CONCAT','ANSI_QUOTES','IGNORE_SPACE','NOT_USED','ONLY_FULL_GROUP_BY','NO_UNSIGNED_SUBTRACTION','NO_DIR_IN_CREATE','POSTGRESQL','ORACLE','MSSQL','DB2','MAXDB','NO_KEY_OPTIONS','NO_TABLE_OPTIONS','NO_FIELD_OPTIONS','MYSQL323','MYSQL40','ANSI','NO_AUTO_VALUE_ON_ZERO','NO_BACKSLASH_ESCAPES','STRICT_TRANS_TABLES','STRICT_ALL_TABLES','NO_ZERO_IN_DATE','NO_ZERO_DATE','INVALID_DATES','ERROR_FOR_DIVISION_BY_ZERO','TRADITIONAL','NO_AUTO_CREATE_USER','HIGH_NOT_PRECEDENCE') NOT NULL default '',
  `comment` char(64) character set utf8 collate utf8_bin NOT NULL default '',
  PRIMARY KEY  (`db`,`name`,`type`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Stored Procedures';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `procs_priv`
--

DROP TABLE IF EXISTS `procs_priv`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `procs_priv` (
  `Host` char(60) NOT NULL default '',
  `Db` char(64) NOT NULL default '',
  `User` char(16) NOT NULL default '',
  `Routine_name` char(64) NOT NULL default '',
  `Routine_type` enum('FUNCTION','PROCEDURE') NOT NULL,
  `Grantor` char(77) NOT NULL default '',
  `Proc_priv` set('Execute','Alter Routine','Grant') NOT NULL default '',
  `Timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`Host`,`Db`,`User`,`Routine_name`,`Routine_type`),
  KEY `Grantor` (`Grantor`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Procedure privileges';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `tables_priv`
--

DROP TABLE IF EXISTS `tables_priv`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `tables_priv` (
  `Host` char(60) NOT NULL default '',
  `Db` char(64) NOT NULL default '',
  `User` char(16) NOT NULL default '',
  `Table_name` char(64) NOT NULL default '',
  `Grantor` char(77) NOT NULL default '',
  `Timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `Table_priv` set('Select','Insert','Update','Delete','Create','Drop','Grant','References','Index','Alter','Create View','Show view') NOT NULL default '',
  `Column_priv` set('Select','Insert','Update','References') NOT NULL default '',
  PRIMARY KEY  (`Host`,`Db`,`User`,`Table_name`),
  KEY `Grantor` (`Grantor`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Table privileges';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `time_zone`
--

DROP TABLE IF EXISTS `time_zone`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `time_zone` (
  `Time_zone_id` int(10) unsigned NOT NULL auto_increment,
  `Use_leap_seconds` enum('Y','N') NOT NULL default 'N',
  PRIMARY KEY  (`Time_zone_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Time zones';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `time_zone_leap_second`
--

DROP TABLE IF EXISTS `time_zone_leap_second`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `time_zone_leap_second` (
  `Transition_time` bigint(20) NOT NULL,
  `Correction` int(11) NOT NULL,
  PRIMARY KEY  (`Transition_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Leap seconds information for time zones';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `time_zone_name`
--

DROP TABLE IF EXISTS `time_zone_name`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `time_zone_name` (
  `Name` char(64) NOT NULL,
  `Time_zone_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`Name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Time zone names';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `time_zone_transition`
--

DROP TABLE IF EXISTS `time_zone_transition`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `time_zone_transition` (
  `Time_zone_id` int(10) unsigned NOT NULL,
  `Transition_time` bigint(20) NOT NULL,
  `Transition_type_id` int(10) unsigned NOT NULL,
  PRIMARY KEY  (`Time_zone_id`,`Transition_time`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Time zone transitions';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `time_zone_transition_type`
--

DROP TABLE IF EXISTS `time_zone_transition_type`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `time_zone_transition_type` (
  `Time_zone_id` int(10) unsigned NOT NULL,
  `Transition_type_id` int(10) unsigned NOT NULL,
  `Offset` int(11) NOT NULL default '0',
  `Is_DST` tinyint(3) unsigned NOT NULL default '0',
  `Abbreviation` char(8) NOT NULL default '',
  PRIMARY KEY  (`Time_zone_id`,`Transition_type_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Time zone transition types';
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `user` (
  `Host` char(60) NOT NULL default '',
  `User` char(16) NOT NULL default '',
  `Password` char(41) NOT NULL default '',
  `Select_priv` enum('N','Y') NOT NULL default 'N',
  `Insert_priv` enum('N','Y') NOT NULL default 'N',
  `Update_priv` enum('N','Y') NOT NULL default 'N',
  `Delete_priv` enum('N','Y') NOT NULL default 'N',
  `Create_priv` enum('N','Y') NOT NULL default 'N',
  `Drop_priv` enum('N','Y') NOT NULL default 'N',
  `Reload_priv` enum('N','Y') NOT NULL default 'N',
  `Shutdown_priv` enum('N','Y') NOT NULL default 'N',
  `Process_priv` enum('N','Y') NOT NULL default 'N',
  `File_priv` enum('N','Y') NOT NULL default 'N',
  `Grant_priv` enum('N','Y') NOT NULL default 'N',
  `References_priv` enum('N','Y') NOT NULL default 'N',
  `Index_priv` enum('N','Y') NOT NULL default 'N',
  `Alter_priv` enum('N','Y') NOT NULL default 'N',
  `Show_db_priv` enum('N','Y') NOT NULL default 'N',
  `Super_priv` enum('N','Y') NOT NULL default 'N',
  `Create_tmp_table_priv` enum('N','Y') NOT NULL default 'N',
  `Lock_tables_priv` enum('N','Y') NOT NULL default 'N',
  `Execute_priv` enum('N','Y') NOT NULL default 'N',
  `Repl_slave_priv` enum('N','Y') NOT NULL default 'N',
  `Repl_client_priv` enum('N','Y') NOT NULL default 'N',
  `Create_view_priv` enum('N','Y') NOT NULL default 'N',
  `Show_view_priv` enum('N','Y') NOT NULL default 'N',
  `Create_routine_priv` enum('N','Y') NOT NULL default 'N',
  `Alter_routine_priv` enum('N','Y') NOT NULL default 'N',
  `Create_user_priv` enum('N','Y') NOT NULL default 'N',
  `ssl_type` enum('','ANY','X509','SPECIFIED') NOT NULL default '',
  `ssl_cipher` blob NOT NULL,
  `x509_issuer` blob NOT NULL,
  `x509_subject` blob NOT NULL,
  `max_questions` int(11) unsigned NOT NULL default '0',
  `max_updates` int(11) unsigned NOT NULL default '0',
  `max_connections` int(11) unsigned NOT NULL default '0',
  `max_user_connections` int(11) unsigned NOT NULL default '0',
  PRIMARY KEY  (`Host`,`User`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Users and global privileges';
SET character_set_client = @saved_cs_client;

--
-- Current Database: `etm_one`
--

USE `etm_one`;

--
-- Final view structure for view `q_card`
--

/*!50001 DROP TABLE `q_card`*/;
/*!50001 DROP VIEW IF EXISTS `q_card`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_card` AS select `a`.`CardGuid` AS `CardGuid`,`a`.`CardNo` AS `CardNo`,ifnull(`a`.`Amount`,0) AS `Amount`,`a`.`CardTypeGuid` AS `CardTypeGuid`,`a`.`LeaveDays` AS `LeaveDays`,`a`.`EffectiveDuration` AS `EffectiveDuration`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`DoStatus` AS `DoStatus`,`a`.`Notes` AS `Notes`,`a`.`MainCardGuid` AS `MainCardGuid`,`a`.`UseType` AS `UseType`,`a`.`StopDate` AS `StopDate`,`b`.`CardTypeName` AS `CardTypeName`,`b`.`MallDiscount` AS `malldiscount`,`d`.`MemberGuid` AS `MemberGuid`,`d`.`RealName` AS `RealName`,`d`.`NickName` AS `Nickname`,`d`.`Guardian` AS `Guardian`,`d`.`Sex` AS `Sex`,`d`.`BirthDate` AS `BirthDate`,`d`.`Mobile` AS `Mobile`,`d`.`DoStatus` AS `MemberStatus`,`e`.`UserName` AS `CreatorName`,concat((case when (`a`.`UseType` = 3) then _utf8'主卡' else _utf8'附属卡' end),(case when (`a`.`UseType` = 0) then _utf8'（共享）' when (`a`.`UseType` = 1) then _utf8'（独享）' else _utf8'' end)) AS `CardType` from (((((`card` `a` left join `cardtype` `b` on((`a`.`CardTypeGuid` = `b`.`CardTypeGuid`))) left join `membercard` `c` on((`a`.`CardGuid` = `c`.`CardGuid`))) left join `q_member` `d` on((`c`.`MemberGuid` = `d`.`MemberGuid`))) left join `k_manager` `e` on((`a`.`CreatorGuid` = `e`.`ManagerGUID`))) left join `card` `f` on((`a`.`MainCardGuid` = `f`.`CardGuid`))) */;

--
-- Final view structure for view `q_cardclasshours`
--

/*!50001 DROP TABLE `q_cardclasshours`*/;
/*!50001 DROP VIEW IF EXISTS `q_cardclasshours`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_cardclasshours` AS select `p`.`CardGuid` AS `CardGuid`,`q`.`CurrentClassHours` AS `CurrentClassHours` from (`card` `p` left join `q_cardpackage` `q` on((`p`.`CardGuid` = `q`.`CardGuid`))) where ((`p`.`DoStatus` = 154) and (`q`.`LessonSeriesGuid` = _utf8'00000000-0000-0000-0000-000000000000')) */;

--
-- Final view structure for view `q_cardflow`
--

/*!50001 DROP TABLE `q_cardflow`*/;
/*!50001 DROP VIEW IF EXISTS `q_cardflow`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_cardflow` AS select `b`.`CardGuid` AS `CardGuid`,`b`.`CardNo` AS `CardNo`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`RealName` AS `RealName`,`a`.`Mobile` AS `Mobile`,`a`.`LessonName` AS `CostContent`,_utf8'课程' AS `CostType`,concat(cast(`a`.`ReduceHours` as char charset utf8),_utf8'课时') AS `ChangeClassHours`,concat((case when (`b`.`UseType` = 3) then _utf8'主卡' else _utf8'附属卡' end),(case when (`b`.`UseType` = 0) then _utf8'(共享)' when (`b`.`UseType` = 1) then _utf8'(独享)' else _utf8'' end)) AS `CardType`,`a`.`SignTime` AS `CostTime`,`a`.`MemberStatus` AS `MemberStatus` from (`q_membercourse` `a` left join `card` `b` on((`a`.`CardGuid` = `b`.`CardGuid`))) where ((`a`.`ReduceHours` > 0) and (`a`.`DoStatus` <> 0) and (`a`.`CardGuid` is not null) and (`a`.`CardGuid` <> _utf8'00000000-0000-0000-0000-000000000000')) union select `b`.`CardGuid` AS `CardGuid`,`b`.`CardNo` AS `CardNo`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`RealName` AS `RealName`,`a`.`Mobile` AS `Mobile`,`a`.`DoTitle` AS `CostContent`,_utf8'活动' AS `CostType`,concat(cast(`a`.`ReduceHours` as char charset utf8),_utf8'课时') AS `ChangeClassHours`,concat((case when (`b`.`UseType` = 3) then _utf8'主卡' else _utf8'附属卡' end),(case when (`b`.`UseType` = 0) then _utf8'(共享)' when (`b`.`UseType` = 1) then _utf8'(独享)' else _utf8'' end)) AS `CardType`,`a`.`SignTime` AS `CostTime`,`a`.`MemberStatus` AS `MemberStatus` from (`q_memberdocourse` `a` left join `card` `b` on((`a`.`CardGuid` = `b`.`CardGuid`))) where ((`a`.`ReduceHours` > 0) and (`a`.`DoStatus` <> 0) and (`a`.`CardGuid` is not null) and (`a`.`CardGuid` <> _utf8'00000000-0000-0000-0000-000000000000')) union select `b`.`CardGuid` AS `CardGuid`,`b`.`CardNo` AS `CardNo`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`RealName` AS `RealName`,`a`.`Mobile` AS `Mobile`,`a`.`DoTitle` AS `CostContent`,_utf8'活动' AS `CostType`,concat(cast(`a`.`ReduceCost` as char charset utf8),_utf8'元') AS `ChangeClassHours`,concat((case when (`b`.`UseType` = 3) then _utf8'主卡' else _utf8'附属卡' end),(case when (`b`.`UseType` = 0) then _utf8'(共享)' when (`b`.`UseType` = 1) then _utf8'(独享)' else _utf8'' end)) AS `CardType`,`a`.`SignTime` AS `CostTime`,`a`.`MemberStatus` AS `MemberStatus` from (`q_memberdocourse` `a` left join `card` `b` on((`a`.`CardGuid` = `b`.`CardGuid`))) where ((`a`.`ReduceCost` > 0) and (`a`.`DoStatus` <> 0) and (`a`.`CardGuid` is not null) and (`a`.`CardGuid` <> _utf8'00000000-0000-0000-0000-000000000000')) union select `a`.`CardGuid` AS `CardGuid`,`b`.`CardNo` AS `CardNo`,`c`.`MemberGuid` AS `MemberGuid`,`d`.`RealName` AS `RealName`,`d`.`Mobile` AS `Mobile`,`a`.`Notes` AS `CostContent`,_utf8'课时变动' AS `CostType`,concat(cast(`a`.`ClassHours` as char charset utf8),_utf8'课时') AS `ChangeClassHours`,concat((case when (`b`.`UseType` = 3) then _utf8'主卡' else _utf8'附属卡' end),(case when (`b`.`UseType` = 0) then _utf8'(共享)' when (`b`.`UseType` = 1) then _utf8'(独享)' else _utf8'' end)) AS `CardType`,`a`.`CreateTime` AS `CostTime`,`d`.`DoStatus` AS `MemberStatus` from (((`cardgift` `a` left join `card` `b` on((`a`.`CardGuid` = `b`.`CardGuid`))) left join `membercard` `c` on((`a`.`CardGuid` = `c`.`CardGuid`))) left join `member` `d` on((`c`.`MemberGuid` = `d`.`MemberGuid`))) where (`a`.`ChangeType` = 1) union select `a`.`CardGuid` AS `CardGuid`,`b`.`CardNo` AS `CardNo`,`b`.`MemberGuid` AS `MemberGuid`,`b`.`RealName` AS `RealName`,`b`.`Mobile` AS `Mobile`,`a`.`Notes` AS `CostContent`,_utf8'商城' AS `CostType`,concat(cast(`a`.`BillAmount` as char charset utf8),_utf8'元') AS `ChangeClassHours`,`b`.`CardType` AS `CardType`,`a`.`CreateTime` AS `CostTime`,`b`.`DoStatus` AS `MemberStatus` from (`outstorebill` `a` left join `q_card` `b` on((`b`.`CardGuid` = `a`.`CardGuid`))) where ((`a`.`CardGuid` <> NULL) or (`a`.`CardGuid` <> _utf8'00000000-0000-0000-0000-000000000000')) */;

--
-- Final view structure for view `q_cardpackage`
--

/*!50001 DROP TABLE `q_cardpackage`*/;
/*!50001 DROP VIEW IF EXISTS `q_cardpackage`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_cardpackage` AS select `a`.`CardGuid` AS `CardGuid`,`a`.`LessonSeriesGuid` AS `LessonSeriesGuid`,`a`.`CurrentClassHours` AS `CurrentClassHours`,`a`.`Notes` AS `Notes`,`b`.`CardNo` AS `CardNo`,concat((case when (`b`.`UseType` = 3) then _utf8'主卡' else _utf8'附属卡' end),(case when (`b`.`UseType` = 1) then _utf8'（独享）' else _utf8'' end)) AS `CardType`,(case when (`a`.`LessonSeriesGuid` = _utf8'00000000-0000-0000-0000-000000000000') then _utf8'通用课时' else `c`.`LessonSeriesName` end) AS `LessonSeriesName` from ((`cardpackage` `a` left join `card` `b` on((`a`.`CardGuid` = `b`.`CardGuid`))) left join `lessonseries` `c` on((`c`.`LessonSeriesGuid` = `a`.`LessonSeriesGuid`))) where (`b`.`UseType` in (1,3)) union all select `bb`.`CardGuid` AS `CardGuid`,`aa`.`LessonSeriesGuid` AS `LessonSeriesGuid`,`aa`.`CurrentClassHours` AS `CurrentClassHours`,`aa`.`Notes` AS `Notes`,`bb`.`CardNo` AS `CardNo`,_utf8'附属卡（共享）' AS `CardType`,(case when (`aa`.`LessonSeriesGuid` = _utf8'00000000-0000-0000-0000-000000000000') then _utf8'通用课时' else `dd`.`LessonSeriesName` end) AS `LessonSeriesName` from (((`card` `bb` left join `card` `cc` on((`bb`.`MainCardGuid` = `cc`.`CardGuid`))) left join `cardpackage` `aa` on((`aa`.`CardGuid` = `cc`.`CardGuid`))) left join `lessonseries` `dd` on((`dd`.`LessonSeriesGuid` = `aa`.`LessonSeriesGuid`))) where (`bb`.`UseType` = 0) */;

--
-- Final view structure for view `q_cardpackage_154`
--

/*!50001 DROP TABLE `q_cardpackage_154`*/;
/*!50001 DROP VIEW IF EXISTS `q_cardpackage_154`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_cardpackage_154` AS select `a`.`CardGuid` AS `CardGuid`,`a`.`LessonSeriesGuid` AS `LessonSeriesGuid`,`a`.`CurrentClassHours` AS `CurrentClassHours`,`c`.`LessonSeriesName` AS `LessonSeriesName` from ((`cardpackage` `a` left join `card` `b` on((`a`.`CardGuid` = `b`.`CardGuid`))) left join `lessonseries` `c` on((`c`.`LessonSeriesGuid` = `a`.`LessonSeriesGuid`))) where ((`b`.`UseType` = 3) and (`b`.`DoStatus` = 154)) union all select `bb`.`CardGuid` AS `CardGuid`,`aa`.`LessonSeriesGuid` AS `LessonSeriesGuid`,`aa`.`CurrentClassHours` AS `CurrentClassHours`,`dd`.`LessonSeriesName` AS `LessonSeriesName` from (((`card` `bb` left join `card` `cc` on(((`bb`.`MainCardGuid` = `cc`.`CardGuid`) and (`cc`.`DoStatus` = 154)))) left join `cardpackage` `aa` on((`aa`.`CardGuid` = `cc`.`CardGuid`))) left join `lessonseries` `dd` on((`dd`.`LessonSeriesGuid` = `aa`.`LessonSeriesGuid`))) where ((`bb`.`UseType` = 0) and (`bb`.`DoStatus` = 154) and (`aa`.`LessonSeriesGuid` is not null)) */;

--
-- Final view structure for view `q_cardtransform`
--

/*!50001 DROP TABLE `q_cardtransform`*/;
/*!50001 DROP VIEW IF EXISTS `q_cardtransform`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_cardtransform` AS select `a`.`CardGuid` AS `CardGuid`,`a`.`CreateTime` AS `CreateTime`,(case when (`a`.`Flow` = 1) then concat(_utf8'现金充值',cast(`a`.`Amount` as char charset utf8),_utf8'元') when (`a`.`Flow` = 2) then concat(_utf8'现金扣减',cast(`a`.`Amount` as char charset utf8),_utf8'元') when (`a`.`Flow` = 3) then concat(cast(`a`.`ClassHours` as char charset utf8),_utf8'课时转换金额',cast(`a`.`Amount` as char charset utf8),_utf8'元') when (`a`.`Flow` = 4) then concat(_utf8'金额',cast(`a`.`Amount` as char charset utf8),_utf8'元转换',cast(`a`.`ClassHours` as char charset utf8),_utf8'课时') end) AS `Flow`,`b`.`CardNo` AS `CardNo`,`b`.`CardType` AS `CardType`,`b`.`RealName` AS `RealName`,`b`.`Nickname` AS `Nickname`,`b`.`Amount` AS `Amount`,`b`.`Guardian` AS `Guardian`,`b`.`CreatorName` AS `CreatorName`,`b`.`CardTypeName` AS `CardTypeName`,`b`.`MemberGuid` AS `MemberGuid`,`b`.`Mobile` AS `Mobile`,`b`.`MemberStatus` AS `MemberStatus` from (`cardtransform` `a` left join `q_card` `b` on((`b`.`CardGuid` = `a`.`CardGuid`))) */;

--
-- Final view structure for view `q_contract`
--

/*!50001 DROP TABLE `q_contract`*/;
/*!50001 DROP VIEW IF EXISTS `q_contract`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_contract` AS select `a`.`ContractGuid` AS `ContractGuid`,`a`.`ContractNum` AS `ContractNum`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`ClassHourName` AS `ClassHourName`,`a`.`ClassHours` AS `ClassHours`,`a`.`amount` AS `amount`,`a`.`LeaveDays` AS `LeaveDays`,`a`.`StartDate` AS `StartDate`,`a`.`EndDate` AS `EndDate`,`a`.`SignDate` AS `SignDate`,`a`.`Attachment` AS `Attachment`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`Notes` AS `Notes`,`a`.`RefundNotes` AS `RefundNotes`,`a`.`DiscardNotes` AS `DiscardNotes`,`a`.`DoStatus` AS `DoStatus`,`a`.`ContractType` AS `ContractType`,`a`.`LastDoTime` AS `LastDoTime`,`a`.`SalemanGuid` AS `SalemanGuid`,`a`.`YAmount` AS `YAmount`,`a`.`ComboType` AS `ComboType`,`a`.`ContractDepositGuid` AS `ContractDepositGuid`,`a`.`CheckUserGuid` AS `CheckUserGuid`,`a`.`CheckDate` AS `CheckDate`,`a`.`CheckNotes` AS `CheckNotes`,`a`.`PayTypeName` AS `PayTypeName`,`a`.`IsPosPay` AS `IsPosPay`,`a`.`PosPayAmount` AS `PosPayAmount`,`a`.`Discount` AS `Discount`,`a`.`ChangePoints` AS `ChangePoints`,`a`.`Saleman2Guid` AS `Saleman2Guid`,`a`.`BuyClassHours` AS `BuyClassHours`,`a`.`GiftClassHours` AS `GiftClassHours`,`a`.`AverageMode` AS `AverageMode`,`a`.`IsNewMode` AS `IsNewMode`,`a`.`PayStatus` AS `PayStatus`,`a`.`CLevel` AS `CLevel`,`a`.`Duration` AS `Duration`,`a`.`Frequency` AS `Frequency`,`a`.`ClassPeriod` AS `ClassPeriod`,`a`.`CourseSeries` AS `CourseSeries`,`a`.`SalemanShare` AS `SalemanShare`,`a`.`Saleman2Share` AS `Saleman2Share`,`f`.`UserName` AS `SalemanName`,`i`.`UserName` AS `Saleman2Name`,`b`.`UserName` AS `CreatorName`,`c`.`RealName` AS `BabyName`,`c`.`Mobile` AS `Mobile`,`c`.`managerguids` AS `ManagerGuids`,`c`.`managernames` AS `ManagerNames`,`c`.`advisornames` AS `advisornames`,`c`.`teachernames` AS `teachernames`,`d`.`ParamName` AS `ContractStatus`,`e`.`ParamName` AS `ContractTypeName`,`c`.`DoStatus` AS `MemberStatus`,`g`.`UserName` AS `CheckUserName`,ifnull(`h`.`Amount`,0) AS `DepositAmount`,`h`.`PayTypeName` AS `DepositPayType`,(case when (date_format(now(),_utf8'%Y-%m-%d') < `a`.`StartDate`) then ((to_days(`a`.`EndDate`) - to_days(`a`.`StartDate`)) + 1) when (date_format(now(),_utf8'%Y-%m-%d') > `a`.`EndDate`) then 0 else ((to_days(`a`.`EndDate`) - to_days(date_format(now(),_utf8'%Y-%m-%d'))) + 1) end) AS `ContractLeftDays` from ((((((((`contract` `a` left join `k_manager` `b` on((`a`.`CreatorGuid` = `b`.`ManagerGUID`))) left join `q_member` `c` on((`a`.`MemberGuid` = `c`.`MemberGuid`))) left join `k_systemparam` `d` on((`a`.`DoStatus` = `d`.`ID`))) left join `k_systemparam` `e` on((`a`.`ContractType` = `e`.`ID`))) left join `k_manager` `f` on((`a`.`SalemanGuid` = `f`.`ManagerGUID`))) left join `k_manager` `i` on((`a`.`Saleman2Guid` = `i`.`ManagerGUID`))) left join `k_manager` `g` on((`a`.`CheckUserGuid` = `g`.`ManagerGUID`))) left join `contractdeposit` `h` on((`h`.`ContractGuid` = `a`.`ContractGuid`))) */;

--
-- Final view structure for view `q_course`
--

/*!50001 DROP TABLE `q_course`*/;
/*!50001 DROP VIEW IF EXISTS `q_course`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_course` AS select `a`.`CourseGuid` AS `CourseGuid`,`a`.`CourseName` AS `CourseName`,`a`.`CourseDate` AS `CourseDate`,`a`.`ClassSectionGuid` AS `ClassSectionGuid`,`a`.`ClassroomGuid` AS `ClassroomGuid`,`a`.`LessonGuid` AS `LessonGuid`,`a`.`Teacher` AS `Teacher`,`a`.`Assistant` AS `Assistant`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`ShowColor` AS `ShowColor`,`b`.`ClassroomName` AS `ClassroomName`,`c`.`ClassSectionName` AS `ClassSectionName`,`c`.`StartTime` AS `StartTime`,`c`.`EndTime` AS `EndTime`,concat(`c`.`StartTime`,_utf8'-',`c`.`EndTime`) AS `ClassSectionTime`,`d`.`MemberCount` AS `MemberCount`,`d`.`FreeCount` AS `FreeCount`,`d`.`ClassHours` AS `ClassHours`,`d`.`Price` AS `Price`,`d`.`LessonName` AS `LessonName`,`d`.`FitAgeFrom` AS `FitAgeFrom`,`d`.`FitAgeTo` AS `FitAgeTo`,`g`.`LessonSeriesName` AS `LessonSeriesName` from ((((`course` `a` left join `classroom` `b` on((`a`.`ClassroomGuid` = `b`.`ClassroomGuid`))) left join `classsection` `c` on((`a`.`ClassSectionGuid` = `c`.`ClassSectionGuid`))) left join `lesson` `d` on((`a`.`LessonGuid` = `d`.`LessonGuid`))) left join `lessonseries` `g` on((`d`.`LessonSeriesGuid` = `g`.`LessonSeriesGuid`))) */;

--
-- Final view structure for view `q_courseanddocourseautosendmsg`
--

/*!50001 DROP TABLE `q_courseanddocourseautosendmsg`*/;
/*!50001 DROP VIEW IF EXISTS `q_courseanddocourseautosendmsg`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_courseanddocourseautosendmsg` AS select `course`.`CourseDate` AS `CourseDate`,`classsection`.`StartTime` AS `StartTime`,`member`.`Mobile` AS `Mobile`,`lesson`.`LessonName` AS `LessonName`,`classsection`.`ClassSectionName` AS `ClassSectionName`,`classroom`.`ClassroomName` AS `ClassroomName`,`member`.`RealName` AS `RealName`,`member`.`Nickname` AS `Nickname`,`member`.`Guardian` AS `Guardian`,`classsection`.`TimeLen` AS `TimeLen`,_utf8'Course' AS `Type`,str_to_date(concat(date_format(`course`.`CourseDate`,_utf8'%Y-%m-%d'),_utf8' ',`classsection`.`StartTime`),_utf8'%Y-%m-%d %k:%i') AS `CourseStartTime` from (((((`membercourse` left join `member` on((`membercourse`.`MemberGuid` = `member`.`MemberGuid`))) left join `course` on((`membercourse`.`CourseGuid` = `course`.`CourseGuid`))) left join `lesson` on((`lesson`.`LessonGuid` = `course`.`LessonGuid`))) left join `classsection` on((`course`.`ClassSectionGuid` = `classsection`.`ClassSectionGuid`))) left join `classroom` on((`course`.`ClassroomGuid` = `classroom`.`ClassroomGuid`))) where (((to_days(`course`.`CourseDate`) - to_days(curdate())) = 0) and (`membercourse`.`DoStatus` <> 42)) */;

--
-- Final view structure for view `q_coursedayreport`
--

/*!50001 DROP TABLE `q_coursedayreport`*/;
/*!50001 DROP VIEW IF EXISTS `q_coursedayreport`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_coursedayreport` AS select `a`.`CourseGuid` AS `CourseGuid`,date_format(`a`.`CourseDate`,_utf8'%Y-%m-%d') AS `CourseDate`,`ww`.`weedName` AS `weekDay`,concat(`b`.`StartTime`,_utf8'-',`b`.`EndTime`) AS `TimeSpan`,`g`.`ClassroomName` AS `ClassroomName`,`a`.`CourseName` AS `CourseName`,`c`.`LessonName` AS `LessonName`,`a`.`Teacher` AS `TeacherName`,`a`.`Assistant` AS `AssistantName`,`c`.`ClassHours` AS `ClassHours`,`m`.`c` AS `YYHY`,`n`.`c` AS `SJSKHY`,`o`.`c` AS `YYTY`,`p`.`c` AS `SJTY`,`q`.`c` AS `QingJia`,`u`.`c` AS `KuangKe`,(case when ((ifnull(`m`.`c`,0) + ifnull(`o`.`c`,0)) = 0) then _utf8'' else concat(cast(round((round(((ifnull(`n`.`c`,0) + ifnull(`p`.`c`,0)) / (ifnull(`m`.`c`,0) + ifnull(`o`.`c`,0))),3) * 100),1) as char(20) charset utf8),_utf8'%') end) AS `cql`,(case when (ifnull(`m`.`c`,0) = 0) then _utf8'' else concat(cast(round((round((ifnull(`n`.`c`,0) / ifnull(`m`.`c`,0)),3) * 100),1) as char(20) charset utf8),_utf8'%') end) AS `hycql` from (((((((((((`course` `a` left join `r_course_week` `ww` on((`ww`.`weedNum` = dayofweek(`a`.`CourseDate`)))) left join `classsection` `b` on((`a`.`ClassSectionGuid` = `b`.`ClassSectionGuid`))) left join `lesson` `c` on((`a`.`LessonGuid` = `c`.`LessonGuid`))) left join `lessonseries` `d` on((`c`.`LessonSeriesGuid` = `d`.`LessonSeriesGuid`))) left join `classroom` `g` on((`a`.`ClassroomGuid` = `g`.`ClassroomGuid`))) left join `q_coursedayreport_sub` `m` on(((`a`.`CourseGuid` = `m`.`CourseGuid`) and (`m`.`seltype` = _utf8'YYHY')))) left join `q_coursedayreport_sub` `n` on(((`a`.`CourseGuid` = `n`.`CourseGuid`) and (`n`.`seltype` = _utf8'SJSKHY')))) left join `q_coursedayreport_sub` `o` on(((`a`.`CourseGuid` = `o`.`CourseGuid`) and (`o`.`seltype` = _utf8'YYTY')))) left join `q_coursedayreport_sub` `p` on(((`a`.`CourseGuid` = `p`.`CourseGuid`) and (`p`.`seltype` = _utf8'SJTY')))) left join `q_coursedayreport_sub` `q` on(((`a`.`CourseGuid` = `q`.`CourseGuid`) and (`q`.`seltype` = _utf8'QingJia')))) left join `q_coursedayreport_sub` `u` on(((`a`.`CourseGuid` = `u`.`CourseGuid`) and (`u`.`seltype` = _utf8'KuangKe')))) */;

--
-- Final view structure for view `q_coursedayreport_sub`
--

/*!50001 DROP TABLE `q_coursedayreport_sub`*/;
/*!50001 DROP VIEW IF EXISTS `q_coursedayreport_sub`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_coursedayreport_sub` AS select `membercourse`.`CourseGuid` AS `CourseGuid`,count(`membercourse`.`MemberCourseGuid`) AS `c`,_utf8'YYHY' AS `seltype` from `membercourse` where (`membercourse`.`CourseType` = 0) group by `membercourse`.`CourseGuid` union all select `membercourse`.`CourseGuid` AS `CourseGuid`,count(`membercourse`.`MemberCourseGuid`) AS `c`,_utf8'SJSKHY' AS `seltype` from `membercourse` where (((`membercourse`.`DoStatus` = 39) or (`membercourse`.`DoStatus` = 40)) and (`membercourse`.`CourseType` = 0)) group by `membercourse`.`CourseGuid` union all select `membercourse_4`.`CourseGuid` AS `CourseGuid`,count(`membercourse_4`.`MemberCourseGuid`) AS `c`,_utf8'YYTY' AS `seltype` from `membercourse` `membercourse_4` where (`membercourse_4`.`CourseType` = 1) group by `membercourse_4`.`CourseGuid` union all select `membercourse`.`CourseGuid` AS `CourseGuid`,count(`membercourse`.`MemberCourseGuid`) AS `c`,_utf8'SJTY' AS `seltype` from `membercourse` where (((`membercourse`.`DoStatus` = 39) or (`membercourse`.`DoStatus` = 40)) and (`membercourse`.`CourseType` = 1)) group by `membercourse`.`CourseGuid` union all select `membercourse`.`CourseGuid` AS `CourseGuid`,count(`membercourse`.`MemberCourseGuid`) AS `c`,_utf8'QingJia' AS `seltype` from `membercourse` where (`membercourse`.`DoStatus` = 42) group by `membercourse`.`CourseGuid` union all select `membercourse`.`CourseGuid` AS `CourseGuid`,count(`membercourse`.`MemberCourseGuid`) AS `c`,_utf8'KuangKe' AS `seltype` from `membercourse` where (`membercourse`.`DoStatus` = 41) group by `membercourse`.`CourseGuid` */;

--
-- Final view structure for view `q_courselist`
--

/*!50001 DROP TABLE `q_courselist`*/;
/*!50001 DROP VIEW IF EXISTS `q_courselist`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_courselist` AS select `a`.`CourseListGuid` AS `CourseListGuid`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`WaitType` AS `WaitType`,`a`.`WaitCourseGuid` AS `WaitCourseGuid`,`a`.`WaitLessonGuid` AS `WaitLessonGuid`,`a`.`SortID` AS `sortid`,`a`.`CourseType` AS `coursetype`,`a`.`CourseGuid` AS `CourseGuid`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`DoStatus` AS `DoStatus`,`a`.`Notes` AS `Notes`,`b`.`RealName` AS `membername`,`b`.`Nickname` AS `Nickname`,`b`.`BirthDate` AS `BirthDate`,`b`.`Guardian` AS `Guardian`,`b`.`Mobile` AS `Mobile`,`b`.`DoStatus` AS `MemberDoStatus`,`c`.`CourseDate` AS `WCourseDate`,`c`.`ClassSectionTime` AS `WClassSectionTime`,`c`.`ClassroomName` AS `WClassroomName`,`c`.`LessonName` AS `WLessonName`,`d`.`LessonName` AS `WaitLessonName`,`e`.`CourseDate` AS `RCourseDate`,`e`.`ClassSectionTime` AS `RClassSectionTime`,`e`.`ClassroomName` AS `RClassroomName`,`e`.`LessonName` AS `RLessonName`,`f`.`UserName` AS `CreatorName` from (((((`courselist` `a` left join `member` `b` on((`a`.`MemberGuid` = `b`.`MemberGuid`))) left join `q_course` `c` on((`c`.`CourseGuid` = `a`.`WaitCourseGuid`))) left join `lesson` `d` on((`d`.`LessonGuid` = `a`.`WaitLessonGuid`))) left join `q_course` `e` on((`a`.`CourseGuid` = `e`.`CourseGuid`))) left join `k_manager` `f` on((`f`.`ManagerGUID` = `a`.`CreatorGuid`))) */;

--
-- Final view structure for view `q_docourse`
--

/*!50001 DROP TABLE `q_docourse`*/;
/*!50001 DROP VIEW IF EXISTS `q_docourse`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_docourse` AS select `a`.`DoGuid` AS `DoGuid`,`a`.`DoTypeGuid` AS `DoTypeGuid`,`a`.`DoTitle` AS `DoTitle`,`a`.`DoContent` AS `DoContent`,`a`.`StartTime` AS `StartTime`,`a`.`EndTime` AS `EndTime`,`a`.`DoProperties` AS `DoProperties`,`a`.`ReduceHours` AS `ReduceHours`,`a`.`ReduceCost` AS `ReduceCost`,`a`.`Cost` AS `Cost`,`a`.`ClassroomGuid` AS `ClassroomGuid`,`a`.`Address` AS `Address`,`a`.`TeacherGuid` AS `TeacherGuid`,`a`.`AssistantGuid` AS `AssistantGuid`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`LessonSeriesGuids` AS `LessonSeriesGuids`,`a`.`MemberCount` AS `MemberCount`,`a`.`Notes` AS `Notes`,`a`.`Notes1` AS `Notes1`,`a`.`Notes2` AS `Notes2`,`a`.`pictures` AS `Pictures`,`a`.`WxLimit` AS `WxLimit`,`a`.`PayType` AS `PayType`,`c`.`DoTypeName` AS `dotypename`,`b`.`ClassroomName` AS `ClassroomName`,`d`.`UserName` AS `TeacherName`,`e`.`UserName` AS `AssistantName`,`f`.`UserName` AS `CreatorName`,`a`.`DoBudget` AS `DoBudget`,`a`.`DoIncome` AS `DoIncome`,`a`.`ManagerGuids` AS `ManagerGuids`,`a`.`ManagerNames` AS `ManagerNames`,`g`.`membernum` AS `membernum`,`g`.`sign` AS `sign`,`g`.`charge` AS `charge`,`g`.`ReduceHoursCount` AS `ReduceHoursCount` from ((((((`docourse` `a` left join `classroom` `b` on((`a`.`ClassroomGuid` = `b`.`ClassroomGuid`))) left join `dotype` `c` on((`c`.`DoTypeGuid` = `a`.`DoTypeGuid`))) left join `k_manager` `d` on((`d`.`ManagerGUID` = `a`.`TeacherGuid`))) left join `k_manager` `e` on((`e`.`ManagerGUID` = `a`.`AssistantGuid`))) left join `k_manager` `f` on((`f`.`ManagerGUID` = `a`.`CreatorGuid`))) left join `q_docoursemember` `g` on((`g`.`DoCourseGuid` = `a`.`DoGuid`))) */;

--
-- Final view structure for view `q_docoursemember`
--

/*!50001 DROP TABLE `q_docoursemember`*/;
/*!50001 DROP VIEW IF EXISTS `q_docoursemember`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_docoursemember` AS select `memberdocourse`.`DoCourseGuid` AS `DoCourseGuid`,count(1) AS `membernum`,sum(`memberdocourse`.`DoStatus`) AS `sign`,sum((`memberdocourse`.`ReduceCost` + `memberdocourse`.`Cost`)) AS `charge`,sum(`memberdocourse`.`ReduceHours`) AS `ReduceHoursCount` from `memberdocourse` group by `memberdocourse`.`DoCourseGuid` */;

--
-- Final view structure for view `q_leave`
--

/*!50001 DROP TABLE `q_leave`*/;
/*!50001 DROP VIEW IF EXISTS `q_leave`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_leave` AS select `a`.`LeaveGuid` AS `LeaveGuid`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`CourseGuid` AS `CourseGuid`,`a`.`LeaveType` AS `LeaveType`,`a`.`Reason` AS `Reason`,`a`.`StartTime` AS `StartTime`,`a`.`EndTime` AS `EndTime`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`Note` AS `Note`,`b`.`UserName` AS `CreatorName`,`c`.`RealName` AS `RealName`,`c`.`Nickname` AS `Nickname`,`c`.`Guardian` AS `Guardian`,`c`.`Sex` AS `Sex`,`c`.`BirthDate` AS `BirthDate`,`c`.`Mobile` AS `Mobile`,`e`.`CourseName` AS `CourseName`,`e`.`CourseDate` AS `CourseDate`,`e`.`LessonName` AS `LessonName`,`e`.`ClassSectionTime` AS `ClassSectionTime`,`e`.`ClassroomName` AS `ClassroomName`,`e`.`LessonGuid` AS `LessonGuid`,`d`.`ReduceHours` AS `ReduceHours`,`d`.`CourseType` AS `CourseType`,`d`.`DoStatus` AS `DoStatus`,`f`.`ParamName` AS `SignStatus`,`g`.`ParamName` AS `MemberStatus` from ((((((`leave` `a` left join `k_manager` `b` on((`a`.`CreatorGuid` = `b`.`ManagerGUID`))) join `member` `c` on((`c`.`MemberGuid` = `a`.`MemberGuid`))) left join `membercourse` `d` on(((`a`.`CourseGuid` = `d`.`CourseGuid`) and (`a`.`MemberGuid` = `d`.`MemberGuid`)))) left join `q_course` `e` on((`a`.`CourseGuid` = `e`.`CourseGuid`))) left join `k_systemparam` `f` on((`f`.`ID` = `d`.`DoStatus`))) left join `k_systemparam` `g` on((`g`.`ID` = `c`.`DoStatus`))) */;

--
-- Final view structure for view `q_member`
--

/*!50001 DROP TABLE `q_member`*/;
/*!50001 DROP VIEW IF EXISTS `q_member`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_member` AS select `a`.`ID` AS `ID`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`RealName` AS `RealName`,`a`.`Nickname` AS `NickName`,`a`.`Guardianship` AS `Guardianship`,`a`.`Guardian` AS `Guardian`,`a`.`Sex` AS `Sex`,`a`.`BirthDate` AS `BirthDate`,`a`.`Address` AS `Address`,`a`.`Phone` AS `Phone`,`a`.`Mobile` AS `Mobile`,`a`.`Mobile1` AS `Mobile1`,`a`.`Msn` AS `Msn`,`a`.`QQ` AS `QQ`,`a`.`Email` AS `Email`,`a`.`photo` AS `Photo`,`a`.`FacePhoto` AS `FacePhoto`,`a`.`UnRecognizeFacePhoto` AS `UnRecognizeFacePhoto`,`a`.`basicinfo` AS `BasicInfo`,`a`.`VisitInfo` AS `VisitInfo`,`a`.`ExperienceInfo` AS `ExperienceInfo`,`a`.`CurrentLevel` AS `CurrentLevel`,`a`.`Scope` AS `Scope`,`a`.`IsVisited` AS `IsVisited`,`a`.`SignDate` AS `SignDate`,`a`.`AreaGuid` AS `AreaGuid`,`a`.`intentiondate` AS `intentiondate`,`a`.`MemberType` AS `MemberType`,(case when (date_format(`a`.`SignDate`,_utf8'%Y-%m-%d') = _utf8'1900-01-01') then 0 else (to_days(`a`.`SignDate`) - to_days(`a`.`CreateTime`)) end) AS `ConvertCycle`,`a`.`Notes` AS `Notes`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`DoStatus` AS `DoStatus`,`a`.`SourceGuid` AS `SourceGuid`,`a`.`BirthMode` AS `BirthMode`,`a`.`ConsultingGuid` AS `consultingGuid`,`a`.`ImportBatchGuid` AS `ImportBatchGuid`,`a`.`MktStaffGuid` AS `MktStaffGuid`,`a`.`IntentionLesson` AS `IntentionLesson`,`a`.`ImportantLevel` AS `ImportantLevel`,`a`.`LastCourseDate` AS `LastCourseDate`,`a`.`MarketNodeGuid` AS `MarketNodeGuid`,`a`.`Marks` AS `Marks`,`b`.`ManagerGuids` AS `managerguids`,`b`.`ManagerNames` AS `managernames`,`b`.`AdvisorNames` AS `advisornames`,`b`.`TeacherNames` AS `teachernames`,`a`.`ExperienceDate` AS `ExperienceDate`,`a`.`VisitDate` AS `VisitDate`,`a`.`IsExperienced` AS `IsExperienced`,`a`.`WXUserName` AS `WXUserName`,`a`.`WXOpenID` AS `WXOpenID`,`a`.`mobileLocation` AS `MobileLocation`,`c`.`NodeName` AS `NodeName`,`d`.`ParamName` AS `MemberStatus`,`f`.`SourceName` AS `SourceName`,`g`.`ParamName` AS `ImportantLevelName`,`h`.`UserName` AS `MktStaffName`,`i`.`BatchTitle` AS `BatchTitle`,`j`.`AssignCount` AS `AssignCount`,`j`.`LastAssignTime` AS `LastAssignTime`,`j`.`FirstFollowTime` AS `FirstFollowTime`,`j`.`LastFollowTime` AS `LastFollowTime`,`j`.`LastFollowContent` AS `LastFollowContent`,`j`.`FollowCount` AS `FollowCount`,`j`.`CijinFollowTime` AS `CijinFollowTime`,`j`.`CijinFollowContent` AS `CijinFollowContent`,`j`.`NextFollowTime` AS `NextFollowTime`,`j`.`NowLessonNames` AS `NowLessonNames`,`j`.`NowLessonGuids` AS `NowLessonGuids`,`j`.`FirstFollowContent` AS `FirstFollowContent` from ((((((((`member` `a` left join `membermanagertemp` `b` on((`a`.`MemberGuid` = `b`.`MemberGuid`))) left join `marketnode` `c` on((`a`.`MarketNodeGuid` = `c`.`NodeGuid`))) left join `k_systemparam` `d` on((`a`.`DoStatus` = `d`.`ID`))) left join `membersource` `f` on((`a`.`SourceGuid` = `f`.`MemberSourceGuid`))) left join `paramconfig` `g` on((`a`.`ImportantLevel` = `g`.`ParamGuid`))) left join `k_manager` `h` on((`h`.`ManagerGUID` = `a`.`MktStaffGuid`))) left join `importbatch` `i` on((`i`.`BatchGuid` = `a`.`ImportBatchGuid`))) left join `membertemp` `j` on((`a`.`MemberGuid` = `j`.`MemberGuid`))) */;

--
-- Final view structure for view `q_memberassign`
--

/*!50001 DROP TABLE `q_memberassign`*/;
/*!50001 DROP VIEW IF EXISTS `q_memberassign`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_memberassign` AS select `a`.`MemberAssignGuid` AS `MemberAssignGuid`,`a`.`MemberGuid` AS `MemberGuid`,`b`.`ID` AS `ID`,`a`.`RelationType` AS `RelationType`,`a`.`OperatorGuid` AS `OperatorGuid`,`a`.`OperateTime` AS `OperateTime`,`a`.`Notes` AS `Notes`,`b`.`RealName` AS `RealName`,`b`.`Guardian` AS `Guardian`,`b`.`Mobile` AS `Mobile`,`c`.`UserName` AS `OperatorName`,`a`.`OldManagerNames` AS `OldManagerNames`,`a`.`newManagerNames` AS `NewManagerNames`,`b`.`Sex` AS `Sex`,`a`.`MemberAssignBatchGuid` AS `MemberAssignBatchGuid` from ((`memberassign` `a` left join `member` `b` on((`a`.`MemberGuid` = `b`.`MemberGuid`))) left join `k_manager` `c` on((`a`.`OperatorGuid` = `c`.`ManagerGUID`))) */;

--
-- Final view structure for view `q_memberclasshours`
--

/*!50001 DROP TABLE `q_memberclasshours`*/;
/*!50001 DROP VIEW IF EXISTS `q_memberclasshours`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_memberclasshours` AS select `m`.`MemberGuid` AS `MemberGuid`,ifnull(sum(`n`.`CurrentClassHours`),0) AS `CurrentClassHours` from (`membercard` `m` left join `q_cardclasshours` `n` on((`m`.`CardGuid` = `n`.`CardGuid`))) group by `m`.`MemberGuid` */;

--
-- Final view structure for view `q_membercourse`
--

/*!50001 DROP TABLE `q_membercourse`*/;
/*!50001 DROP VIEW IF EXISTS `q_membercourse`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_membercourse` AS select `a`.`MemberCourseGuid` AS `MemberCourseGuid`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`CourseGuid` AS `CourseGuid`,`a`.`CourseType` AS `CourseType`,`a`.`DoStatus` AS `DoStatus`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`ReduceHours` AS `ReduceHours`,`a`.`ClassHourType` AS `ClassHourType`,`a`.`Cost` AS `Cost`,`a`.`IsFixed` AS `IsFixed`,`a`.`SignTime` AS `SignTime`,`a`.`CardGuid` AS `CardGuid`,`a`.`LessonSeriesGuid` AS `LessonSeriesGuid`,`a`.`ChangePoints` AS `ChangePoints`,`a`.`MakeUp` AS `MakeUp`,`a`.`FeedBackInfo` AS `FeedbackInfo`,`a`.`SortID` AS `SortID`,`a`.`pictures` AS `Pictures`,`b`.`NickName` AS `Nickname`,`b`.`RealName` AS `RealName`,`b`.`Guardian` AS `Guardian`,`b`.`Mobile` AS `Mobile`,`b`.`WXOpenID` AS `WXOpenID`,`b`.`BirthDate` AS `BirthDate`,`b`.`Sex` AS `Sex`,`b`.`advisornames` AS `AdvisorNames`,`b`.`teachernames` AS `TeacherNames`,`b`.`managernames` AS `ManagerNames`,`b`.`Scope` AS `Scope`,`c`.`CourseName` AS `CourseName`,`c`.`CourseDate` AS `CourseDate`,`c`.`ClassroomName` AS `ClassroomName`,`c`.`ClassroomGuid` AS `classroomguid`,`c`.`ClassSectionGuid` AS `ClassSectionGuid`,`c`.`ClassSectionName` AS `ClassSectionName`,`c`.`StartTime` AS `StartTime`,`c`.`EndTime` AS `EndTime`,`c`.`ClassSectionTime` AS `ClassSectionTime`,`c`.`LessonGuid` AS `LessonGuid`,`c`.`LessonName` AS `LessonName`,`c`.`MemberCount` AS `MemberCount`,`c`.`FreeCount` AS `FreeCount`,`c`.`ClassHours` AS `ClassHours`,`c`.`Teacher` AS `Teacher`,`c`.`Assistant` AS `Assistant`,`c`.`LessonSeriesName` AS `LessonSeriesName`,`d`.`ParamName` AS `SignStatus`,`b`.`DoStatus` AS `MemberStatus`,`e`.`UserName` AS `CreatorName`,`a`.`ContractNos` AS `ContractNos`,`a`.`ReduceGiftClassHours` AS `ReduceGiftClassHours`,`a`.`ReduceBuyClassHours` AS `ReduceBuyClassHours`,`a`.`HomeworkStatus` AS `HomeworkStatus` from ((((`membercourse` `a` left join `q_member` `b` on((`a`.`MemberGuid` = `b`.`MemberGuid`))) left join `q_course` `c` on((`a`.`CourseGuid` = `c`.`CourseGuid`))) left join `k_systemparam` `d` on((`a`.`DoStatus` = `d`.`ID`))) left join `k_manager` `e` on((`a`.`CreatorGuid` = `e`.`ManagerGUID`))) */;

--
-- Final view structure for view `q_memberdocourse`
--

/*!50001 DROP TABLE `q_memberdocourse`*/;
/*!50001 DROP VIEW IF EXISTS `q_memberdocourse`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `q_memberdocourse` AS select `a`.`MemberDoCourseGuid` AS `MemberDoCourseGuid`,`a`.`MemberGuid` AS `MemberGuid`,`a`.`DoCourseGuid` AS `DoCourseGuid`,`a`.`DoCourseType` AS `DoCourseType`,`a`.`DoStatus` AS `DoStatus`,`a`.`CreateTime` AS `CreateTime`,`a`.`CreatorGuid` AS `CreatorGuid`,`a`.`ReduceHours` AS `ReduceHours`,`a`.`ReduceCost` AS `ReduceCost`,`a`.`Cost` AS `Cost`,`a`.`ReduceType` AS `ReduceType`,`a`.`CardGuid` AS `CardGuid`,`a`.`LessonSeriesGuid` AS `LessonSeriesGuid`,`a`.`SignTime` AS `SignTime`,`a`.`ChangePoints` AS `ChangePoints`,`a`.`WasteBookGuid` AS `WasteBookGuid`,`b`.`NickName` AS `Nickname`,`b`.`RealName` AS `RealName`,`b`.`Guardian` AS `Guardian`,`b`.`Mobile` AS `Mobile`,`b`.`BirthDate` AS `BirthDate`,`b`.`Sex` AS `Sex`,`b`.`SourceName` AS `SourceName`,concat(`c`.`StartTime`,_utf8' 至 ',`c`.`EndTime`) AS `docoursetime`,`c`.`ClassroomName` AS `ClassroomName`,`c`.`DoTitle` AS `DoTitle`,`c`.`DoProperties` AS `DoProperties`,`d`.`ParamName` AS `ParamName`,`b`.`DoStatus` AS `MemberStatus`,`b`.`advisornames` AS `AdvisorNames`,`b`.`managernames` AS `ManagerNames`,`b`.`teachernames` AS `TeacherNames`,`c`.`TeacherName` AS `MainTeacher`,`c`.`StartTime` AS `StartTime`,`c`.`EndTime` AS `EndTime`,`c`.`Address` AS `Address`,`a`.`ContractNos` AS `ContractNos`,`a`.`ReduceGiftClassHours` AS `ReduceGiftClassHours`,`a`.`ReduceBuyClassHours` AS `ReduceBuyClassHours`,`a`.`PayStatus` AS `PayStatus` from (((`memberdocourse` `a` left join `q_member` `b` on((`a`.`MemberGuid` = `b`.`MemberGuid`))) left join `q_docourse` `c` on((`a`.`DoCourseGuid` = `c`.`DoGuid`))) left join `k_systemparam` `d` on((`a`.`DoStatus` = `d`.`ID`))) */;

--
-- Final view structure for view `q_product`
--

/*!50001 DROP TABLE `q_product`*/;
/*!50001 DROP VIEW IF EXISTS `q_product`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_product` AS select `a`.`ProductName` AS `ProductName`,`a`.`ProductCode` AS `ProductCode`,`a`.`ProductGuid` AS `ProductGuid`,`a`.`PurchasePrice` AS `PurchasePrice`,`a`.`SalePrice` AS `SalePrice`,`a`.`InventoryAmount` AS `InventoryAmount`,(case when (`a`.`CanExchangePoint` = 1) then _utf8'是' else _utf8'否' end) AS `CanExchangePoint`,`a`.`ExchangePoints` AS `ExchangePoints`,`a`.`CreateTime` AS `CreateTime`,`a`.`Notes` AS `Notes`,`b`.`CategoryName` AS `CategoryName`,`c`.`UserName` AS `CreatorName`,`a`.`ProductCategoryGuid` AS `ProductCategoryGuid`,`a`.`DoStatus` AS `DoStatus`,`a`.`ISMallProduct` AS `ISMallProduct`,`a`.`Discount` AS `Discount` from ((`product` `a` left join `productcategory` `b` on((`a`.`ProductCategoryGuid` = `b`.`ProductCategoryGuid`))) left join `k_manager` `c` on((`a`.`CreatorGuid` = `c`.`ManagerGUID`))) */;

--
-- Final view structure for view `q_productinstore`
--

/*!50001 DROP TABLE `q_productinstore`*/;
/*!50001 DROP VIEW IF EXISTS `q_productinstore`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`%` SQL SECURITY DEFINER */
/*!50001 VIEW `q_productinstore` AS select `a`.`Amount` AS `Amount`,`a`.`CreateTime` AS `CreateTime`,`a`.`InStoreGuid` AS `InStoreGuid`,`a`.`ProductGuid` AS `ProductGuid`,`a`.`DoStatus` AS `DoStatus`,`a`.`Notes` AS `Notes`,`a`.`PurchasePrice` AS `PurchasePrice`,`b`.`CanExchangePoint` AS `CanExchangePoint`,`b`.`ImgPath` AS `ImgPath`,`b`.`InventoryAmount` AS `InventoryAmount`,`b`.`ProductName` AS `ProductName`,`b`.`SalePrice` AS `SalePrice`,`b`.`ProductCode` AS `ProductCode`,`b`.`ProductCategoryGuid` AS `ProductCategoryGuid`,`c`.`UserName` AS `CreatorName`,`d`.`CategoryName` AS `CategoryName` from (((`productinstore` `a` left join `product` `b` on((`b`.`ProductGuid` = `a`.`ProductGuid`))) left join `k_manager` `c` on((`c`.`ManagerGUID` = `a`.`CreatorGuid`))) left join `productcategory` `d` on((`d`.`ProductCategoryGuid` = `b`.`ProductCategoryGuid`))) */;

--
-- Final view structure for view `r_course_week`
--

/*!50001 DROP TABLE `r_course_week`*/;
/*!50001 DROP VIEW IF EXISTS `r_course_week`*/;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `r_course_week` AS select 1 AS `weedNum`,_utf8'星期天' AS `weedName` union select 2 AS `weedNum`,_utf8'星期一' AS `weedName` union select 3 AS `weedNum`,_utf8'星期二' AS `weedName` union select 4 AS `weedNum`,_utf8'星期三' AS `weedName` union select 5 AS `weedNum`,_utf8'星期四' AS `weedName` union select 6 AS `weedNum`,_utf8'星期五' AS `weedName` union select 7 AS `weedNum`,_utf8'星期六' AS `weedName` */;

--
-- Current Database: `mysql`
--

USE `mysql`;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-11 13:19:26
