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

# @app.route("/write", methods=['POST'])
# def write():
#     userinput = request.form.get("userinput")
#     oid = handle.mycollection.insert({"message":userinput})
#     return redirect ("/")

@app.route("/get_sentiment/<lat>/<lon>/<radius>", methods=['GET'])
def info(lat, lon, radius):
    # coord = request.args.get('coord')
    # make circle with these coordinates
    lat = float(lat)
    lon = float(lon)
    radius = int(radius)

    # perform aggregate by ranges of lat and long that would be within the circle
    # pipeline = [{ "$geoNear" : {
    #              "near" : { "type" : "Point", "coordinates" : [lat, lon]},
    #              "distanceField": "dist.calculated",
    #              }}]
    # pipeline = [('geoNear', 'places'), ('near', [lat, lon])]

                 # "maxDistance" :  max_distance,
                 # "num" : 100,
                 # "spherical" : True
    print 'hellur',lat, lon, radius
    tweets = handle.tweets.find({"coords": {"$near": [lat, lon]}}).limit(radius)
    json_tweets = []

    for tweet in tweets:
        # refactored to use aggregate in tweets query
        json_tweets.append(dumps(tweet))
        # if in_circle(lat, lon, radius, tweet['coords']):

    # for tweet in json_tweets:
        # print tweet['coords']
        # print type(parse_cords(tweet['coords'])), parse_cords(tweet['coords'])

    return jsonify({'tweets':json_tweets})

# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.run(host='localhost', port=port, debug=True, threaded=True)
