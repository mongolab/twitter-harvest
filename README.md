Twitter-Harvest
====================

Twitter-Harvest is a Twitter [User Timeline](https://dev.twitter.com/docs/api/1.1/get/statuses/user_timeline) harvesting tool that allows the user to download statuses (tweets) in the form of JSON objects and stores them into a MongoLab database.  You must provide a connection URI for your database.

Compatible with Python 2.7.x, you must also have Twitter Auth Credentials (detailed below).


Usage
---------

###Install###

Run:

    python setup.py install
    
###Harvest###

Run:

    python harvest.py --uri mongolab-uri --consumer-key consumer-key --consumer-secret consumer-secret --access-token access-token --access-secret access-secret
    
The uri, consumer-key, consumer-secret, access-token and access-secret arguments are required.

###Other Useful Options###

-c sets the count or number of tweets to be returned per request (max 200 per request, default = 200)

-u chooses the username timeline that you would like to harvest (default = mongolab)

-r sets whether you would like retweets included in the results (default = true)

###Help Contents###

    usage: harvest.py [-h] [-c C] [-u U] [-r R] --uri URI 
                      --consumer-key CONSUMER_KEY --consumer-secret CONSUMER_SECRET
                      --access-token ACCESS_TOKEN --access-secret ACCESS_SECRET
    
    Twitter User Timeline Harvest
    
    optional arguments:
    -h, --help                          show this help message and exit
    -c C                                sets the count or number of tweets to be returned per request. max = 200
    -u U                                choose username timeline you are interested in harvesting. no @ symbol
    -r R                                set whether you want retweets (true) or only self tweets (false)
    --uri URI                           MongoLab URI, example: mongodb://dbuser:dbpassword@dbh85.mongolab.com:port/dbname
    --consumer-key    CONSUMER_KEY      Consumer Key from your Twitter App OAuth settings
    --consumer-secret CONSUMER_SECRET   Consumer Secret from your Twitter App OAuth settings
    --access-token    ACCESS_TOKEN      Access Token from your Twitter App OAuth settings
    --access-secret   ACCESS_SECRET     Access Token Secret from your Twitter App Dev Credentials

Twitter App Setup
-----------------

For those unfamiliar with the Twitter Dev/App page, here are instructions for getting this script up and running.

1. Visit Twitter dev [page](https://dev.twitter.com/).
2. Go to My Applications (should be drop down from your username).
3. Create new app, fill in required fields.
4. Your access token, access token secret, consumer key, and consumer secret should all be displayed. Assign those values accordingly in the script.
5. You may also want to edit the application type based on what you want.  Under the settings tab there is an application type section that can be changed.


PyMongo
---------

Twitter-Harvest uses the save (upsert) method for handling documents. PyMongo documentation for upserts [here](http://api.mongodb.org/python/current/api/pymongo/collection.html). For those unfamiliar with upserts, MongoDB upsert documentation [here](http://docs.mongodb.org/manual/core/update/#update-operations-with-the-upsert-flag).


Contact
-------

Feel free to contact me via twitter [@c2kc](https://twitter.com/c2kc) or email <chang.christopher@gmail.com> if you have any questions or comments!
