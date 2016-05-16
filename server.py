import os
from pymongo import MongoClient
from flask import Flask, render_template, jsonify
from bson.son import SON
is_prod = os.environ.get('IS_HEROKU', None)
three_days_in_seconds = 60*60*24


def in_circle(center_x, center_y, radius, tweet_coords):
    x = tweet_coords[0]
    y = tweet_coords[1]
    square_dist = (center_x - x) ** 2 + (center_y - y) ** 2
    return square_dist <= radius ** 2


def connect():
    if is_prod:
        global connection
        string = 'ds023442.mlab.com:23442'
        uri = string.rsplit()[0]
        connection = MongoClient(uri, port=23442, maxPoolSize=100, waitQueueMultiple=10, connect=False, serverSelectionTimeoutMS=5000)
    else:
        connection = MongoClient('localhost', 27017, maxPoolSize=100, waitQueueMultiple=10, connect=False, serverSelectionTimeoutMS=1)
    if is_prod:
        handle = connection['heroku_0p1s62cb']
        handle.authenticate('heroku_0p1s62cb', 'aev0huua42o4qjnrnen2ilj3a3')
    else:
        handle = connection['tweets']
    return handle


def process_aggregate_response(aggregate_polarity, sample_size):
    # have to iterate to get first, and only, aggregate average value...break out into helper
    if aggregate_polarity is None:
        return {'tweets': 'No tweets available'}
    else:
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
            return {'tweets': sample_size, 'average_polarity': average_polarity, 'most_positive': most_positive, 'most_negative': most_negative}


app = Flask(__name__)
handle = connect()
handle.tweets.create_index([('coords', '2d')])
handle.tweets.create_index('date', expireAfterSeconds=three_days_in_seconds)


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


@app.route("/get_sentiment/<lat>/<lon>/<km_radius>", methods=['GET'])
def get_sentiment(lat, lon, km_radius):
    # basic protection against invalid query params
    try:
        lat = float(lat)
        lon = float(lon)
        degree_radius = (int(km_radius)/111.2)
    except:
        return jsonify({'parameters incorrect': 'please use valid coordinates and a positive numerical value for the radius'})

    if abs(lat) > 90 or abs(lon) > 180 or degree_radius <= 0:
        return jsonify({'parameters incorrect': 'please use valid coordinates and a positive numerical value for the radius'})

    # TODO: expand this aggregator to avoid second tweets query
    query = {"coords": SON([("$near", [lat, lon]), ("$maxDistance", degree_radius)])}
    tweets = handle.tweets.find(query)

    # if sample_size is 0, then we return a json object with a notification
    sample_size = tweets.count() if tweets.count() != 0 else "No tweets available for this location at this time"
    if type(sample_size) == str:
        return jsonify({'tweets': sample_size})

    # use $geoNear here to get actual polarity values in that area, then use aggregator to average
    pipeline = [{"$geoNear": {"near": [lat, lon], "distanceField": "coords", "maxDistance": degree_radius}}, {"$group": {"_id": None, "avgPolarity": {"$avg": "$polarity"}, "mostPositive": {"$max": "$polarity"}, "mostNegative": {"$min": "$polarity"}}}]
    aggregate_polarity = handle.tweets.aggregate(pipeline)

    response = process_aggregate_response(aggregate_polarity, sample_size)
    return jsonify(response)

# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 46012))
    if is_prod:
        app.run(host='0.0.0.0', port=port)
    else:
        app.run(host='localhost', port=port, debug=True)
