CREATE DATABASE IF NOT EXISTS `postquote_scraper`;

CREATE TABLE IF NOT EXISTS `pqs_mentions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `threadid` int(11) NOT NULL,
  `mentionedin` int(11) NOT NULL,
  `mentiontime` datetime NOT NULL,
  `alias` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `userID` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `pqs_threadlist` (
  `threadid` int(11) NOT NULL,
  `status` tinyint(1) DEFAULT NULL,
  UNIQUE KEY `threadid` (`threadid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
  
CREATE TABLE IF NOT EXISTS `pqs_userlist` (
  `userid` int(11) NOT NULL,
  `username` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`userid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;