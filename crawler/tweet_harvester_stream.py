import os
import io
import logging
import couchdb
import argparse
import time
import json
from utils import *
from tweepy import Stream


class TweetListener(Stream):

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret,
                 time_limit: int, number_of_tweets: int,
                 couchdb_server: str, file: str, db_name: str):

        super().__init__(consumer_key=consumer_key,consumer_secret=consumer_secret,
                         access_token=access_token,access_token_secret=access_token_secret)

        self.start_time = time.time()
        self.time_limit = time_limit

        self.count = 0
        self.number_of_tweets = number_of_tweets

        self.file = file # switched to couchdb info later?

        if db_name in couchdb.Server(couchdb_server):
            self.db = couchdb.Server(couchdb_server)[db_name]
        else:
            self.db = couchdb.Server(couchdb_server).create(db_name)

    def on_data(self, data):
        try:
            # an extra tweet returned after the stream closed for some reason
            if time.time()-self.start_time > self.time_limit:
                print('time has been reached')
                self.disconnect()

            if self.count >= self.number_of_tweets:
                print('number of tweets has been reached')
                self.disconnect()

            tweet = json.loads(data)
            self.count += 1

            # check if this is a tweet in case of some other info
            if 'text' in tweet.keys():
                clf = simpleClassifier()
                if tweet['id_str'] not in self.db:
                    dic = {}
                    dic['_id'] = tweet["id_str"]
                    dic['text'] = tweet['text']
                    dic['geo'] = tweet['geo']['coordinates'] if tweet['geo'] else 'None'
                    dic['place'] = tweet['place']["bounding_box"]["coordinates"][0] if tweet['place'] else 'None'
                    dic['senti'] = clf.classify(tweet['text'])

                    self.db.save(dic)
                    del dic

                # file saving
                if self.file:
                    with open(self.file, 'a') as my_file:
                        json.dump(tweet, my_file)
                        my_file.write('\n')

                # print(tweet)

        except BaseException as e:
            # print(json.loads(data))
            print(e)


    def on_request_error(self, status_code):

        if status_code == 429:
            print('Wait on rate limit!')
            time.sleep(15*60+1)

        else:
            print(status_code)


    def on_connection_error(self):
        self.disconnect()



if __name__ == "__main__":
    # argpaser
    paser = argparse.ArgumentParser()

    paser.add_argument("--time",type=int,default=24*60*60,help="How long do you want this stream to last")
    paser.add_argument("--limit", type=int, default=500000, help="How many tweets you want to search in stream")
    paser.add_argument("--dbname", type=str, default="tweets", help="The name of the database you wan to store")
    paser.add_argument("--config", type=str, default=None, help="Provide information for configuration.json:PATH")
    paser.add_argument("--local",type=str,default=None,help="Specify the local file you want to store the data in .json")
    args = paser.parse_args()

    config = args.config  # path of the config file

    try:

        with open(config, 'r') as f:

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
            query = configuration['KEY WORDS']

    except IOError:
        print('The file path of the config file is probably wrong!')
        exit(1)

    # default query
    # query = ['covid','virus','lockdown']

    # if you want to store them to local file as well specify filename with file='XXX.json'
    stream = TweetListener(consumer_key=api_key,consumer_secret=api_secret,
                           access_token=access_token,access_token_secret=access_token_secret,
                           time_limit=args.time,number_of_tweets=args.limit,
                           couchdb_server='http://admin:admin@127.0.0.1:5984/',
                           db_name=args.dbname, file=args.local)


    try:
        # locations are bounding box for melb
        print("stream started")
        stream.filter(languages=["en"], track=query,
                      locations=[144.593741856, -38.433859306, 145.512528832, -37.5112737225])
    except KeyboardInterrupt:
        stream.disconnect()
