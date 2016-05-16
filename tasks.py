from textblob import TextBlob
import json
from config import MONGO_DEV_URL, MONGO_DEV_PORT, MONGO_DEV_URL, REDIS_DEV_URL, REDIS_DEV_PORT
import os
import sys
from celery import Celery
import time
from server import connection, handle
is_prod = os.environ.get('IS_HEROKU', None)
print 'task'
# if is_prod:
#     import consumer


# REDIS_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
app = Celery('tasks', broker='redis://redistogo:56bdf242e048ef6d8083d7016967c2ce@catfish.redistogo.com:10220/')
app.config_from_object('celeryconfig')

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
    time.sleep(30)
    text = tweet['text']

    try:
        blob = TextBlob(u'%s' % tweet['text'])
    except:
        return
    sentiment = blob.sentiment
    tweet['polarity'] = sentiment.polarity
    tweet['subjectivity'] = sentiment.subjectivity
    tweet['coords'] = parse_cords(tweet['coords'])
    handle.tweets.insert_one(tweet)
    return tweet
