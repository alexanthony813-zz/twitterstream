from pymongo import MongoClient
from textblob import TextBlob
import json

conn = MongoClient('localhost', 27017)
db = conn.tweets


def sent_analysis(tweet):
  text = tweet['text']
  blob = TextBlob(u'%s' % tweet['text'])
  sentiment = blob.sentiment
  tweet['analysis'] = sentiment
  print sentiment
  db.tweets.insert_one(tweet)

if __name__=='__main__':
  main()
