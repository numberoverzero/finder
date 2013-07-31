from flask import request, jsonify, abort
from finder import app


@app.route('/echo', methods=["PUT", "POST"])
def echo():
    if not request.json:
        abort(400)
    return jsonify(**request.json)
