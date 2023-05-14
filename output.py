import os
import datetime
from database import Database
from config import *

def logfile(prefix, data):
    folder_path = 'logs'
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{prefix}_{timestamp}.txt'

    # Create the folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Text file path
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(data)

def buildList(data):

    result = ""

    for i, row in enumerate(data):

        userid      =   str(row[5])
        username    =   row[6]
        if not (data[i][5] == data[i-1][5]):
            userlink    =   "[MENTION=" + userid + "][B]" + username + "[/B][/MENTION]"
        else:
            userlink = " "

        alias       =   row[4]
        dateposted  =   row[3].strftime("%B %d, %Y")
        postnumber  =   str(row[2])
        threadlink  =   "[URL=\"https://forums.example.com/showthread.php/?p=" + postnumber + "#post" + postnumber + "\"][B]" + alias + "[/B][/URL]"

        result += userlink     + "[indent]aka "
        result += threadlink
        result += "[/indent]\n"

    return result
# Connect to DB
db = Database(host="localhost", user="root", password="", database="postquote_scraper")

# Get the list of usernames/aliases
resultslist = db.getAliasList()

# Output the formatted usernames/aliases to file
logfile("post", buildList(resultslist))

# Disconnect from DB
db.disconnect()