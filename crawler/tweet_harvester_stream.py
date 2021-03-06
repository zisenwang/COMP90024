import os
import io
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

        super().__init__(consumer_key=consumer_key, consumer_secret=consumer_secret,
                         access_token=access_token, access_token_secret=access_token_secret)

        self.start_time = time.time()
        self.time_limit = time_limit

        self.count = 0
        self.number_of_tweets = number_of_tweets

        self.file = file

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
                    dic['created_time'] = tweet['created_at']
                    dic['text'] = clf.preprocess(tweet['text'])
                    dic['geo'] = tweet['geo']['coordinates'] if tweet['geo'] else 'None'
                    dic['place'] = tweet['place']["bounding_box"]["coordinates"][0] if tweet['place'] else 'None'
                    dic['senti'] = clf.sentiment(dic['text'])
                    dic['label'] = 'positive' if dic['senti']['polarity'] > 0 else 'negative'

                    # print(dic)
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
            print('unknown error occurred')
            print(e)
            return True

        return True

    def on_request_error(self, status_code):

        if status_code == 429:
            print('Wait on rate limit!')
            time.sleep(15*60+10)

        else:
            print(status_code)


if __name__ == "__main__":
    # argpaser
    paser = argparse.ArgumentParser()

    paser.add_argument("--time",type=int,default=24*60*60, help="How long do you want this stream to last")
    paser.add_argument("--limit", type=int, default=50000, help="How many tweets you want to search in stream")
    paser.add_argument("--dbname", type=str, default="tweets", help="The name of the database you wan to store")
    paser.add_argument("--config", type=str, default=None, help="Provide information for configuration.json:PATH")
    paser.add_argument("--local",type=str,default=None, help="Specify the local file you want to store the data in .json")
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

            # retrieve location info
            locations = configuration["LOCATIONS"]['bounding_box']

            # retrieve specified dbname
            dbname = args.dbname if args.dbname != "tweets" else configuration["DBNAME"]

    except IOError:
        print('The file path of the config file is probably wrong!')
        exit(1)

    # default query
    # query = ['covid','virus','lockdown']

    # if you want to store them to local file as well specify filename with file='XXX.json'
    stream = TweetListener(consumer_key=api_key, consumer_secret=api_secret,
                           access_token=access_token,access_token_secret=access_token_secret,
                           time_limit=args.time, number_of_tweets=args.limit,
                           couchdb_server='http://admin:admin@172.26.132.194:5984/',
                           db_name=dbname, file=args.local)


    try:
        # locations are bounding box for melb
        print("stream started")
        # Bounding boxes do not act as filters for other filter parameters.
        # For example track=twitter&locations=-122.75,36.8,-121.75,37.8
        # would match any Tweets containing the term Twitter (even non-geo Tweets)
        # OR coming from the San Francisco area.
        # stream.filter(track=query, languages=["en"], locations=locations)
        stream.filter(languages=["en"], locations=locations)

    except KeyboardInterrupt:
        stream.disconnect()


