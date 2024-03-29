#!/usr/bin/env python3
from bson import json_util
from flask import Flask, render_template
import pymongo
import os
import config
from flask import request
import logging

logging.basicConfig(filename=config.log_file,
                    level=config.log_level, format='%(asctime)s %(message)s')

app = Flask(__name__)

serverUrl = os.environ.get('MONGO_URL', config.mongo_url)
client = pymongo.MongoClient(serverUrl)

db = client.ephemera
default_collection = db.ephemera

#routes
@app.route("/")
def index():
    collections = db.list_collection_names()
    return render_template('index.html', collections=collections)

#API routes
@app.route("/api")
def api():
    data = default_collection.find()
    return json_util.dumps(data)

@app.route("/api/<collection>")
def api_collection(collection):
    collection = db[collection]
    data = collection.find()
    return json_util.dumps(data)

@app.route("/api/<collection>/add", methods=['POST'])
def api_collection_add(collection):
    collection = db[collection]
    collection.insert_one(request.json)
    data = collection.find()
    return json_util.dumps(data)

@app.route("/api/<collection>/<id>")
def api_collection_id(collection,id):
    collection = db[collection]
    logging.info(id)
    data = collection.find({id:'test'})
    return json_util.dumps(data)

#Data Views
@app.route("/view/<collection>")
def view_api_collection(collection):
    collection_name = collection
    collection = db[collection]
    data = collection.find({},{'_id': 0})
    data = [item for item in data]
    return render_template('view_collection.html',data=data,collection_name=collection_name)

if __name__ == '__main__':
    app.run(debug=config.flask_debug, host=config.flask_host, port=config.flask_port)
