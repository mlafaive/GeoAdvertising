import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)
from extensions import db
from models import User, Interest
from passlib.hash import sha256_crypt
from datetime import datetime
import ast
import re

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
		parser.add_argument('last_offer_time', type=str)
		parser.add_argument('interests', type=str)
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
			# Scrub password argument for length between 8 and 50
			if re.match('^.{8,50}$', args['password']) is None:
				return {'error': 'specified password is too short or too long'}, 400

			user.password = sha256_crypt.hash(args['password'])




		if args['last_offer_time'] is not None:
			# Assumes time string format(m/d/y hour:minute, ex: 01/28/2018 15:23)
			user.last_offer_time = args['last_offer_time']

		# Convert string representation of interests into a list
		if args['interests'] is not None:
			# Parse the string
			interests = ast.literal_eval(args["interests"])

			# Convert interest names to Interest objects
			new_interests = []
			for _interest in interests:
				interest = Interest.query.filter_by(name=_interest).first()
				if interest is None:
					interest = Interest(_interest)
				new_interests.append(interest)

			# Replace the users's interest with the new list
			user.interests[:] = new_interests

		# Commit and Return the new user info
		db.session.commit()
		return user.serialize, 200
