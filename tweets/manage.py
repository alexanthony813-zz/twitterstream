# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Flask, request, render_template, jsonify, redirect
from flask.ext.script import Manager, Server
from tweets import app, conn, db
from bson import Binary, Code
from bson.json_util import dumps, loads

manager = Manager(app)

# Turn on debugger by default and reloader
manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
    host = 'localhost')
)

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/get_sentiment')
def getSentiment():
  tweets = db.tweets.find()
  print dumps(tweets)
  # conn.close()
  print jsonify({})
  return jsonify({})


if __name__ == "__main__":
    manager.run()
