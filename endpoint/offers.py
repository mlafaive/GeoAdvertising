import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from extensions import db
import dateutil
from dateutil import *
import ast
from models import Business, Offer, Interest

class AllOffers(Resource):
	@jwt_required
	def get(self):
		# Retrieve User with _email from DB
		Offer.query.all()
		resp = { "offers": [i.serialize for i in Offer.query.all()] }
		print(resp)
		return resp

class SingleOffer(Resource):
	@jwt_required
	def get(self, _id):
		# Ensure the offer exists
		offer = Offer.query.get(_id)
		if offer is None:
			return {'error': 'offer does not exist'}

		return offer.serialize

	@jwt_required
	def patch(self, _id):
		# Ensure the offer exists
		offer = Offer.query.get(_id)
		if offer is None:
			return {'error': 'offer does not exist'}

		# Ensure the user requesting the patch manages the business
		business = Business.get(offer.business_id)
		if business.manager != get_jwt_identity():
			flask.abort(403)

		# Parse the request body
		parser = reqparse.RequestParser()
		parser.add_argument('start_time', type=str)
		parser.add_argument('end_time', type=str)
		parser.add_argument('description', type=str)
		parser.add_argument('interests', type=str)
		args = parser.parse_args()

		# Convert timestamps to datetimes and update
		if args["start_time"] is not None:
			offer.start_time = dateutil.parser.parse(args["start_time"])
		if args["end_time"] is not None:
			offer.end_time = dateutil.parser.parse(args["end_time"])

		# Convert interests to a list and update
		if args["interests"] is not None:
			# Parse the string
			interests = ast.literal_eval(args["interests"])

			# Remove previous interests
			offer.interests[:] = []

			# Add new interests
			for _interest in interests:
				interest = Interst.query.filter_by(name=_interest)
				if interest is none:
					interest = Interest(_interest)
				offer.interests.append(interest)

		if args["description"] is not None:
			offer.description = args["description"]



class BusinessOffers(Resource):
	@jwt_required
	def get(self, _id):
		# Ensure the business exists
		business = Business.query.get(_id)
		if business is None:
		    return {'error': 'business does not exist'}, 400

		# TODO: return list of actual offer objects
		# Return list of offer ids
		return {'offers': [o.get_public_data for o in business.offers]}


	@jwt_required
	def post(self, _id):
		# Ensure the business exists
		business = Business.query.get(_id)
		if business is None:
		    return {'error': 'business does not exist'}, 400

		# Ensure the user manages the business
		if get_jwt_identity() != business.manager_address:
		    flask.abort(403)

		# Parse Arguments
		parser = reqparse.RequestParser()
		parser.add_argument('start_time', type=str, required=True, help='start_time is required and must be in UTC format')
		parser.add_argument('end_time', type=str, required=True, help='end_time is required and must be in UTC format')
		parser.add_argument('description', type=str, required=True, help='description of the offer is required')
		parser.add_argument('interests', type=str, required=True, help='list of interests is required')
		args = parser.parse_args()

		# Create Datetime objects from UTC strings
		# Assumes start_time and end_time are already converted to UTC,
		start_time = dateutil.parser.parse(args["start_time"])
		end_time = dateutil.parser.parse(args["end_time"])

		# Create the offer
		data = {
		    'business_id': business.id,
		    'start_time': start_time,
		    'end_time': end_time,
		    'description': args['description']
		}
		offer = Offer(**data)

		# Append the interests to the offer
		for _interest in ast.literal_eval(args['interests']):
			interest = Interest.query.filter_by(name=_interest).first()
			if interest is None:
				interest = Interest(_interest)
			offer.interests.append(interest)

		db.session.add(offer)
		db.session.commit()

		return offer.serialize, 201
