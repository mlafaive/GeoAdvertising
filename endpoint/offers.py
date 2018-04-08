import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (jwt_required, get_jwt_identity)

from extensions import db
from sqlalchemy import exc



import ast
import dateutil
from dateutil import *
from dateutil.tz import *
import datetime

from math import radians, sin, cos, sqrt, atan2


from models import User, Business, Offer, Interest, City




def perms(offer, identity):
	resp = offer.serialize
	resp['isOwner'] = offer.business.manager_address == identity
	return resp


def loc_distance(user_loc,city_loc):
	R=6373.0

	user_lat,user_lon=user_loc
	city_lat,city_lon=city_loc

	user_lat_rad = radians(user_lat)
	user_lon_rad = radians(user_lon)

	city_lat_rad = radians(city_lat)
	city_lon_rad = radians(city_lon)

	diff_lat = user_lat_rad-city_lat_rad
	diff_lon = user_lon_rad-city_lon_rad

	a = sin(diff_lat/2)**2 + cos(user_lat_rad) * cos(city_lat_rad) * sin(diff_lon/2)**2
	c = 2 * atan2(sqrt(a), sqrt(1-a))

	dist = R * c

	return dist


def km_to_mi(km):
	return 0.62137119224*km


def mi_to_km(mi):
	return 1.60934*mi





class AllOffers(Resource):
	@jwt_required
	def get(self):


		email = get_jwt_identity()


		#
		# PARSE THE POSTED ARGUMENTS
		#
		parser = reqparse.RequestParser()
		parser.add_argument('latitude', type=float, location='args')
		parser.add_argument('longitude', type=float, location='args')
		parser.add_argument('distance', type=float, location='args')
		args = parser.parse_args()

		if (args["distance"] is None):
			filter_dist = mi_to_km(1)
		else:
			filter_dist = mi_to_km(args["distance"])




		if (args['latitude'] is None or args['longitude'] is None):
			#
			# QUERY AND SERIALIZE ALL OFFERS
			#
			resp = { "offers": [i.serialize for i in Offer.query.all()] }, 200

			return resp

		else:

			# Pseudo code description of algorithm
			#
			#
			# Check if user exists
			#  if no, return error
			#
			# If user exists, check if enough time has passed since last offer
			#  if no, return error
			#
			# Get all cities
			# Calculate distance from cities to user
			# Sort list of cities to find closest city
			#  if closest city is further than 15 miles from user, return error
			#
			# If no businesses are located in closest city, return error
			#
			# For each business closer than 0.125mi to user in the closest city
			#  for each offer of business
			#   if offer shares any interest with user add it to list
			#
			# If any offers in list, return random offer

			# Retrieve User with _email from DB
			user = User.query.get(email)
			# Check if user exists
			if user is None:
			   return {'error': 'user does not exist'}, 400

			
			
			

			#
			# FIND CLOSEST CITY TO USER
			#
			# Find all cities
			cities = City.query.all()
			# If no cities found, do not proceed with search
			if len(cities)==0:
				return {'offers': []}, 200

			# Calculate distance to user for each city
			cities = [(city, loc_distance((args['latitude'],args['longitude']),(city.latitude, city.longitude))) for city in cities]
			# Sort list of cities on distance to user in increasing order
			cities.sort(key=lambda tup: tup[1])

			# Get closest city to user at first position in list
			closest_city = cities[0]

			# If the closest city is more than 24.14km(15mi) from user location, return no offers
			if closest_city[1] > 24.14:
				return {'offers': []}, 200

			# Get city object of closest city to user
			closest_city = closest_city[0]





			#
			# CHECK IF THERE ARE BUSINESSES IN CLOSEST CITY
			#
			if len(closest_city.businesses)==0:
				return {'offers', []}, 200



			# Get current time in utc, matching timezone of user.last_offer_time
			current_time = datetime.datetime.now(datetime.timezone.utc)

			#
			# FIND RELEVANT, LIVE OFFERS IN CLOSEST CITY
			#
			close_offers = []
			for business in closest_city.businesses:
				# Check distance from business to user
				business_dist = loc_distance((args['latitude'],args['longitude']),(business.latitude, business.longitude))
				if business_dist < filter_dist:
					# Consider all offers of businesses within 0.2km(0.125mi) of user
					for offer in business.offers:

						offer_live = (offer.start_time < current_time and current_time < offer.end_time)
						offer_relevant = (not set(offer.interests).isdisjoint(user.interests))

						# If offer is currently active and relevant to the user, add it to list
						if offer_live and offer_relevant:
							close_offers.append((offer,business_dist))

			# If no offers were found to be close, live and relevant, return no offer
			if len(close_offers)==0:
				return {'offers': []}, 200






			#
			# Otherwise return a random close, live and relevant offer
			#
			# Update last_offer_time of user to now
			user.last_offer_time = current_time
			db.session.commit()



			max_results=100
			close_offers = close_offers[:max_results]
			close_offers.sort(key=lambda tup: tup[1])



			result_data = []
			for close_offer in close_offers:
				offer, dist = close_offer
				offer_data = offer.serialize
				offer_data["distance"] = km_to_mi(dist)
				result_data.append(offer_data)

			return {'offers': result_data}, 200

class AcceptOffer(Resource):
	@jwt_required
	def post(self, _id):
		#
		# QUERY FOR OFFER WITH OFFER ID
		#
		offer = Offer.query.get(_id)
		# If no offer exists with id, return error
		if offer is None:
			return {'error': 'offer does not exist'}

		email = get_jwt_identity()

		user = User.query.get(email)
		# Check if user exists
		if user is None:
			return {'error': 'user does not exist'}, 400
		offer.users_accepted.append(user)
		db.session.commit()
		
		return 200


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

		email = get_jwt_identity()

		user = User.query.get(email)
		# Check if user exists
		if user is None:
			return {'error': 'user does not exist'}, 400
		offer.users_viewed.append(user)
		db.session.commit()
		b = offer.business
		resp = perms(offer, email)
		resp['business']['latitude'] = b.latitude
		resp['business']['longitude'] = b.longitude

		resp['accepted'] = offer in user.offers_accepted
		
		return resp

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
		parser.add_argument('interests', type=list, location='json')
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
			if not isinstance(args["interests"], list):
				return {'error': 'interests must be a list'}, 400
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
		resp = offer.serialize
		resp['isOwner'] = True
		return resp



	@jwt_required
	def delete(self, _id):
		#
		# ENSURE OFFER TO DELETE EXISTS
		#
		offer = Offer.query.get(_id)
		# If no offer exists with id, return error
		if offer is None:
			return {'error': 'offer does not exist'}


		#
		# ENSURE USER REQUESTING DELETE MANAGES BUSINESS OWNING OFFER
		#
		# Get business with offer's business id
		business = Business.query.get(offer.business_id)
		if business.manager_address != get_jwt_identity():
			flask.abort(403)


		# Delete the business
		db.session.delete(offer)
		db.session.commit()

		# Return with a 204
		return '', 204




class BusinessOffers(Resource):
	@jwt_required
	def get(self, _id):
		#
		# Ensure the business exists
		#
		business = Business.query.get(_id)
		if business is None:
		    return {'error': 'business does not exist'}, 400

		email = get_jwt_identity()
		# Return list of all offers the business has
		resp = {'offers': [perms(o, email) for o in business.offers]}
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
		parser.add_argument('interests', type=list, required=True, help='list of interests is required', location='json')
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
		if not isinstance(args["interests"], list):
				return {'error': 'interests must be a list'}, 400

		print("interests", args["interests"])
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


		resp = offer.serialize
		resp['isOwner'] = True
		return resp, 201





