import os, random, json, random
import string

from flask import Flask, send_file, request
from flask_restful import Resource, Api, abort
from tablib import Dataset

app = Flask(__name__)
api = Api(app)


def check_name_exists(name):
    datasets = os.listdir('datasets')
    if name not in datasets:
        abort(404, message="File {} does not exist".format(name))


def create_new_entry(data):
    while True:
        new_id = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        new_id = '{}.json'.format(new_id)
        if new_id not in os.listdir('datasets'):
            break

    with open('datasets/{}'.format(new_id), 'w') as f:
        json.dump(data, f)
    return new_id


class Datasets(Resource):
    def get(self):
        dataset_dir = 'datasets'
        files = filter(lambda x: os.path.isfile(os.path.join(dataset_dir, x)), os.listdir(dataset_dir))
        files_sizes = [(fn, os.stat(os.path.join(dataset_dir, fn)).st_size) for fn in files]
        jsonified_file_info = {'file_info': files_sizes}
        return jsonified_file_info

    def post(self):
        new_data = request.json[0]
        new_id = create_new_entry(new_data)
        return new_id, 201


class DatasetIds(Resource):
    def get(self, id):
        check_name_exists(id)
        with open('datasets/{}'.format(id), 'r') as f:
            data = json.load(f)
            return data, 200

    def delete(self, id):
        check_name_exists(id)
        os.remove("datasets/{}".format(id))
        return 204


class Excel(Resource):
    def get(self, id):
        check_name_exists(id)

        temps = os.listdir("temp")
        for t in temps:
            os.remove("temp/{}".format(t))

        with open('datasets/{}'.format(id), 'r') as f:
            json_data = Dataset().load(f, format='json')
            xls_data = json_data.export('xls')
            with open('temp/{}.xls'.format(id[:-5]), 'wb') as tmp:
                tmp.write(xls_data)
            return send_file('temp/{}.xls'.format(id[:-5]))


api.add_resource(Datasets, '/datasets')
api.add_resource(DatasetIds, '/datasets/<id>')
api.add_resource(Excel, '/datasets/<id>/excel')
