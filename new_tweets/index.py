from flask import Flask, render_template, request, redirect
import os
from pymongo import MongoClient
# Set the path
from flask import Flask, request, render_template, jsonify, redirect
from bson.json_util import dumps

def connect():
# Substitute the 5 pieces of information you got when creating
# the Mongo DB Database (underlined in red in the screenshots)
# Obviously, do not store your password as plaintext in practice
    connection = MongoClient('localhost',27017, maxPoolSize=50, waitQueueMultiple=10)
    handle = connection['tweets']
    return handle

app = Flask(__name__)
handle = connect()

@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')

# @app.route("/write", methods=['POST'])
# def write():
#     userinput = request.form.get("userinput")
#     oid = handle.mycollection.insert({"message":userinput})
#     return redirect ("/")

@app.route("/info", methods=['GET'])
def info():
    tweets = handle.tweets.find()
    json_tweets = []

    for tweet in tweets:
        json_tweets.append(dumps(tweet))

    return jsonify({'tweets':json_tweets})

# Remove the "debug=True" for production
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))

    app.run(host='localhost', port=port, debug=True, threaded=True)
