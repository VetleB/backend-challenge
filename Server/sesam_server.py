from flask import Flask, send_file
from flask_restful import Resource, Api, abort
import os
import json
from tablib import Dataset

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
    def get(self, id):
        check_id_exists(id)
        temps = os.listdir("temp")
        for t in temps:
            os.remove("temp/{}".format(t))

        with open('datasets/{}'.format(id), 'r') as f:
            json_data = Dataset().load(f, format='json')
            xls_data = json_data.export('xls')
            with open('temp/{}.xls'.format(id[:-5]), 'wb') as f:
                f.write(xls_data)
            return send_file('temp/{}.xls'.format(id[:-5]))


api.add_resource(Datasets, '/datasets')
api.add_resource(DatasetIds, '/datasets/<id>')
api.add_resource(Excel, '/datasets/<id>/excel')
