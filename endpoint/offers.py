import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from extensions import db
from models import Offer

class Offers(Resource):
	@jwt_required
	def get(self):
		# Retrieve User with _email from DB
		Offer.query.all()
		resp = { "offers": [i.serialize for i in Offer.query.all()] }
		print(resp)
		return resp