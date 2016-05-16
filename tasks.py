from textblob import TextBlob
import json
from config import MONGO_DEV_URL, MONGO_DEV_PORT, MONGO_DEV_URL
import os
import sys
from celery import Celery

app = Celery('tasks', broker='redis://localhost')

# TWITTER!!!!!!!!!!!!!!!
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import unicodedata
import redis
import nltk
from textblob import TextBlob
from config import MONGO_DEV_URL, MONGO_DEV_PORT, MONGO_DEV_URL
from textblob import TextBlob
from config import api_ckey, api_csecret, api_atoken, api_asecret, REDIS_TO_GO, REDIS_DEV_URL, REDIS_DEV_PORT, REDIS_PROD_PORT, REDIS_PROD_URL
import os
from time import sleep
from server import connection, handle

def parse_cords(coordstring):
    try:
        coords = coordstring.split(',')
        x_beg_slice = coords[1].index('[')+1
        x = float(coords[1][x_beg_slice:])
        y_end_slice = coords[2].index(']')
        y = float(coords[2][:y_end_slice])
        coords = [x, y]
        return coords
    except:
        return []

@app.task
def sent(tweet):
    print 'in worker\n'
    if type(tweet)==str:
        return 'f'
    # async write
    # handle = connection['tweets']
    # handle.authenticate('')

    text = tweet['text']

    try:
        blob = TextBlob(u'%s' % tweet['text'])
    except:
        return
    sentiment = blob.sentiment
    tweet['polarity'] = sentiment.polarity
    tweet['subjectivity'] = sentiment.subjectivity
    tweet['coords'] = parse_cords(tweet['coords'])
    return tweet
    # handle.tweets.insert_one(tweet) RECONFIGURE TO USE BUILT IN
    print 'man, im going to miss that thread!'
