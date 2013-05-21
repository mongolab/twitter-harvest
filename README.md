Harvest
====================

Tutorial for harvesting Twitter user timelines. Allow developers interested in learning more about MongoDB to populate their database with some easily accessible data.

This tutorial uses the "save" method for handling documents (essentially an "upsert"). Pymongo documentation [here](http://api.mongodb.org/python/current/api/pymongo/collection.html). For those unfamiliar with "upserts", MongoDB upsert documentation [here](http://docs.mongodb.org/manual/applications/update/update-operations-with-the-upsert-flag).

Compatible with Python 2.7.x

Run:

python setup.py install

python harvest.py your args here


Twitter App Setup
-----------------

For those unfamiliar with the Twitter Dev/App page, here are instructions for getting this script up and running.

1. Visit Twitter dev [page](https://dev.twitter.com/).
2. Go to My Applications (should be drop down from your username).
3. Create new app, fill in required fields.
4. Your access token, access token secret, consumer key, and consumer secret should all be displayed. Assign those values accordingly in the script.
5. You may also want to edit the application type based on what you want.  Under the settings tab there is an application type section that can be changed.


Contact
-------

Feel free to contact me via twitter [@c2kc](https://twitter.com/c2kc) or email <chang.christopher@gmail.com> if you have any questions or comments!
