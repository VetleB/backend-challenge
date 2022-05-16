from flask import Flask
from flask_restful import Resource, Api, abort
import os
import json

app = Flask(__name__)
api = Api(app)


def check_id_exists(id):
    datasets = os.listdir('datasets')
    if id not in datasets:
        abort(404, message="Id {} does not exist".format(id))


class Datasets(Resource):
    def get(self):
        return 1

    def post(self):
        return 1


class DatasetIds(Resource):
    def get(self, id):
        check_id_exists(id)
        with open('datasets/{}'.format(id), 'r') as f:
            data = json.load(f)
            return data, 200

    def delete(self, id):
        check_id_exists(id)
        os.remove("datasets/{}".format(id))
        return '', 204


class Excel(Resource):
    def get(self):
        return 1


api.add_resource(Datasets, '/datasets')
api.add_resource(DatasetIds, '/datasets/<id>')
api.add_resource(Excel, '/datasets/<id>/excel')
