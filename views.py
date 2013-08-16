from flask import request, jsonify, abort
from finder import app, db, controllers, models
from jsonquery import jsonquery

@app.route('/echo', methods=["PUT", "POST"])
def echo():
    if not request.json:
        abort(400)
    return jsonify(**request.json)

@app.route('/card/<string:name>', methods=["GET"])
def card(name):
	query = {
		'column': 'processed_ascii_name',
		'operator': 'ilike',
		'value': name
	}
	card = jsonquery(db.session, models.Card, query).first()
	card_dict = controllers.with_fields(card)
	return jsonify(**card_dict)
