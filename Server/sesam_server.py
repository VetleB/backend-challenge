import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


def check_id_exists(id):
    ids = os.listdir("datasets")
    return id in ids


@app.route("/datasets", methods=["GET"])
def get_entries():
    return "Hello, world!"


@app.route("/datasets", methods=["POST"])
def create_entry():
    new_data = json.loads(request.data)
    return "Hello, world!"


@app.route("/datasets/<id>", methods=["GET"])
def get_entry(id):
    if check_id_exists(id):
        with open("datasets/{}".format(id), 'r') as f:
            data = json.load(f)
            return jsonify(data)
    else:
        return '', 404


@app.route("/datasets/<id>", methods=["DELETE"])
def delete_entry():
    return "Hello, world!"


@app.route("/datasets/<id>/excel", methods=["GET"])
def get_excel():
    return "Hello, world!"
