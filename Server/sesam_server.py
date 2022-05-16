from flask import Flask

app = Flask(__name__)


@app.route("/datasets", methods=["GET"])
def hello():
    return "Hello, world!"


@app.route("/datasets", methods=["POST"])
def hello():
    return "Hello, world!"


@app.route("/datasets/<id>", methods=["GET"])
def hello():
    return "Hello, world!"


@app.route("/datasets/<id>", methods=["DELETE"])
def hello():
    return "Hello, world!"


@app.route("/datasets/<id>/excel", methods=["GET"])
def hello():
    return "Hello, world!"
