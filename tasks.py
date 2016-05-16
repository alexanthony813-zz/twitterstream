from textblob import TextBlob
import json
from config import MONGO_DEV_URL, MONGO_DEV_PORT, MONGO_DEV_URL
import os
import sys
from celery import Celery
import time
from server import connection, handle

app = Celery('tasks', broker='redis://localhost')
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
    print text

    try:
        blob = TextBlob(u'%s' % tweet['text'])
    except:
        return
    sentiment = blob.sentiment
    tweet['polarity'] = sentiment.polarity
    tweet['subjectivity'] = sentiment.subjectivity
    tweet['coords'] = parse_cords(tweet['coords'])
    print 'man, im going to miss that thread!'
    handle.tweets.insert_one(tweet)
    print tweet
    return tweet
