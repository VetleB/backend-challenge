import os, random, json, random
import string

from flask import Flask, send_file, request
from flask_restful import Resource, Api, abort
from tablib import Dataset

app = Flask(__name__)
api = Api(app)


def check_name_exists(name):
    """
    Checks if a name exists in among existing entries

    :param name: Name to be checked
    :return:
    """
    datasets = os.listdir('datasets')
    if name not in datasets:
        abort(404, message="File {} does not exist".format(name))


def create_new_entry(data):
    """
    Create new entry with random id

    :param data: Data that will become the new entry
    :return: The id of the new object
    """
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
        """
        Get names and corresponding file sizes of all dataset entries

        :return: JSON object containing a list of tuples (file_name, file_size)
        """
        dataset_dir = 'datasets'
        files = filter(lambda x: os.path.isfile(os.path.join(dataset_dir, x)), os.listdir(dataset_dir))
        files_sizes = [(fn, os.stat(os.path.join(dataset_dir, fn)).st_size) for fn in files]
        jsonified_file_info = {'file_info': files_sizes}
        return jsonified_file_info, 200

    def post(self):
        """
        Create a new dataset entry

        :return: Id of the created entry
        """
        new_data = request.json[0]
        new_id = create_new_entry(new_data)
        return new_id, 201


class DatasetIds(Resource):
    def get(self, id):
        """
        Fetch the dataset entry matching the id

        :param id: Id of the entry to be fetched
        :return: JSON object
        """
        check_name_exists(id)
        with open('datasets/{}'.format(id), 'r') as f:
            data = json.load(f)
            return data, 200

    def delete(self, id):
        """
        Delete dataset entry matching the id

        :param id: Id of entry to be deleted
        :return:
        """
        check_name_exists(id)
        os.remove("datasets/{}".format(id))
        return 204


class Excel(Resource):
    def get(self, id):
        """
        Fetch the dataset entry matching the id and convert it to a .xls file

        :param id: Id of the entry to be fetched
        :return: .xls file
        """
        check_name_exists(id)

        temps = os.listdir("temp")
        for t in temps:
            os.remove("temp/{}".format(t))

        with open('datasets/{}'.format(id), 'r') as f:
            json_data = Dataset().load(f, format='json')
            xls_data = json_data.export('xls')
            with open('temp/{}.xls'.format(id[:-5]), 'wb') as tmp:
                tmp.write(xls_data)
            return send_file('temp/{}.xls'.format(id[:-5])), 200


api.add_resource(Datasets, '/datasets')
api.add_resource(DatasetIds, '/datasets/<id>')
api.add_resource(Excel, '/datasets/<id>/excel')
