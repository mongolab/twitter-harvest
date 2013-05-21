#!/usr/bin/env python

__author__ = 'chris chang'


import pymongo
import oauth2 as oauth
import urllib2, json
import sys, getopt, time 

def oauth_header(url, consumer, token):
    params =  {'oauth_version': '1.0',
               'oauth_nonce': oauth.generate_nonce(),
               'oauth_timestamp': int(time.time()),
              }
    req = oauth.Request(method = 'GET',url = url, parameters = params)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(),consumer, token)
    head = req.to_header()['Authorization'].encode('utf-8')
    #print head
    return head

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hu:c:r:",["help", "username"]) 
    except getopt.GetoptError:
        print 'getOpt error'
        sys.exit(2)

    #Fields for query:
    username = 'mongolab'
    count = '200'
    retweet = 'true'

    for o, a in opts:
        if o in ("-h", "--help"):
            #usage()
            sys.exit()
        elif o in ("-u", "--username"):
            username = a
        elif o in ("-c"):
            count = a
        elif o in ("-r"):
            retweet = a
        else:
            assert False, "unhandled option"

    URI = raw_input("Enter your MongoLab URI: ")
    conn = pymongo.MongoClient(URI)
    uri_parts = pymongo.uri_parser.parse_uri(URI)
    db_name = uri_parts['database']
    db = conn[db_name]
    db.Harvest.ensure_index("id_str", unique = True)
    
    #Build Signature
    base_url = "https://api.twitter.com/1.1/statuses/user_timeline.json?include_entities=true&screen_name=%s&count=%s&include_rts=%s" % (username, count, retweet)
    url = base_url 
    CONSUMER = raw_input("Enter your Consumer Key: ")
    CONSUMER_SECRET = raw_input("Enter your Consumer Secret: ")
    TOKEN = raw_input("Enter your Access Token: ")
    TOKEN_SECRET = raw_input("Enter Access Secret: ")
    oauth_consumer = oauth.Consumer(key = CONSUMER, secret = CONSUMER_SECRET)
    oauth_token = oauth.Token(key = TOKEN, secret = TOKEN_SECRET)
   
    stop = False
    while True:
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
            print tweet['text']
            print tweet['id_str']
            id_str = tweet["id_str"]
            if max_id == -1 or max_id > id_str:
                max_id = id_str
            elif max_id == id_str:
                stop = True
                break
            try:
                db.Harvest.save(tweet)
            except pymongo.errors.DuplicateKeyError:
                print "Duplicate Tweet"
                dupCount += 1 
                if dupCount > 5:
                    stop = True
                    print 'Hit Max Tweets'
                    break
                continue
        if stop:
            break
        url = base_url + "&max_id=" + max_id

if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except SystemExit as e:
        if e.code == 0:
            pass
