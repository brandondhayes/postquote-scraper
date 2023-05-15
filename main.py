import requests
import sys
import datetime
from tqdm import tqdm
from database import Database
from bs4 import BeautifulSoup
from config import *

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

def getSoup(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

BASE_URL = 'https://forums.example.com/showthread.php/'

db = Database(host="localhost", user="root", password="", database="postquote_scraper")

# Load all unscraped target threads from DB
targets = db.getAllTargets()

# Scan each thread in targets
for threadid in tqdm(targets, desc='Target Threads'):

    # Clear post cache
    postsDB = {}

    # Skip this thread if we already scanned it
    if db.isFinished(threadid) == True:
        continue

    # Get the first page
    targetURL = BASE_URL + str(threadid)
    soup = getSoup(targetURL)

    # Check if thread has multiple pages
    pagecount = getPageCount(soup)

    # Scan each page in target thread
    for i in tqdm(range(pagecount), desc='Thread Pages', leave=False):

        # Search individual posts
        for current_post in soup.find_all('li', class_='postbitlegacy postbitim postcontainer old'):

            # Cache the current post
            try:
                postid = int(current_post.get('id')[5:])
                userid = int(current_post.find('a', class_='username').get('href').split('/')[1].split('-')[0])
                username = current_post.find('strong').get_text()
                posttime = current_post.find('span', class_='date').get_text().replace('\xa0', ' ')
                posttime = datetime.datetime.strptime(posttime, "%m/%d/%Y, %I:%M %p").strftime("%Y-%m-%d %H:%M:%S")
            except:
                # Not a member, skip
                continue

            postsDB[postid] = {
                'userid':   userid,
                'username': username,
                'time':     posttime
            }


            content = current_post.find('div', class_='content')

            # Find all quote blocks in current post
            for quote_block in content.find_all('div', class_='bbcode_postedby'):

                # Try to get an alias and postid
                try:

                    quote_postid = int(quote_block.find('a').get('href').split('#post')[1])
                    quote_alias = quote_block.find('strong').get_text()
                    # quote = {
                    #     'postid':   int(quote_block.find('a').get('href').split('#post')[1]),
                    #     'alias':    quote_block.find('strong').get_text()
                    # }
                except:
                    # Bad quote block, ignore
                    continue

                if quote_postid in postsDB:
                    if quote_alias != postsDB[quote_postid]['username']:

                        # If name is different from current, log it
                        conflict = {
                            'threadid':     threadid,
                            'mentionedin':  postid,
                            'mentiontime':  posttime,
                            'alias':        quote_alias,
                            'userid':       postsDB[quote_postid]['userid']
                        }

                        # Record mention
                        db.addMention(conflict)

                        # Log the user's username as it exists today
                        activeuser = {
                            'userid':       postsDB[quote_postid]['userid'],
                            'username':     postsDB[quote_postid]['username']
                        }
                        db.addActiveUser(activeuser)

                else:

                    # Quote not found in thread or User/post deleted
                    missing = {
                        'threadid':     threadid,
                        'mentionedin':  postid,
                        'mentiontime':  posttime,
                        'alias':        quote_alias,
                        'userid':       None
                    }
                    db.addMention(missing)

        # If there are more pages remaining, get soup from next page
        if i < pagecount:
            nextURL=f'{targetURL}/page{i+2}'
            soup = soup = getSoup(nextURL)

    # Mark this target completed
    db.markFinished(threadid)

# Disconnect from DB
db.disconnect()