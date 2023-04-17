Overview

A while back, a forum I frequent added the ability to allow users to change their names, which led to a huge amount of confusion. Members were changing their names multiple times a week, and some members were changing their names to other members' old names. I noticed that, when quoting another user's post, the username that member had at that particular time was added directly into the quoting user's post.

IE: Originally Posted by USERNAME

I figured there would be a way to write a simple script that could crawl through a thread and find posts of user's quoted containing names which do not match their current username. By running this script through an entire forum, one could easily generate a database of almost known username changes. 

Currently this script only goes through a single thread, but I would like to add functionality to allow crawling of an entire forum's threads, as well as the ability to pause and resume, modulate the speed of GET requests, and have a GUI mode to display the current progress.