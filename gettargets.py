import requests
from database import Database
from bs4 import BeautifulSoup
from config import *

##########################################
# Define which threads we want to target
# for scraping post quotes
##########################################

BASE_URL = 'https://forums.example.com/forumdisplay.php/6'      # URL to subforum to scan
VARS_URL = '?pp=200'                                            # number of threads per page
pagecount = 41                                                   # max number of threads to scan

db = Database(host="localhost", user="root", password="", database="postquote_scraper")

targetsDB = []

for i in range(pagecount):

    print(f'Scanning page {i+1} of {pagecount}')
    targetURL = f'{BASE_URL}/page{i+1}{VARS_URL}'
    response = requests.get(targetURL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    targetsDB = []

    threadlist = soup.find('ol', class_='threads')
    threadlist = threadlist.find_all('li', id=lambda x: x and x.startswith('thread_'))

    for thread in threadlist:
        targetsDB.append(thread.get('id').split('_')[1])

    db.addTargets(targetsDB)
    print(tuple(targetsDB))
    print(f'finished page {i+1} of {pagecount}')

# Disconnect from DB
db.disconnect()