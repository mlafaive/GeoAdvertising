import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)
from extensions import db
from models import User, Interest, City, Business
from passlib.hash import sha256_crypt
import datetime
from math import radians, sin, cos, sqrt, atan2
import ast
import re
import random

# TODO: Parse Input // handle the errors properly

class UserCreate(Resource):
	def post(self):
		# Speicfy a parser with expected arguments
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str, required=True, help='name is required')
		parser.add_argument('email', type=str, required=True, help='email is required')
		parser.add_argument('password', type=str, required=True, help='password is required')
		args = parser.parse_args()


		# Scrub name argument for length between 1 and 50
		# User name can include any characters
		if re.match('^.{1,50}$', args['name']) is None:
			return {'error': 'specified name is too short or too long'}, 400

		# Scrub email argument for length between 1 and 50
		if re.match('^.{1,50}$', args['email']) is None:
			return {'error': 'specified email is too short or too long'}, 400
		# Scrub email argument for formatting according to RFC 5322
		if re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', args['email']) is None:
			return {'error': 'specified email is not valid'}, 400

		# Scrub password argument for length between 8 and 50
		if re.match('^.{8,50}$', args['password']) is None:
			return {'error': 'specified password is too short or too long'}, 400

        




		# Retrieve User with _email from DB
		user = User.query.get(args["email"])

		# Check if user already exists
		if user is not None:
		   return {'error': 'user already exists'}, 409


		# Hash the password
		args['password'] = sha256_crypt.hash(args['password'])

		# Insert the user into DB
		user = User(**args)
		db.session.add(user)
		db.session.commit()

		return {
			'access_token': create_access_token(identity = args["email"]),
			'refresh_token': create_refresh_token(identity = args["email"])
		}

class UserRefresh(Resource):
	@jwt_refresh_token_required
	def post(self):
		return {
			'access_token': create_access_token(identity = get_jwt_identity())
		}


class UserBusinesses(Resource):
	@jwt_required
	def get(self, _email):

		# Scrub email argument for length between 1 and 50
		if re.match('^.{1,50}$', _email) is None:
			return {'error': 'specified email is too short or too long'}, 400
		# Scrub email argument for formatting according to RFC 5322
		if re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', _email) is None:
			return {'error': 'specified email is not valid'}, 400



		# Ensure requested email and token identity are the same
		if get_jwt_identity() != _email:
			flask.abort(403)
		# Retrieve User with _email from DB
		user = User.query.get(_email)

		# Check if user exists
		if user is None:
		   return {'error': 'user does not exist'}, 400

		resp = {'businesses': [b.serialize for b in user.businesses]}
		print(resp)
		return resp


class UserLogin(Resource):
	def post(self):
		# Specify a parser with expected arguments
		parser = reqparse.RequestParser()
		parser.add_argument('email', type=str, required=True, help='email is required')
		parser.add_argument('password', type=str, required=True, help='password is required')
		args = parser.parse_args()


		# Scrub email argument for length between 1 and 50
		if re.match('^.{1,50}$', args['email']) is None:
			return {'error': 'specified email is too short or too long'}, 400
		# Scrub email argument for formatting according to RFC 5322
		if re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', args['email']) is None:
			return {'error': 'specified email is not valid'}, 400


		# Scrub password argument for length between 8 and 50
		if re.match('^.{8,50}$', args['password']) is None:
			return {'error': 'specified password is too short or too long'}, 400


		# Retrieve the user
		user = User.query.get(args["email"])

		# If user does not exist return an error
		if user is None:
			return {'error': 'the username or password provided is invalid'}, 400

		# If password is incorrect, return an error
		if sha256_crypt.verify(args["password"], user.password) is False:
			return {'error': 'the username or password provided is invalid'}, 400
		# Else, create a jwt for the user and return
		return {
			'access_token': create_access_token(identity = args["email"]),
			'refresh_token': create_refresh_token(identity = args["email"])
		}

class UserDML(Resource):
	@jwt_required
	def get(self, _email):
		# Scrub email argument for length between 1 and 50
		if re.match('^.{1,50}$', _email) is None:
			return {'error': 'specified email is too short or too long'}, 400
		# Scrub email argument for formatting according to RFC 5322
		if re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', _email) is None:
			return {'error': 'specified email is not valid'}, 400


		# Ensure requested email and token identity are the same
		if get_jwt_identity() != _email:
			flask.abort(403)


		# Retrieve User with _email from DB
		user = User.query.get(_email)

		# Check if user exists
		if user is None:
		   return {'error': 'user does not exist'}, 400


		return user.serialize, 200

	@jwt_required
	def delete(self, _email):
		# Scrub email argument for length between 1 and 50
		if re.match('^.{1,50}$', _email) is None:
			return {'error': 'specified email is too short or too long'}, 400
		# Scrub email argument for formatting according to RFC 5322
		if re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', _email) is None:
			return {'error': 'specified email is not valid'}, 400


		# Ensure requested email and token identity are the same
		if get_jwt_identity() != _email:
			flask.abort(403)

		# Retrieve User with _email from DB
		user = User.query.get(_email)

		# Check if user exists
		if user is None:
		   return {'error': 'user does not exist'}, 400


		# Remove user from DB
		db.session.delete(user)
		db.session.commit()
		# return
		return {}, 204

	# TODO: Figure out how datetimes should be parsed
	@jwt_required
	def patch(self, _email):

		# Scrub email argument for length between 1 and 50
		if re.match('^.{1,50}$', _email) is None:
			return {'error': 'specified email is too short or too long'}, 400
		# Scrub email argument for formatting according to RFC 5322
		if re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', _email) is None:
			return {'error': 'specified email is not valid'}, 400


		# Ensure requested email and token identity are the same
		if get_jwt_identity() != _email:
			flask.abort(403)


		# Retrieve User with _email from DB
		user = User.query.get(_email)

		# Check if user exists
		if user is None:
			return {'error': 'user does not exist'}, 400


		# Speicfy a parser with expected arguments
		parser = reqparse.RequestParser()
		parser.add_argument('name', type=str)
		parser.add_argument('password', type=str)
		parser.add_argument('old_password', type=str)
		parser.add_argument('last_offer_time', type=str)
		parser.add_argument('interests', type=list, location='json')
		args = parser.parse_args()

		#
		if args["name"] is not None:
			# Scrub name argument for length between 1 and 50
			# User name can include any characters
			if re.match('^.{1,50}$', args['name']) is None:
				return {'error': 'specified name is too short or too long'}, 400

			user.name = args["name"]


		
		# Encrypt password if it was posted
		if args['password'] is not None:
			if args["old_password"] is None:
				return {'error': 'must send old password to update'}, 400

			if re.match('^.{8,50}$', args["old_password"]) is None:
				return {'error': 'specified password is too short or too long'}, 400

			if sha256_crypt.verify(args["old_password"], user.password) is False:
				return {'error': 'the password provided is invalid'}, 400

			# Scrub password argument for length between 8 and 50
			if re.match('^.{8,50}$', args['password']) is None:
				return {'error': 'specified password is too short or too long'}, 400

			user.password = sha256_crypt.hash(args['password'])




		if args['last_offer_time'] is not None:
			# Assumes time string format(m/d/y hour:minute, ex: 01/28/2018 15:23)
			user.last_offer_time = args['last_offer_time']

		# Convert string representation of interests into a list
		if args['interests'] is not None:
			# Convert interest names to Interest objects
			new_interests = []

			if not isinstance(args["interests"], list):
				return {'error': 'interests must be a list'}, 400

			for _interest in args["interests"]:
				if not isinstance(_interest, int):
					return {'error': 'interest ids must be integers'}, 400

				interest = Interest.query.get(_interest)
				if interest is None:
					return {'error': 'interest does not exist'}, 400
				new_interests.append(interest)

			# Replace the users's interest with the new list
			user.interests[:] = new_interests

		# Commit and Return the new user info
		db.session.commit()
		return user.serialize, 200



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




class UserOffers(Resource):
	@jwt_required
	def post(self, _email):
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




		# Scrub email argument for length between 1 and 50
		if re.match('^.{1,50}$', _email) is None:
			return {'error': 'specified email is too short or too long'}, 400
		# Scrub email argument for formatting according to RFC 5322
		if re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)', _email) is None:
			return {'error': 'specified email is not valid'}, 400


		#
		# Ensure requested email and token identity are the same
		#
		if get_jwt_identity() != _email:
			flask.abort(403)


		


		# Retrieve User with _email from DB
		user = User.query.get(_email)
		# Check if user exists
		if user is None:
		   return {'error': 'user does not exist'}, 400



		#
		# CHECK IF ENOUGH TIME HAS PASSED SINCE LAST OFFER
		#
		# Get current time in utc, matching timezone of user.last_offer_time
		current_time = datetime.datetime.now(datetime.timezone.utc)
		# If difference in time between now and last offer is less than expected
		#  return error, and no offer
		if current_time - user.last_offer_time < datetime.timedelta(minutes=1):
			return {'result': 'no offer at this time'}, 404
		



		#
		# PARSE THE POSTED ARGUMENTS
		#
		parser = reqparse.RequestParser()
		parser.add_argument('latitude', type=float)
		parser.add_argument('longitude', type=float)
		args = parser.parse_args()





		#
		# FIND CLOSEST CITY TO USER
		#
		# Find all cities
		cities = City.query.all()
		# If no cities found, do not proceed with search
		if len(cities)==0:
			return {'result': 'you are not located near any city'}, 404

		# Calculate distance to user for each city
		cities = [(city, loc_distance((args['latitude'],args['longitude']),(city.latitude, city.longitude))) for city in cities]
		# Sort list of cities on distance to user in increasing order
		cities.sort(key=lambda tup: tup[1])

		# Get closest city to user at first position in list
		closest_city = cities[0]

		# If the closest city is more than 24.14km(15mi) from user location, return no offers
		if closest_city[1] > 24.14:
			return {'result': 'you are not located near any city'}, 404

		# Get city object of closest city to user
		closest_city = closest_city[0]





		#
		# CHECK IF THERE ARE BUSINESSES IN CLOSEST CITY 
		#
		if len(closest_city.businesses)==0:
			return {'result', 'there are no businesses in the closest city to you'}, 404
		



		#
		# FIND RELEVANT, LIVE OFFERS IN CLOSEST CITY
		#
		close_offers = []
		for business in closest_city.businesses:
			# Check distance from business to user
			business_dist = loc_distance((args['latitude'],args['longitude']),(business.latitude, business.longitude))
			if business_dist < 0.3:
				# Consider all offers of businesses within 0.2km(0.125mi) of user
				for offer in business.offers:

					offer_live = (offer.start_time < current_time and current_time < offer.end_time)
					offer_relevant = (not set(offer.interests).isdisjoint(user.interests))

					# If offer is currently active and relevant to the user, add it to list
					if offer_live and offer_relevant:
						close_offers.append((offer,business_dist))

		# If no offers were found to be close, live and relevant, return no offer
		if len(close_offers)==0:
			return {'result': 'there are no close offers'}, 404
		





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






















