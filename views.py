from flask import request, jsonify, abort
from finder import app


@app.route('/<name>', methods=["PUT", "POST"])
def greet(name):
    if not request.json:
        abort(400)
    return jsonify(**{
        'msg': 'Hello, {}'.format(name),
        'json': request.json,
    })
