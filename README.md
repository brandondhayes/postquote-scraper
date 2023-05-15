# postquote-scraper

## Summary
This project scrapes a vBulletin forum to collect previously used usernames and associates them with a user ID.

## Files
`schema.sql` contains the database structure I used to store information scraped from the forum.

`database.py` contains the Database object I used to handle communcation between my local MySQL database and the Python script

`config.py` contains the cookie I used for forum authentication

`gettargets.py` contains the **first** script I used to gather target threadids for scraping. 

`main.py` contains the **second** script I used to scrape posts for quotes, using the threadid targets provided by `gettargets.py`

`output.py` contains the **third** script I used to build the finished output, formatted in BBCode


## Problem

Some years ago, a private vBulletin forum I frequented introduced a feature which allowed users to change their usernames. With no restriction on how often a user could change their username and no security features to stop members from changing their usernames to old usernames that other members previously used, this led to a great deal of chaos and confusion on the forum. Additionally, when a user performed a name change the username string associated with their account's user ID was updated directly, leaving no audit trail for a user's previous usernames.

During the chaos, I noticed that when a user would quote someone, the quote would show the username of the original poster at the time the post was quoted, rather than their live username as it currently exists. 
```
#7486912
StellarDawn: Yeah I got my laptop there, it was the same price as Best Buy 
                 but it included an extra warranty for free

#7486957
Amber: [QUOTE=WhisperingShadow;7486912]Yeah I got my laptop there, it was the same price as Best Buy 
           but it included an extra warranty for free[/QUOTE]
           Dang that's pretty crazy
```
In this example, you can see that user **StellarDawn** has made a post about their TV, and user **Amber** made a reply to their post. However if we look closely, it seems that Amber is actually quoting the post of a user named **WhisperingShadow**

When you quote another user in vBulletin, it adds the username (rather than a dynamic user ID) of the owner of that post and post number of the post to the quote block. This functionality essentially "preserves" the username the quoted user had at the time. Using this information, we can write a script to collect these username mismatches and build a database of historic usernames .

My goal with this project was to build a database of all known usernames for a given user, to be used as a resources to help other members of the forum differentiate between users.

## Solution



I decided to use the BeautifulSoup library to parse the HTML as I had some experience using it in an earlier project. After first using the requests library to make a GET request, we can use the response to make a BeautifulSoup object. Using the inspect feature in the browser, we can see which HTML tags contain the relevant data we're looking for.

```
def getSoup(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')
```

Using the response of this first page, we can take a look and see if the thread has 1 or more pages by looking for the div tag used to display the page list.

```
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
```

We will use this `pagecount` to make sure we collect posts from every page of the thread, and now we can start scraping posts.

Using `for current_post in soup.find_all('li', class_='postbitlegacy postbitim postcontainer old')` we can break down the page into individual posts.

First, we're going to try getting all of the relevant information from the first post. This try statement will fail is the user is a guest, which frankly there aren't many and for the purposes of this project we will ignore. By using `continue` we can skip directly to the next post.

```
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
```

Since we know this is a valid member, we're going to cache the userid, the username of the poster as it is today, and time of the post in a dictionary using the postid as a key. This allows us to use a dictionary like hashmap, and will give us a way to compare usernames contained in post quotes later.
```
postsDB[postid] = {
    'userid':   userid,
    'username': username,
    'time':     posttime
}
```

Now we can move on to the actual post content. What we're looking for are quote blocks, although members can use [QUOTE][/QUOTE] tags without linking a username or post id, and we want to ignore these and continue to the next quote block (if it exists).

```
content = current_post.find('div', class_='content')

# Find all quote blocks in current post
for quote_block in content.find_all('div', class_='bbcode_postedby'):

	# Try to get an alias and postid
	try:
		quote = {
			'postid':   int(quote_block.find('a').get('href').split('#post')[1]),
			'alias':    quote_block.find('strong').get_text()
		}
	except:
		# Bad quote block, ignore
		continue
```

If we are succesful in finding a post ID and username alias in a quote block, we can compare it to the information we have saved in our postsDB cache. If the username in the quoted post and their username as it exists today, we will record the conflict and add it to our database.

```
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
```
If `quote_postid` does not exist in postsDB, the post may have been deleted or the quoted post may be from a different thread. In either case I decided to also store these in the database with a userid of `None`, so that I could analyze them later.

```
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
```
Once this page is done, we'll get the next page if there are any remaining and continue, or mark the thread complete in our database.
```
        # If there are more pages remaining, get soup from next page
        if i < pagecount:
            nextURL=f'{targetURL}/page{i+2}'
            soup = soup = getSoup(nextURL)

    # Mark this target completed
    db.markFinished(threadid)
```


## Limitations
This is not a very elegant solution to this problem and while coding it I realized I had too many nested loops. I decided to leave the code as is rather than creating a fully OOP solution as the results were more important to me than having the best written code. If I had to do this project again, I would probably make distinct classes for forums, threads, posts, and users. I would also have liked to add a way to define specific windows of threads to scrape, such as all threads created between January 1, 2012 to January 1 2023, and then make a search algorithm to find which pages needed to be scraped for target threads.
