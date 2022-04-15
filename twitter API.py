# 记得用cisco vpn
import tweepy
import configparser
import pandas as pd
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#public_tweets = api.home_timeline()
search_words = "#covid-19,#melbourne"
data_since = "2021-1-1"
tweets =tweepy.Cursor(api.search_tweets, q=search_words,lang = "en",since=data_since).items(10)
columns = ['Time', 'User', 'Tweet']
data = []
for tweet in tweets:
    data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
df = pd.DataFrame(data, columns=columns)

df.to_csv('tweets1.csv')
