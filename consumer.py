from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import unicodedata
import redis
import rq
import nltk
from textblob import TextBlob
import worker
from config import api_ckey, api_csecret, api_atoken, api_asecret, REDIS_TO_GO, REDIS_DEV_URL, REDIS_DEV_PORT, REDIS_PROD_PORT, REDIS_PROD_URL
import os
print 'consuming\n>>>>>>>>>>>>>>>>>>>>>>>>>'
ckey = api_ckey
csecret = api_csecret
atoken = api_atoken
asecret = api_asecret

PRODUCTION_URL = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
if PRODUCTION_URL:
  print 'prod\n>>>>>>>>>\n\n\n\____________',PRODUCTION_URL
  r = redis.from_url(PRODUCTION_URL, port=6379, db=0)
else:
  print 'not production!!!!!!!!!!!!!!'
  r = redis.StrictRedis(REDIS_DEV_URL, port=REDIS_DEV_PORT, db=0)

q = rq.Queue(connection=r)


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
    # put in sentiment analysis callback rather than str(i)
    q.enqueue(worker.sent_analysis, tweet, timeout=20)
    print 'q__________________________________\n', q
    return True

  def on_error(self, status):
    print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
# basically using very common english words to track and filter out for language (en lue of proper firehose connection from Twitter)
twitterStream.filter(languages=['en'], track=['a', 'the', 'i', 'you', 'u'])

if __name__ == '__main__':
  with rq.Connection(r):
    # reconfigure to use processes
    worker = rq.Worker(map(q, ['high', 'default', 'low']))
    worker.work()
