# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, jsonify, redirect
from flask.ext.script import Manager, Server
from tweets import app, conn, db
from bson import Binary, Code
from bson.json_util import dumps, loads

from flask import Flask
# from flask.ext.mongoengine import MongoEngine
# from mongokit import Connection, Document
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(__name__)
conn = MongoClient('localhost', 27017)
db = conn.tweets.tweets

# connection = Connection
# db = MongoEngine(app)
# finds = db.find()

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/get_sentiment')
def getSentiment():
  tweets = db.find()
  print dumps(tweets)
  # conn.close()
  print jsonify({})
  return jsonify({})


if __name__ == '__main__':
  print("running")
  app.run(threaded=True)
