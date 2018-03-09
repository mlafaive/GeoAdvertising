from flask_restful import Resource, reqparse, HTTPException
from extensions import db
from models import User
from passlib.hash import sha256_crypt

class UserAlreadyExistsError(HTTPException):
	pass

class UserCreate(Resource):
    def post(self):
        # Speicfy a parser with expected arguments
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='name is required')
        parser.add_argument('email', type=str, required=True, help='email is required')
        parser.add_argument('password', type=str, required=True, help='password is required')
        args = parser.parse_args()

        # Check if user already exists
        if User.query.filter_by(email = args["email"]).first() is not None:
           return {'error': 'user already exists'}, 409


        # Hash the password
        args['password'] = sha256_crypt.hash(args['password'])

        # Insert the user into DB
        user = User(**args)
        db.session.add(user)
        db.session.commit()

        return args, 201

class UserDML(Resource):
    def get(self, _email):
        # Check if user exists
        if User.query.filter_by(email = _email).first() is None:
           return {'error': 'user does not exist'}, 400

        # Retrieve User with _email from DB
        user = User.query.filter_by(email = _email).first()
        return user.serialize, 200

    def delete(self, _email):
        # Check if user exists
        if User.query.filter_by(email = _email).first() is None:
           return {'error': 'user does not exist'}, 400

        # Retrieve User with _email
        user = User.query.filter_by(email = _email).first()
        # Remove user from DB
        db.session.delete(user)
        db.session.commit()
        # return
        return {}, 204

    # TODO: Figure out how datetimes should be parsed
    def patch(self, _email):
        # Check if user exists
        if User.query.filter_by(email = _email).first() is None:
           return {'error': 'user does not exist'}, 400

        # Speicfy a parser with expected arguments
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('password', type=str)
        parser.add_argument('last_offer_time')
        parser.add_argument('businesses', type=list)
        parser.add_argument('interests', type=list)
        args = parser.parse_args()

        # Retrieve User with _email
        user = User.query.filter_by(email = _email).first()

        # Encrypt password if it was posted
        if args['password'] is not None:
            args['password'] = sha256_crypt.hash(args['password'])

        # Update the user with any arg that is not None
        for arg in args:
            if args[arg] is not None:
                setattr(user, arg, args[arg])

        # Commit and Return the new user info
        db.session.commit()
        return user.serialize, 200
