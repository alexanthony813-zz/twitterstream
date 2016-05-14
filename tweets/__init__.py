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


if __name__ == '__main__':
  print("running")
  app.run(threaded=True)
