Make sure you have a correct config.json file under the same directory, 
where you have to specify your tokens and keys and also the key words you want to search, 
in the format of {"API":{"api_key":XXX,"api_secret":XXX,...},"KEY WORDS":["melbourne","covid",...]}.<br>
For search recent tweets
```
./tweepy_search_run.sh
```
For stream tweets
```
./tweepy_stream_run.sh
```
You might also want to change the arguments in these two scripts for a more explanatory harvest.<br>
```
python3 ./tweet_harvester_stream.py --time 5 --limit 10 --config './config.json'
```
Current available arguments are 'limit' and 'time'. Time is only for stream.
Limit is the number of tweets you want to harvest. Time is how long you want the stream to last.