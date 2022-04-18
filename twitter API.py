# 记得用cisco vpn
import tweepy
import configparser
import pandas as pd
import json
from textblob import TextBlob
import sys
import matplotlib.pyplot as plt

def percentage(part,whole):
    return 100*float(part)/float(whole)

config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

searchTerm = input("Enter keyword/hashtag to search about: ")
numTweet = int(input("Enter how many tweets to analyse: "))

tweets = tweepy.Cursor(api.search_tweets, q=searchTerm, lang="en").items(numTweet)


positive = 0
negative = 0
neutral = 0
polarity = 0


for tweet in tweets:
    print(tweet.text)
    analysis = TextBlob(tweet.text)
    if(analysis.sentiment.polarity == 0.00):
        neutral += 1
    elif(analysis.sentiment.polarity < 0.00):
        negative += 1
    elif(analysis.sentiment.polarity > 0.00):
        positive += 1

positive = percentage(positive, numTweet)
negative = percentage(negative, numTweet)
neutral = percentage(neutral, numTweet)

positive = format(positive, '.2f')
neutral = format(neutral, '.2f')
negative = format(negative, '.2f')

print("How people are reacting on" + searchTerm + "by analyzing" + str(numTweet) + "Tweets.")

if (polarity == 0):
    print("Neutral")
elif (polarity < 0):
    print("Negative")
elif (polarity>0):
    print("postive")



labels = ['Positive ['+str(positive)+'%]', 'Neutral [' + str(neutral)+'%]', 'Negative ['+str(negative)+ '%]']
sizes = [positive, neutral, negative]
colors = ['yellow', 'blue', 'red']
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
plt.legend(patches, labels, loc="best")
plt.title("How people are reacting on " + searchTerm + "by analyzing" + str(numTweet) + "Tweets.")
plt.axis('equal')
plt.tight_layout()
plt.show()
#
#public_tweets = api.home_timeline()
#search_words = "#covid-19,#melbourne"
#data_since = "2020-1-1"
#tweets =tweepy.Cursor(api.search_tweets, q=search_words,lang = "en",since=data_since).items(30)
#columns = ['Time', 'User', 'Tweet']
#data = []
#for tweet in tweets:
   # data.append([tweet.created_at, tweet.user.screen_name, tweet.text])
    #json.loads(data)
#df = pd.DataFrame(data, columns=columns)
#df.to_json('twitter123.json')
#with open('tweets.json', 'w') as json_file:
    #json.dump(data, json_file)

