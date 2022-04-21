import os
import json
import argparse
import time
import tweepy
import couchdb

from sentiment_analyzer import simpleClassifier

class SearchTweet():

    def __init__(self,api: tweepy.API,couchdb_server:str,file: str):
        # havent figured out on how to run this for a certain amount of time
        # self.time

        self.api = api
        self.file = file # possibly changed to couchdb credentials and whatnot

        self.server = couchdb.Server(couchdb_server)

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

                        '''
                        potential feasible fields, id text geo place lang...
                        do sth with tweets fields, for example
                        # if tweet['geo']:
                        #     print(tweet['geo'])
                        info can be pre-filtered here before stored to couchdb
                        need further test on wait_on_rate_limit whenever couchdb is done
                        '''

                        dbname = 'search_covid_tweets'
                        # dbname should be replaced by a more specific name to indicate the certain database
                        if dbname in self.server:
                            db = self.server[dbname]
                        else:
                            db = self.server.create(dbname)

                        db.save(tweet)

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
    paser.add_argument("--config", type=str, default=None, help="Provide information for configuration.json:PATH")
    paser.add_argument("--local",type=str,default=None,help="Specify the local file you want to store the data in .json")
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
        searchTweets = SearchTweet(api=api,couchdb_server='http://admin:admin@127.0.0.1:5984/',file=args.local)
        searchTweets.search(q=query, lang='en', geocode=geocode, limit=args.limit)  # limit = lim

    except KeyboardInterrupt:
        exit(1)
