FROM python:3.7

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

#ENTRYPOINT ['/tweepy_stream_run.sh']
CMD ["python","tweet_harvester_stream.py","--config","./config.json"]