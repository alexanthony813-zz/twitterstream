from flask import Flask, render_template, request, redirect
import os
from pymongo import MongoClient, GEO2D
# Set the path
from flask import Flask, request, render_template, jsonify, redirect
from bson.json_util import dumps
from bson.son import SON
import requests

def in_circle(center_x, center_y, radius, tweet_coords):
    x = tweet_coords[0]
    y = tweet_coords[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2

def connect():
# Substitute the 5 pieces of information
    connection = MongoClient('localhost',27017, maxPoolSize=50, waitQueueMultiple=10)
    handle = connection['tweets']
    return handle

app = Flask(__name__)
handle = connect()
handle.tweets.create_index([("coords", GEO2D)])

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/get_sentiment/<lat>/<lon>/<km_radius>", methods=['GET'])
def get_sentiment(lat, lon, km_radius):
    lat = float(lat)
    lon = float(lon)
    degree_radius = (int(km_radius)/111.2)

    print 'hellur', degree_radius
    query = {"coords" : SON([("$near", [lat, lon]), ("$maxDistance", degree_radius)])}
    tweets = handle.tweets.find(query)

    json_tweets = []

    for tweet in tweets:
        json_tweets.append(dumps(tweet))

    return jsonify({'tweets':json_tweets})

# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.run(host='localhost', port=port, debug=True, threaded=True)
