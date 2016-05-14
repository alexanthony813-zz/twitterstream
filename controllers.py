from pymongo import MongoClient
from textblob import TextBlob
import json

conn = MongoClient('localhost', 27017)
db = conn.tweets

def parse_cords(coordstring):
    coords = coordstring.split(',')
    x_beg_slice = coords[1].index('[')+1
    x = float(coords[1][x_beg_slice:])
    y_end_slice = coords[2].index(']')
    y = float(coords[2][:y_end_slice])
    coords = [x, y]
    return coords

def sent_analysis(tweet):
    text = tweet['text']
    blob = TextBlob(u'%s' % tweet['text'])
    sentiment = blob.sentiment
    tweet['analysis'] = sentiment
    tweet['coords'] = parse_cords(tweet['coords'])
    db.tweets.insert_one(tweet)

if __name__=='__main__':
  main()
