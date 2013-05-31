#!/usr/bin/env python

__author__ = 'chris chang'


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
    head = req.to_header()['Authorization'].encode('utf-8')
    return head

def main():
    #Parse Argument Fields
    parser = argparse.ArgumentParser(
        description = 'Twitter User Timeline Harvest')
    parser.add_argument('-c', help = 'sets the count or number of tweets to be returned per request. max = 200', default = '200')
    parser.add_argument('-u', help = 'choose username timeline you are interested in harvesting. no @ symbol', default = 'mongolab')
    parser.add_argument('-r', help = 'set whether you want retweets (true) or only self tweets (false)', default = 'true')
    parser.add_arugment('--uri', help = 'MongoLab URI, example: mongodb://dbuser:dbpassword@dbh85.mongolab.com:port/dbname', required = True)
    parser.add_argument('--consumer-key', help = 'Consumer Key from your Twitter App OAuth settings', required = True)
    parser.add_argument('--consumer-secret', help = 'Consumer Secret from your Twitter App OAuth settings', required = True)
    parser.add_argument('--access-token', help = 'Access Token from your Twitter App OAuth settings', required = True)
    parser.add_argument('--access-secret', help = 'Access Token Secret from your Twitter App Dev Credentials', required = True)

    args = parser.parse_args()

    #Fields for query:
    
    username = args.u 
    count = args.c 
    retweet = args.r 
    
    #Build Signature
    CONSUMER_KEY = args.consumer_key
    CONSUMER_SECRET = args.consumer_secret
    ACCESS_TOKEN = args.access_token
    ACCESS_SECRET = args.access_secret

    base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json?include_entities=true&screen_name=%s&count=%s&include_rts=%s" % (username, count, retweet)
    url = base_url 
    oauth_consumer = oauth.Consumer(key = CONSUMER_KEY, secret = CONSUMER_SECRET)
    oauth_token = oauth.Token(key = ACCESS_TOKEN, secret = ACCESS_SECRET)
 
    #Setup MongoLab Goodness
    URI = args.uri 
    conn = pymongo.MongoClient(URI)
    uri_parts = pymongo.uri_parser.parse_uri(URI)
    db_name = uri_parts['database']
    db = conn[db_name]
    db.Harvest.ensure_index("id_str", unique = True)
    
    #Begin Harvesting
    loop = True 
    while loop:
        auth = oauth_header(url, oauth_consumer, oauth_token)
        headers = {"Authorization": auth}
        request = urllib2.Request(url, headers = headers)
        f = urllib2.urlopen(request)
        tweets = json.load(f)
        if 'errors' in tweets:
            print 'Hit rate limit, code: %s, message: %s' % (tweets['errors']['code'], tweets['errors']['message'])
            sys.exit()
        max_id = -1
        dupCount = 0
        for tweet in tweets:
            id_str = tweet["id_str"]
            if max_id == -1 or max_id > id_str:
                max_id = id_str
            elif max_id == id_str:
                loop = False 
                break
            try:
                print tweet['text']
                db.Harvest.save(tweet)
            except pymongo.errors.DuplicateKeyError:
                dupCount += 1 
                if dupCount > 5:
                    loop = False 
                    print 'Hit Max Tweets'
                    break
                continue
        #Continue Harvesting for older Tweets. Max 3200
        url = base_url + "&max_id=" + max_id

if __name__ == '__main__':
    try:
        main()
    except SystemExit as e:
        if e.code == 0:
            pass
