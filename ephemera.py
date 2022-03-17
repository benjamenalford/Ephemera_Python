#!/usr/bin/env python3
from bson import json_util
from flask import Flask
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

if __name__ == '__main__':
    app.run(debug=config.flask_debug, host=config.flask_host, port=config.flask_port)
