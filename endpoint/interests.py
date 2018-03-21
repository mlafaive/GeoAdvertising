import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from extensions import db
from models import Interest

class AllInterests(Resource):
	@jwt_required
	def get(self):
		# Retrieve interests
		resp = { "interests": [i.serialize for i in Interest.query.all()] }
		return resp
