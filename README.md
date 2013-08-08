Twitter-Harvest
====================

Twitter-Harvest is a Twitter [User Timeline](https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline) tool that allows the user to download statuses (tweets) from user timelines as JSON objects and store them into a MongoDB database.  

Developed on Python 2.7.x, you must also have Twitter Auth Credentials (detailed below).


Usage
---------

###Install###

Run:

    python setup.py install
    
* setup.py uses setuptools!

###Harvest###

Run:

    python twitter-harvest.py --consumer-key consumer-key --consumer-secret consumer-secret --access-token access-token --access-secret access-secret --db mongodb-uri
    
* The consumer-key, consumer-secret, access-token and access-secret arguments are required.

###Other Useful Options###

-r          include native retweets in harvest (default = False)

-v          print in stdout all the tweets being harvested (default = False)

--db        connection URI, allows for insertion into a MongoDB

--numtweets total number of tweets to be harvested (max = 3200)

--user      user's timeline you would like to harvest. must be public or already following. (default = mongolab)

### Help Contents ###
```
usage: twitter-harvest.py [-h] [-r] [-v] [--numtweets NUMTWEETS] [--user USER]
                          --db DB --consumer-key CONSUMER_KEY
                          --consumer-secret CONSUMER_SECRET 
                          --access-token ACCESS_TOKEN 
                          --access-secret ACCESS_SECRET

Connects to Twitter User Timeline endpoint, retrieves tweets and inserts into
a MongoDB database. Developed on Python 2.7

optional arguments:
  -h, --help                          show this help message and exit
  -r, --retweet                       include native retweets in the harvest
  -v, --verbose                       print harvested tweets in shell
  --numtweets NUMTWEETS               set total number of tweets to be harvested, max = 3200
  --user USER                         choose user timeline for harvest
  --db DB                             MongoDB URI, example: mongodb://dbuser:dbpassword@dbhnn.mongolab.com:port/dbname
  --consumer-key CONSUMER_KEY         Consumer Key from your Twitter App OAuth settings
  --consumer-secret CONSUMER_SECRET   Consumer Secret from your Twitter App OAuth settings
  --access-token ACCESS_TOKEN         Access Token from your Twitter App OAuth settings
  --access-secret ACCESS_SECRET       Access Token Secret from your Twitter App Dev Credentials
```

Twitter App Setup
-----------------

For those unfamiliar with the Twitter Dev/App page, here are instructions for getting this script up and running.

1. Visit the Twitter dev [page](https://dev.twitter.com/).
2. Go to My Applications (should be a drop down from your username).
3. Create new app, fill in required fields.
4. Your access token, access token secret, consumer key, and consumer secret should all be displayed. Assign those values accordingly in the script :)


Contact
-------

Feel free to contact me via twitter [@chrisckchang](https://twitter.com/chrisckchang), email <chris@mongolab.com>, or drop us a line at support@mongolab.com if you have any questions or comments!
