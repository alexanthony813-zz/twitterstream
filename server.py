from flask import Flask, render_template, request, redirect
import os
from pymongo import MongoClient, GEO2D
# Set the path
from flask import Flask, request, render_template, jsonify, redirect
from bson.json_util import dumps
from bson.son import SON
import requests
from config import MONGO_DEV_URL, MONGO_DEV_PORT, MONGO_PROD_URL, MONGOHQ_URL, MONGO_URI, MONGO_GOLD_URI
is_prod = os.environ.get('IS_HEROKU', None)

# string = r'mongodb://heroku_0p1s62cb:aev0huua42o4qjnrnen2ilj3a3@ds023442.mlab.com:23442/heroku_0p1s62cb'
string = 'ds023442.mlab.com:23442'
print '>>>>>>>>>>>>>>\n',string
uri = string.rsplit()[0]
print '>>>>>>>>>>>>>>>',uri

def in_circle(center_x, center_y, radius, tweet_coords):
    x = tweet_coords[0]
    y = tweet_coords[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

def connect():
    # refactor with ternary
    MONGO_URL = MONGO_DEV_URL
    if not is_prod:
        print 'PROD MONGOD!!!!!!!!!!!!!!!!!!!!\n\n\n\n\n_____________________________'
        connection = MongoClient(uri, port=23442, maxPoolSize=50, waitQueueMultiple=10)
    else:
        print 'not mongo\n\n\n\n\n\n\n\n___________________________'
        connection = MongoClient(uri, MONGO_DEV_PORT, maxPoolSize=50, waitQueueMultiple=10)
    handle = connection['tweets']
    db.authenticate('alex13', 'seal13')
    return handle

def process_aggregate_response(aggregate_polarity, sample_size):
    # have to iterate to get first, and only, aggregate average value...break out into helper
    for result in aggregate_polarity:
        average_polarity = result['avgPolarity']
        most_positive_tweet = handle.tweets.find_one({'polarity': result['mostPositive']})
        most_negative_tweet = handle.tweets.find_one({'polarity': result['mostNegative']})
        most_positive_coordinates = most_positive_tweet['coords']
        most_positive_text = most_positive_tweet['text']
        most_negative_coordinates = most_negative_tweet['coords']
        most_negative_text = most_negative_tweet['text']
        most_negative = {'text': most_negative_text, 'coordinates': most_negative_coordinates}
        most_positive = {'text': most_positive_text, 'coordinates': most_positive_coordinates}
    else:
        return {'tweets': sample_size, 'average_polarity': average_polarity, 'most_positive': most_positive, 'most_negative': most_negative}


app = Flask(__name__)
handle = connect()
handle.tweets.create_index([('coords', '2d')])

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/get_sentiment/<lat>/<lon>/<km_radius>", methods=['GET'])
def get_sentiment(lat, lon, km_radius):

    # TD: add form control so server doesn't crash for invalid coords
    lat = float(lat)
    lon = float(lon)
    degree_radius = (int(km_radius)/111.2)

    # TD: reformat to use agg
    query = {"coords": SON([("$near", [lat, lon]), ("$maxDistance", degree_radius)])}
    tweets = handle.tweets.find(query)
    sample_size = tweets.count() if tweets.count() != 0 else "No tweets available for this location at this time"

    # use $geoNear here to get actual polarity values in that area, then use aggregator to average
    pipeline = [{"$geoNear": {"near": [lat, lon], "distanceField": "coords", "maxDistance": degree_radius}}, {"$group": {"_id": None, "avgPolarity": {"$avg": "$polarity"}, "mostPositive": {"$max": "$polarity"}, "mostNegative": {"$min": "$polarity"}}}]
    aggregate_polarity = handle.tweets.aggregate(pipeline)

    response = process_aggregate_response(aggregate_polarity, sample_size)
    return jsonify(response)

# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 27017))
    if is_prod:
        print 'we\'re doin it live!'
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='localhost', port=port, debug=True, threaded=True)
