import json
from pprint import pprint
import flask
from flask import *
from models import User
from extensions import db
from passlib.hash import sha256_crypt

users_api = Blueprint("users_api", __name__)

@users_api.route('/api/users/', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        resp = {
            "users": [i.serialize for i in Users.query.all()]
        }
        return flask.jsonify(resp)
    if request.method == "POST":
        try:
            # Get JSON from the request
            req = flask.request.get_json()

            # Check if account exists (e-mails are unique)
            exists = db.session.query(Users.id).filter_by(email_address = req["email_address"]).scalar()
            if exists:
                raise ValueError('An account with this email already exists.')

            # Create the user in the database
            return create_user(req)
        except (TypeError, ValueError) as e:
            return flask.jsonify({"status": 400, "msg": str(e)})

def create_user(req):
    if req is None:
        return flask.jsonify({"status": 400, "msg": "invalid request"})

    # Hash the password and overwrite
    req["password"] = sha256_crypt.hash(req["password"])

    # Add the user to SQLAlchemy
    new_user = Users(**req)
    db.session.add(new_user)
    db.session.commit()

    return flask.jsonify(req, 201)

@users_api.route('/api/users/<string:email>/', methods=['GET', 'PATCH', 'DELETE'])
def user(email):
    # Return an error if the user does not exist
    user = Users.query.filter_by(email_address = email).first()
    if user is None:
        return flask.jsonify({
            "status": 400,
            "msg": "An account with this email does not exist."
        })

    if request.method == 'GET':
        return flask.jsonify(user.serialize)
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return ('', 204)
    if request.method == 'PATCH':
        # Get the request data
        req = flask.request.get_json()

        # Create a list of valid update keys
        valid = ["name", "phone_numer", "password", "dob"]

        # Error out if any requested keys are not valid
        for key in req.keys():
            if key not in valid:
                return flask.jsonify({"status": 400, "msg": "patch request invalid"})

        # Update valid fields
        if 'name' in req:
            user.name = req["name"]
        if 'phone_number' in req:
            user.phone_number = req["phone_number"]
        if 'password' in req:
            user.password = sha256_crypt.hash(req["password"])
        if 'dob' in req:
            user.dob = req["dob"]

        # commit
        db.session.commit()

        # return the new user data
        return flask.jsonify(user.serialize)
