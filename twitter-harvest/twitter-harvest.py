##############################################################################
#
# Copyright (c) 2012 ObjectLabs Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
################################################################################

#!/usr/bin/env python

__author__ = 'mongolab'


import pymongo
import oauth2 as oauth
import urllib2, json
import sys, argparse, time 

def oauth_header(url, consumer, token):
    params =  {'oauth_version': '1.0',
               'oauth_nonce': oauth.generate_nonce(),
               'oauth_timestamp': int(time.time()),
              }
    req = oauth.Request(method = 'GET',url = url, parameters = params)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(),consumer, token)
    return req.to_header()['Authorization'].encode('utf-8')

def main():
    
    ### Build arg parser
    parser = argparse.ArgumentParser(description = 'Connects to Twitter User Timeline endpoint, retrieves tweets and inserts into a MongoLab database. Developed on Python 2.7')
    parser.add_argument('-r', '--retweet', help = 'include native retweets in the harvest', action = 'store_true')
    parser.add_argument('-v', '--verbose', help = 'print harvested tweets in shell', action = 'store_true')
    parser.add_argument('--numtweets', help = 'set total number of tweets to be harvested. max = 3200', type = int, default = 3200)
    parser.add_argument('--user', help = 'choose twitter user timeline for harvest', default = 'mongolab')
    parser.add_argument('--db', help = 'MongoLab DB URI, example: mongodb://dbuser:dbpassword@dbh85.mongolab.com:port/dbname', required = True)
    parser.add_argument('--consumer-key', help = 'Consumer Key from your Twitter App OAuth settings', required = True)
    parser.add_argument('--consumer-secret', help = 'Consumer Secret from your Twitter App OAuth settings', required = True)
    parser.add_argument('--access-token', help = 'Access Token from your Twitter App OAuth settings', required = True)
    parser.add_argument('--access-secret', help = 'Access Token Secret from your Twitter App Dev Credentials', required = True)

    ### Fields for query
    args = parser.parse_args()
    user = args.user 
    numtweets = args.numtweets
    verbose = args.verbose
    retweet = args.retweet

    ### Build Signature
    CONSUMER_KEY = args.consumer_key
    CONSUMER_SECRET = args.consumer_secret
    ACCESS_TOKEN = args.access_token
    ACCESS_SECRET = args.access_secret

    ### Build Endpoint + Set Headers
    base_url = url = "https://api.twitter.com/1.1/statuses/user_timeline.json?include_entities=true&count=200&screen_name=%s&include_rts=%s" % (user, retweet)
    oauth_consumer = oauth.Consumer(key = CONSUMER_KEY, secret = CONSUMER_SECRET)
    oauth_token = oauth.Token(key = ACCESS_TOKEN, secret = ACCESS_SECRET)
 
    ### Setup MongoLab Goodness
    uri = args.db 
    conn = pymongo.MongoClient(uri)
    uri_parts = pymongo.uri_parser.parse_uri(uri)
    db = conn[uri_parts['database']]
    db['twitter-harvest'].ensure_index("id_str")
  
    ### Helper Variables for Harvest
    max_id = -1
    tweet_count = 0

    ### Begin Harvesting
    while True:
        auth = oauth_header(url, oauth_consumer, oauth_token)
        headers = {"Authorization": auth}
        request = urllib2.Request(url, headers = headers)
        stream = urllib2.urlopen(request)
        tweet_list = json.load(stream)

        if 'errors' in tweet_list:
            print 'Hit rate limit, code: %s, message: %s' % (tweets['errors']['code'], tweets['errors']['message'])
       	    return
	if max_id == -1:
	    tweets = tweet_list
	else:
	    tweets = tweet_list[1:]
	    if len(tweets) == 0:
		print 'Finished Harvest!'
	        return
	
	for tweet in tweets:
	    max_id = id_str = tweet["id_str"]
	    try:
		if tweet_count == numtweets:
		   print 'Hit numtweets!' 
		   return 
		db['twitter-harvest'].update({"id_str":id_str},tweet,upsert = True)
		tweet_count+=1
		if verbose == True:
		   print tweet["text"]
	    except Exception:
                print 'Unexpected error encountered'
		return    
	url = base_url + "&max_id=" + max_id

    print 'Finished Harvesting!'

if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        if e.code == 0:
            pass
