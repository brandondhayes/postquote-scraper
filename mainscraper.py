import requests
import os
import datetime
from bs4 import BeautifulSoup
from config import *

# Get our soup
response = requests.get(basescanurl, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

postsDB = []
conflictDB = []

def getPageCount(soup):
    # Get the # of pages in the thread
    pagecount = soup.find('div', class_='pagination_top')
    pagecount = pagecount.find('a', class_='popupctrl')

    if pagecount is not None:
        pagecount = pagecount.get_text()
        pagecount = pagecount[10:]
    else:
        pagecount = 1

    return int(pagecount)

def logfile(prefix, data):
    folder_path = 'logs'
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{prefix}_{timestamp}.txt'

    # Create the folder if it does not exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    # Text file path
    file_path = os.path.join(folder_path, file_name)

    # Open the text file in write mode
    with open(file_path, 'w') as file:
        # Iterate through the dictionary array and write to the file
        for item in data:
            file.write(str(item) + '\n')

# Check if there are any other pages
pagecount = getPageCount(soup)

for i in range(pagecount):
    # Get all posts on page and save them to postsDB
    for post_element in soup.find_all('li', class_='postbitlegacy postbitim postcontainer old'):

        post = {
            'postid': post_element.get('id')[5:],
            'userid': post_element.find('a', class_='username offline popupctrl').get('href').split('/')[1].split('-')[0],
            'username': post_element.find('strong').get_text(),
        }
        postsDB.append(post)

    # Check for post quotes, look in postsDB to find a match and compare names
    for post_element in soup.find_all('div', class_='bbcode_postedby'):
        try:
            quote = {
                'postid': post_element.find('a').get('href').split('#post')[1],
                'alias': post_element.find('strong').get_text()
            }
        except:
            continue

        # Loop through postsDB and find a match where quote['postid'] == postsDB[i]['postid']
        for cached_post in postsDB:
            if quote['postid'] == cached_post['postid']:
                if cached_post['username'] != quote['alias']:
                    conflict = {
                        'postid': quote['postid'],
                        'userid': cached_post['userid'],
                        'username': cached_post['username'],
                        'alias': quote['alias']
                    }
                    conflictDB.append(conflict)

    # Scan the next page of the thread
    scanurl=f'{basescanurl}/page{i+1}'
    print(f'scanning page {i+1} of {pagecount}')
    response = requests.get(scanurl, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

# Save results to file
print(conflictDB)

# logfile('postsDB', postsDB)
logfile('conflictDB', conflictDB)