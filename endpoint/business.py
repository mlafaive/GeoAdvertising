import flask
from flask_restful import Resource, reqparse, HTTPException
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity)
from extensions import db
from models import Business, City
import geopy
from tzwhere import tzwhere
from sqlalchemy import exc


class BusinessCreate(Resource):
    @jwt_required
    #TODO: Error handle (dont forget when API returns with a limit error)
    #TODO: How to tell if a business is a duplicate?
    def post(self):
        # Parse the posted object
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('store_address', type=str, required=True)
        parser.add_argument('city_name', type=str, required=True)
        parser.add_argument('state_name', type=str, required=True)
        args = parser.parse_args()

        # Set manager to the token's identity, and add to args
        manager = get_jwt_identity()

        args["manager"] = manager

        # Get the geolocation of the store using its address, city, and state
        geo = geopy.geocoders.GoogleV3(api_key='AIzaSyD56wh0KThJ-ekY1WBICUzt_wEX6MtEH7c')
        location = geo.geocode('{}, {}, {}'.format(args["store_address"], args["city_name"], args["state_name"]))
        store_address = location.address.split(",")[0].strip()
        city_name = location.address.split(",")[1].strip()
        state_name = location.address.split(",")[2].split()[0].strip()

        # Get the timzone of the store using its latitude and longitude
        timezone = geo.timezone((location.latitude, location.longitude))

        # Fetch the City or create if it doesn't exist
        city = City.query.filter_by(city_name = city_name, state_name = state_name).first()
        if city is None:
            city = City(city_name = city_name, state_name = state_name, timezone = timezone.zone)
            db.session.add(city)
            db.session.flush()
            # ^ Does SA update the city here???

        # Create business
        init = {
            "name": args["name"],
            "store_address": store_address,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "manager_address": manager,
            "city_id": city.id
        }
        business = Business(**init)
        db.session.add(business)

        try:
            db.session.commit()
        except exc.IntegrityError:
            return {'error': 'business at location in same city already exists'}, 400

        return business.serialize, 201

class BusinessDML(Resource):
    @jwt_required
    def get(self, _id):
        # Ensure the business exists
        business = Business.query.get(_id)
        if business is None:
            return {'error': 'business does not exist'}, 400

        # Return with the business data
        return business.get_public_data

    @jwt_required
    def delete(self, _id):
        # Ensure the business exists
        business = Business.query.get(_id)
        if business is None:
            return {'error': 'business does not exist'}, 400

        # Ensure the user manages the business
        email = get_jwt_identity()
        if business.manager.email != email:
            flask.abort(403)

        # Delete the business
        db.session.delete(business)
        db.session.commit()

        # Return with a 204
        return '', 204

class BusinessOffers(Resource):
    @jwt_required
    def get(self, _id):
        # Ensure the business exists
        business = Business.query.get(_id)
        if business is None:
            return {'error': 'business does not exist'}, 400

        # TODO: return list of actual offer objects
        # Return list of offer ids
        return {'offers': [o.serialize for o in business.offers]}
