## Overview

A little backstory: some time ago, a vBulletin forum I frequent introduced a feature which allowed users to change their usernames. The way this feature was implemented allowed users to change the username variable stored in the database directly, leading to a huge amount of confusion as members were changing their names multiple times a day, and even impersonating other members by taking others' old usernames. 

During this confusion I noticed that when reading through older posts, anytime a user quoted another user's post, the username the quoted user had at that time was 'hard-coded' into the post. The BBCODE when quoting another user looks something like this:
```
[QUOTE=Username987;7486912]Oh also got my tv there.. Same price as Amazon but included extra warranty for free[/QUOTE]
```
I figured that if you could write a script that went through each post on the forums looking for post quotes, then compare the name shown on the quoted post to the current user's username, you could easily build a database of all known usernames a given userid has been associated with. 

My goal with this project is to build a database of all known aliases for a given user to be used as a resource for other members of the forum.

## Project Status
Currently this script only goes through a single thread, but I would like to add functionality to allow crawling of an entire forum's threads, as well as the ability to pause and resume crawling, modulate the speed of GET requests to not overload the server, and add a GUI to display the script's current progress. I would also like to rewrite this script using OOP practices, such as using classes for posts, threads, and soup data.


## Challenges
The forums that I built this script for are private, and you must be logged in to view threads and posts. In previous projects that required user authentication, I had no problem copying and pasting the values from my cookies in my logged-in web browser. When I first began coding this project, I tried using a Sessions() object from the requests library, but I couldn't get it to work with the values I was trying to provide. 

The solution that worked for me was using a dictionary to store the values I wanted to pass along in the header of the GET request:
```
# NOTE: the host and cookie information has been edited for privacy
headers = {
    'Host': 'forum.example.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Cookie': 'bb_lastvisit=1602363469; bb_lastactivity=0; bb_userid=3827; bb_password=b1f67866cbe9c2a04ff94720adad4dd; vbulletin_collapse=c_thanks_post5489317; vbulletin_userlist_hide_avatars_buddylist=0; bb_sessionhash=e579029c9f04ed288a70a0d3a6f5892',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache'
}
```

And then pass the headers dictionary to the .get function
```
response = requests.get(basescanurl, headers=headers)
```
