import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from extensions import db
from sqlalchemy import exc


import ast
import dateutil
from dateutil import *
from dateutil.tz import *


from models import Business, Offer, Interest



class AllOffers(Resource):
	@jwt_required
	def get(self):
		#
        # QUERY AND SERIALIZE ALL OFFERS
        #
		resp = { "offers": [i.serialize for i in Offer.query.all()] }
		
		return resp



class SingleOffer(Resource):
	@jwt_required
	def get(self, _id):
		#
        # QUERY FOR OFFER WITH OFFER ID 
        #
		offer = Offer.query.get(_id)
		# If no offer exists with id, return error
		if offer is None:
			return {'error': 'offer does not exist'}

		return offer.serialize

	@jwt_required
	def patch(self, _id):
		#
        # ENSURE OFFER TO PATCH EXISTS
        #
		offer = Offer.query.get(_id)
		# If no offer exists with id, return error
		if offer is None:
			return {'error': 'offer does not exist'}



		#
        # ENSURE USER REQUESTING PATCH MANAGES BUSINESS OWNING OFFER
        #
		# Get business with offer's business id
		business = Business.query.get(offer.business_id)
		if business.manager_address != get_jwt_identity():
			flask.abort(403)



		#
		# PARSE THE REQUEST BODY
		#
		parser = reqparse.RequestParser()
		parser.add_argument('start_time', type=str)
		parser.add_argument('end_time', type=str)
		parser.add_argument('description', type=str)
		parser.add_argument('interests', type=list)
		args = parser.parse_args()



		#
		# Convert timestamps to datetimes and update
		#
		if args["start_time"] is not None:
			offer.start_time = args["start_time"]
		if args["end_time"] is not None:
			offer.end_time = args["end_time"]



		#
		# Convert interests to a list and update
		#
		if args["interests"] is not None:
			# Make sure all are integers
			if not all(isinstance(x,int) for x in args["interests"]):
				return {'error': 'ids must be integers'}, 400
			# Convert interest names to Interest objects
			new_interests = []
			for _interest in args["interests"]:
				interest = Interest.query.get(_interest)
				if interest is None:
					return {'error': 'interest does not exist'}, 400
				new_interests.append(interest)

			# Replace the offer's interest with the new list
			offer.interests[:] = new_interests

		#
		# Update description
		#
		if args["description"] is not None:
			offer.description = args["description"]



		# Commit changes and return
		db.session.commit()
		return offer.serialize





class BusinessOffers(Resource):
	@jwt_required
	def get(self, _id):
		#
		# Ensure the business exists
		#
		business = Business.query.get(_id)
		if business is None:
		    return {'error': 'business does not exist'}, 400


		# Return list of all offers the business has
		resp = {'offers': [o.serialize for o in business.offers]}
		return resp



	@jwt_required
	def post(self, _id):
		#
		# Ensure the business exists
		#
		business = Business.query.get(_id)
		if business is None:
			return {'error': 'business does not exist'}, 400

		#
		# Ensure the user manages the business
		#
		if get_jwt_identity() != business.manager_address:
			flask.abort(403)



		#
		# Parse Arguments
		#
		parser = reqparse.RequestParser()
		parser.add_argument('start_time', type=str, required=True, help='start_time is required and must be in UTC format')
		parser.add_argument('end_time', type=str, required=True, help='end_time is required and must be in UTC format')
		parser.add_argument('description', type=str, required=True, help='description of the offer is required')
		parser.add_argument('interests', type=list, required=True, help='list of interests is required')
		args = parser.parse_args()



		#
		# Create the offer
		#
		data = {
			'business_id': business.id,
			'start_time': args['start_time'],
			'end_time': args['end_time'],
			'description': args['description']
		}
		offer = Offer(**data)

		# Check if all integers
		if not all(isinstance(x,int) for x in args["interests"]):
			return {'error': 'interest ids must be integers'}, 400
		# Convert interest names to Interest objects
		new_interests = []
		for _interest in args["interests"]:
			interest = Interest.query.get(_interest)
			if interest is None:
				return {'error': 'interest does not exist'}, 400
			new_interests.append(interest)

		# Replace the offer's interest with the new list
		offer.interests[:] = new_interests


		db.session.add(offer)


		#
		# Hanle integrity errors with try/except
		#
		try:
			db.session.commit()
		except exc.IntegrityError:
			db.session.rollback()
			return {'error': 'offer with same description already owned by business'}, 400


		return offer.serialize, 201
