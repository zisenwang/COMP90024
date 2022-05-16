Make sure you have a correct config.json file under the same directory, 
where you have to specify your tokens and keys and information about the city, 
for more details, please refer to the config.json in this folder. 
And if you are just testing the harvester locally, 
you might have to change the IP address and user information of CouchDB in the main function to fit your own CouchDB.<br>
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
Limit is the number of tweets you want to harvest. Time is how long you want the stream to last.<br>
```
python3 ./tweet_harvester_stream.py --time 5 --limit 10 --local 'stream.json' --config './config.json'
```
Now you can also use --local argument to specify the local json file to store data.
```
python3 ./tweet_harvester_stream.py --time 5 --limit 10 --dbname 'stream_covid_tweets' --local 'stream.json' --config './config.json'
```
Another argument --dbname has been added to specify the name of the database where you want to store the tweets. By default, it is set to "tweets".<br>
