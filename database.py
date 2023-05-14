import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        print("Connecting to database...")
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()

    def disconnect(self):
        self.cursor.close()
        self.connection.close()


    def isFinished(self, threadid):
        query = "SELECT * FROM `pqs_threadlist` WHERE `threadid` = (%s) AND `status` = 1 LIMIT 1"
        data = threadid

        self.cursor.execute(query, (data,))

        if self.cursor.fetchone() is not None:
            return True
        else:
            return False
        
    def markFinished(self, threadid):
        query = "UPDATE `pqs_threadlist` SET `status` = '1' WHERE `pqs_threadlist`.`threadid` = %s"
        data = threadid

        self.cursor.execute(query, (data,))
        self.connection.commit()

    def getAliasList(self):
        query = "SELECT m1.*, m2.`username` FROM `pqs_mentions` m1 JOIN `pqs_userlist` m2 ON m2.`userid` = m1.`userID` WHERE m1.`userID` IS NOT NULL AND (m1.`alias`, m1.`mentiontime`) IN (     SELECT `alias`, MIN(`mentiontime`) FROM `pqs_mentions` WHERE `userID` IS NOT NULL GROUP BY `alias` ) ORDER BY m2.`username` ASC, m1.`mentiontime` ASC"

        self.cursor.execute(query)

        results = self.cursor.fetchall()

        return results



    # Returns a list of unscraped threads from the database
    def getAllTargets(self):
        query = "SELECT `threadid` FROM `pqs_threadlist` WHERE `status` IS NULL"

        self.cursor.execute(query)

        results = self.cursor.fetchall()
        
        return list(map(lambda x: x[0], results))


    def getNextTarget(self):
        query = "SELECT * FROM `pqs_threadlist` WHERE `status` IS NULL LIMIT 1"

        self.cursor.execute(query,)

        threadid = self.cursor.fetchone()

        return threadid[0]
    
    def getProgressCount(self):
        query = "SELECT COUNT(CASE WHEN `status` IS NULL THEN 1 END) AS null_status_count, COUNT(*) AS total_rows_count FROM `pqs_threadlist`"

        self.cursor.execute(query,)

        count = self.cursor.fetchone()

        return count

    def addMention(self, mention):
        query = "INSERT INTO `pqs_mentions` (`threadid`, `mentionedin`, `mentiontime`, `alias`, `userID`) VALUES (%s, %s, %s, %s, %s)"
        data = tuple(mention.values())

        self.cursor.execute(query, data)
        self.connection.commit()

    def addActiveUser(self, userinfo):
        query = "INSERT IGNORE INTO `pqs_userlist` (`userID`, `username`) VALUES (%s, %s)"
        data = tuple(userinfo.values())

        self.cursor.execute(query, data)
        self.connection.commit()

    def addTargets(self, targets):
        query = "INSERT IGNORE INTO `pqs_threadlist` (`threadid`) VALUES (%s)"
        data = [(x,) for x in targets]

        self.cursor.executemany(query, data)
        self.connection.commit()

    def clearData(self):
        print("Truncating pqs_conflicts...")
        query = "TRUNCATE TABLE `pqs_threadlist`"
        self.cursor.execute(query)
        self.connection.commit()

        print("Truncating pqs_mentions...")
        query = "TRUNCATE TABLE `pqs_mentions`"
        self.cursor.execute(query)
        self.connection.commit()

        print("Truncating pqs_missing...")
        query = "TRUNCATE TABLE `pqs_userlist`"
        self.cursor.execute(query)
        self.connection.commit() 