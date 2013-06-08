from flask.ext.restful import Resource, abort
from finder.models import Card
from finder import api
#fields, marshal_with



#gen_fields = {
#    'key': fields.Raw,
#    'salt': fields.Raw,
#    'expiration': fields.Raw
#}


class Greet(Resource):
    #@marshal_with(gen_fields)
    def get(self, name):
        if name in ['test']:
            abort(403, message="Must provide a real name.")
        return {'msg': 'Hello, %s' % name}
api.add_resource(Greet, '/hello/<string:name>')
