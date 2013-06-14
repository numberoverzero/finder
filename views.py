from flask.ext.restful import Resource, abort
from finder import api


class Greet(Resource):
    def get(self, name):
        if name in ['test']:
            abort(403, message="Must provide a real name.")
        return {'msg': 'Hello, %s' % name}
api.add_resource(Greet, '/hello/<string:name>')
