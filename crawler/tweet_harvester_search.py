import os
import json
import argparse
import time
import tweepy
import couchdb

from utils import *

class SearchTweet():

    def __init__(self,api: tweepy.API,db_name:str,couchdb_server:str,file: str):
        # havent figured out on how to run this for a certain amount of time
        # self.time

        self.api = api
        self.file = file # possibly changed to couchdb credentials and whatnot

        if db_name in couchdb.Server(couchdb_server):
            self.db = couchdb.Server(couchdb_server)[db_name]
        else:
            self.db = couchdb.Server(couchdb_server).create(db_name)

    def search(self,q,lang,geocode,limit):
        try:
            # limit: Maximum number of items to iterate over (paginate)
            # no idea what the actual number is this max
            # and what will happen if our limit is beyond max
            statuses = tweepy.Cursor(method=self.api.search_tweets,
                                     q=q, lang=lang,geocode=geocode,
                                     result_type='recent',tweet_mode='extended').items(limit)
            if statuses:
                for stat in statuses:
                    tweet = stat._json
                    if 'full_text' in tweet:
                        clf = simpleClassifier()
                        if tweet['id_str'] not in self.db:
                            dic = {}
                            dic['_id'] = tweet["id_str"]
                            dic['text'] = tweet['full_text']
                            dic['geo'] = tweet['geo']['coordinates'] if tweet['geo'] else 'None'
                            dic['place'] = tweet['place']["bounding_box"]["coordinates"][0] if tweet['place'] else 'None'
                            dic['senti'] = clf.classify(tweet['full_text'])

                            self.db.save(dic)
                            del dic

                        # file saving
                        if self.file:
                            with open(self.file, 'a') as my_file:
                                json.dump(tweet, my_file)
                                my_file.write('\n')

                        # print(tweet)

        except BaseException as e:
            print(e)
            print('Some unexpected errors happened')


if __name__ == "__main__":
    # argpaser
    paser = argparse.ArgumentParser()

    paser.add_argument("--limit", type=int, default=10000, help="How many tweets you want to search in the last week")
    paser.add_argument("--dbname", type=str, default="tweets", help="The name of the database you wan to store")
    paser.add_argument("--config", type=str, default=None, help="Provide information for configuration.json:PATH")
    paser.add_argument("--local", type=str, default=None, help="Specify the local file you want to store the data in .json")

    args = paser.parse_args()

    config = args.config  # path of the config file

    try:

        with open(config,'r') as f:

            configuration = json.loads(f.read())

            if 'API' not in configuration:
                print('API KEYS not found')
                exit(1)

            if 'KEY WORDS' not in configuration:
                print('KEY WORDS not found')
                exit(1)

            # retrieve secret keys and tokens
            api_config = configuration['API']

            api_key = api_config['api_key']
            api_secret = api_config['api_secret']

            access_token = api_config['access_token']
            access_token_secret = api_config['access_token_secret']

            bearer_token = api_config['bearer_token']

            # retrieve key words to search
            query = ' '.join(configuration['KEY WORDS'])

    except IOError:
        print('The file path of the config file is probably wrong!')
        exit(1)

    # authentication
    auth = tweepy.OAuth1UserHandler(consumer_key=api_key, consumer_secret=api_secret,
                                    access_token=access_token, access_token_secret=access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     retry_errors={404, 401, 503}) # https://developer.twitter.com/en/docs/twitter-ads-api/response-codes

    # default query
    # query = "melbourne covid -filter:retweets"

    # latitude,longitude,radius for melb
    geocode = '-37.813611,144.963056,20km'

    try:
        # just in case if there is a problem with the loop for search_tweets
        # while False:
        #     print('search started')
        #     searchTweets = SearchTweet(api=api, file='search.json')
        #     searchTweets.search(q=query,lang='en',geocode=geocode,limit=lim)

        print('search started')
        # if you want to store them to local file as well, specify filename with file='XXX.json'
        searchTweets = SearchTweet(api=api,couchdb_server='http://admin:admin@127.0.0.1:5984/',
                                   db_name=args.dbname,file=args.local)
        searchTweets.search(q=query, lang='en', geocode=geocode, limit=args.limit)  # limit = lim

    except KeyboardInterrupt:
        exit(1)
