import json
from pprint import pprint
import flask
from flask import *
from models import User
from extensions import db
from passlib.hash import sha256_crypt
import base64
import re

users_api = Blueprint("users_api", __name__)

@users_api.route('/api/users/', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        resp = jsonify({
            "users": [i.serialize for i in User.query.all()]
        })
        resp.status_code = 200
        return resp
    if request.method == "POST":
        try:
            # Get JSON from the request

            # TODO validate request

            req = request.get_json()

            # Check if account exists (e-mails are unique)
            exists = db.session.query(User.email).get(req["email_address"]).scalar() is not None
            if exists:
                raise ValueError('An account with this email already exists.')

            # Create the user in the database
            return create_user(req)
        except (TypeError, ValueError) as e:
            resp = jsonify({"msg": str(e)})
            resp.status_code = 400
            return resp

def create_user(req):
    if req is None:
        resp = jsonify({"msg": "invalid request"})
        resp.status_code = 400
        return resp

    # TODO validate request

    # Hash the password and overwrite
    req["password"] = sha256_crypt.hash(req["password"])

    # Add the user to SQLAlchemy
    new_user = User(**req)
    db.session.add(new_user)
    db.session.commit()

    resp = jsonify(new_user.serialize)
    resp.status_code = 201
    return resp

@users_api.route('/api/users/<string:email>/', methods=['GET', 'PATCH', 'DELETE'])
def user(email):
    # Return an error if the user does not exist
    user = User.query.get(email)
    if user is None:
        resp = jsonify({"msg": "User not found."})
        resp.status_code = 404
        return resp

    # authenticate
    if 'Authorization' not in request.headers:
        resp = jsonify({"msg": "Unautheticated request"})
        resp.status_code = 403
        return resp

    parts = []
    email = ''
    password = ''
    try:
        parts = base64.b64decode(request.headers['Authorization'].split()[1].encode()).decode().split(':')

        email = parts[0]
        password = parts[1]

    except (TypeError, IndexError) as e:
        resp = jsonify({"msg": str(e)})
        resp.status_code = 403
        return resp

    if email != user.email_address or not sha256_crypt.verify(password, user.password):
        resp = jsonify({"msg": "Unautheticated request"})
        resp.status_code = 403
        return resp

    if request.method == 'GET':
        resp = jsonify(user.serialize)
        resp.status_code = 200
        return resp
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        resp = jsonify({})
        resp.status_code = 204
        return resp

    if request.method == 'PATCH':
        # Get the request data
        req = request.get_json()

        # Create a list of valid update keys
        valid = ["name", "password"]

        # Error out if any requested keys are not valid
        for key in req.keys():
            if key not in valid:
                return jsonify({"status": 400, "msg": "patch request invalid"})

        # Update valid fields
        if 'name' in req:
            if len(req["name"]) > 50 or not re.match("^[A-Za-z ]*$", req["name"]):
                resp = jsonify({"msg": "Invalid name"})
                resp.status_code = 400
                return resp
            user.name = req["name"]


        if 'password' in req:
            if not re.match("^[A-Za-z0-9!$@&]*$", req["password"]):
                resp = jsonify({"msg": "Invalid password"})
                resp.status_code = 400
                return resp
            user.password = sha256_crypt.hash(req["password"])

        # commit
        db.session.commit()

        # return the new user data
        resp = jsonify(user.serialize)
        resp.status_code = 400
        return resp

@users_api.route('/api/users/<string:email>/businesses/', methods=['GET'])
def user_businesses(email):
    user = User.query.get(email)
    if user is None:
        resp = jsonify({"msg": "User not found."})
        resp.status_code = 404
        return resp

    resp = jsonify({
            "businesses": [b.serialize for b in user.businesses]
        })
    resp.status_code = 200
    return resp
