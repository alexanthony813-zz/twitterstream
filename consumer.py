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
from tasks import sent

ckey = api_ckey
csecret = api_csecret
atoken = api_atoken
asecret = api_asecret

PRODUCTION_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
if PRODUCTION_URL:
  r = redis.from_url(PRODUCTION_URL, port=6379, db=0)
else:
  r = redis.StrictRedis(REDIS_DEV_URL, port=REDIS_DEV_PORT, db=0)


class listener(StreamListener):

  def on_data(self, data):
    # also get geolocation, save to redis.
    json_data = json.loads(data)

    try:
      coords = unicode(json_data['coordinates'])
      unicode_coords = unicodedata.normalize('NFKD', coords).encode('utf-8','ignore')
    except:
      # end process for tweets that are not geo_enabled
      return

    if coords != "None":
      created_at = unicode(json_data['created_at'])  
      unicode_created_at = unicodedata.normalize('NFKD', created_at).encode('utf-8','ignore')    
    else:
      return

    try:
      text = unicode(json_data['text'])
      unicode_text = unicodedata.normalize('NFKD', text).encode('utf-8','ignore')
    except:
      # end process for tweets without any text value
      return

    tweet = {'coords': unicode_coords, 'created_at': unicode_created_at, 'text': unicode_text}
    print 'here'
    result = sent.delay(tweet)
    # print i.scheduled()
    print 'there'
    # res = AsyncResult(result)
    # res.ready()

  def on_error(self, status):
    print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
# basically using very common english words to track and filter out for language (en lue of proper firehose connection from Twitter)
twitterStream.filter(languages=['en'], track=['a', 'the', 'i', 'you', 'u'])


# /////////////////////////////////////////////////////

# # from tasks import sent_analysis, print_piss
# import tasks
# from celery.result import AsyncResult
# from celery.task.control import inspect
# i = inspect()

# hopefully this is the right broker
# from worker import sent_analysis

# def parse_cords(coordstring):
#     try:
#         coords = coordstring.split(',')
#         x_beg_slice = coords[1].index('[')+1
#         x = float(coords[1][x_beg_slice:])
#         y_end_slice = coords[2].index(']')
#         y = float(coords[2][:y_end_slice])
#         coords = [x, y]
#         return coords
#     except:
#         return []

# @app.task
# def sent_analysis(tweet):
#     print 'in worker\n'
#     # async write
#     # handle = connection['tweets']
#     handle.authenticate('')

#     text = tweet['text']

#     try:
#         blob = TextBlob(u'%s' % tweet['text'])
#     except:
#         return
#     sentiment = blob.sentiment
#     tweet['polarity'] = sentiment.polarity
#     tweet['subjectivity'] = sentiment.subjectivity
#     tweet['coords'] = parse_cords(tweet['coords'])
#     handle.tweets.insert_one(tweet)
#     print 'man, im going to miss that thread!'
    # def write(arg_tweet):

    # thread = Thread(target=write,args=(tweet,))
    # thread.start()
# ///////////////////////////////////////////////////////////////////
