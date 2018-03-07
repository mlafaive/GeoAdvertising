import json
from pprint import pprint
import flask
from flask import *
from models import Offer
from extensions import db
import re

offers_api = Blueprint("offers_api", __name__)

@offers_api.route('/api/offers/', methods=['GET', 'POST'])
def offers():
	if request.method == "GET":
		#return all offers
		resp = jsonify({
			"offers": [i.serialize for i in Offer.query.all()]
			})
		resp.status_code = 200
		return resp
	if request.method == "POST":
		#create an offer
		try:
            # Get JSON from the request

            # TODO validate request

			req = request.get_json()

			# Check if business creating the offer exists (business_id are unique)
			exists = db.session.query(Offer.business_id).get(req["business_id"]).scalar() is not None
			if exists:
				raise ValueError('No business with this id exists.')

            # Create the user in the database
			return create_offer(req)
		except (TypeError, ValueError) as e:
		    resp = jsonify({"msg": str(e)})
		    resp.status_code = 400
		    return resp

def create_offer(req):
    if req is None:
        resp = jsonify({"msg": "invalid request"})
        resp.status_code = 400
        return resp

    #check that times are valid in offer
    #for i in req["availability"]
   	#	if req["availability"]["start"]

    # Add the offer to SQLAlchemy
    new_user = Offer(**req)
    db.session.add(new_offer)
    db.session.commit()

    resp = jsonify(new_offer.serialize)
    resp.status_code = 201
    return resp
	


