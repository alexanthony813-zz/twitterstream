from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import unicodedata
import redis
import rq
import nltk
from textblob import TextBlob
from controllers import sent_analysis
from config import api_ckey, api_csecret, api_atoken, api_asecret

ckey = api_ckey
csecret = api_csecret
atoken = api_atoken
asecret = api_asecret

# might have to deploy this
r = redis.StrictRedis(host='localhost', port=6379, db=0)
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
    q.enqueue(sent_analysis, tweet, timeout=20)
    print 'q>>>>>>>>>>>>>>>>>>>>>>>>>>\n',q.jobs
    return True

  def on_error(self, status):
    print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
# basically using very common english words to track and filter out for language (en lue of proper firehose connection from Twitter)
twitterStream.filter(languages=['en'], track=['a', 'the', 'i', 'you', 'u'])
