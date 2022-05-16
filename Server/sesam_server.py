from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Datasets(Resource):
    def get(self):
        return 1

    def post(self):
        return 1


class DatasetIds(Resource):
    def get(self, id):
        return 1

    def delete(self, id):
        return 1


class Excel(Resource):
    def get(self):
        return 1


api.add_resource(Datasets, '/datasets')
api.add_resource(DatasetIds, '/datasets/<id>')
api.add_resource(Excel, '/datasets/<id>/excel')
