import json
from pprint import pprint
import flask
from flask import *
from models import Business
from extensions import db
from passlib.hash import sha256_crypt
import base64
import re

businesses_api = Blueprint("businesses_api", __name__)

@businesses_api.route('/api/businesses/', methods=['GET', 'POST'])
def users():
    if request.method == "GET":
        resp = jsonify({
            "businesses": [i.serialize for i in Business.query.all()]
        })
        resp.status_code = 200
        return resp
    if request.method == "POST":
        try:
            # Get JSON from the request

            # TODO validate request

            req = request.get_json()

            # Create the user in the database
            return create_business(req)
        except (TypeError, ValueError) as e:
            resp = jsonify({"msg": str(e)})
            resp.status_code = 400
            return resp

def create_business(req):
    if req is None:
        resp = jsonify({"msg": "invalid request"})
        resp.status_code = 400
        return resp

    # TODO validate request

    # Add the user to SQLAlchemy
    new_business = Business(**req)
    db.session.add(new_business)
    db.session.commit()

    resp = jsonify(new_business.serialize)
    resp.status_code = 201
    return resp

@businesses_api.route('/api/businesses/<int:id>/', methods=['GET', 'DELETE'])
def business(id):
    # Return an error if the user does not exist
    business = Business.query.get(id)
    if business is None:
        resp = jsonify({"msg": "Business not found."})
        resp.status_code = 404
        return resp

    # TODO authenticate here


    if request.method == 'GET':
        resp = jsonify(business.serialize)
        resp.status_code = 200
        return resp
    if request.method == 'DELETE':
        db.session.delete(business)
        db.session.commit()

        resp = jsonify({})
        resp.status_code = 204
        return resp

@business_api.route('/api/businesses/<int:id>/offers/', methods=['GET'])
def business_offers(email):
    business = Business.query.get(id)
    if business is None:
        resp = jsonify({"msg": "User not found."})
        resp.status_code = 404
        return resp

    resp = jsonify({
            "offers": [o.serialize for o in business.offers]
        })
    resp.status_code = 200
    return resp

