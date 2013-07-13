from flask.ext.restful import Resource, abort, reqparse
from finder import api

parser = reqparse.RequestParser()
parser.add_argument('age', type=str)


class Greet(Resource):
    def get(self, name):
        args = parser.parse_args()
        if name in ['test']:
            abort(403, message="Must provide a real name.")
        return {'msg': 'Hello, %s' % name, 'age': args['age']}
api.add_resource(Greet, '/hello/<string:name>')
