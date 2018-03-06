import json
from pprint import pprint
import flask
from flask import *
from models import Users
from extensions import db
from passlib.hash import sha256_crypt

users_api = Blueprint("users_api", __name__)

@users_api.route('/api/users/', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        data = {
            "users": [i.serialize for i in Users.query.all()]
        }
        return flask.jsonify(data)
    if request.method == "POST":
        try:
            # Get JSON from the request
            data = flask.request.get_json()

            # Check if account exists (e-mails are unique)
            exists = db.session.query(Users.id).filter_by(email_address = data["email_address"]).scalar()
            if exists:
                raise ValueError('An account with this email already exists.')

            # Create the user in the database
            return create_user(flask.request.get_json())
        except (TypeError, ValueError) as e:
            return flask.jsonify({"status": 400, "msg": str(e)})

def create_user(data):
    if data is None:
        return flask.jsonify({"status": 400, "msg": "invalid request"})

    # Hash the password and overwrite
    data["password"] = sha256_crypt.hash(data["password"])

    # Add the user to SQLAlchemy
    new_user = Users(**data)
    db.session.add(new_user)
    db.session.commit()

    return flask.jsonify(data)

@users_api.route('/api/users/<string:email>/', methods=['GET', 'POST', 'PATCH'])
def user(email):
    if request.method == 'GET':
        data = Users.query.filter_by(email_address = email).first()
        if data is not None:
            return flask.jsonify(data)
        else:
            return flask.jsonify({
                "status": 400,
                "msg": "An account with this email does not exist."
            })
