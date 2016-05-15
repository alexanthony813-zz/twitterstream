from textblob import TextBlob
import json
from config import MONGO_DEV_URL, MONGO_DEV_PORT, MONGO_DEV_URL
import os
from server import handle

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

def sent_analysis(tweet):
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

if __name__ == '__main__':
    main()