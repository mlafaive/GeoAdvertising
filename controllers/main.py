from flask import *
import flask
from models import User, Business, Interest, Offer, City

import werkzeug.exceptions as ex


main = Blueprint('main', __name__)

@main.route('/')
def main_hello():
    all_users = [i.serialize for i in User.query.all()]
    all_businesses = [i.serialize for i in Business.query.all()]
    all_interests = [i.serialize for i in Interest.query.all()]
    all_offers = [i.serialize for i in Offer.query.all()]
    all_cities = [i.serialize for i in City.query.all()]

    resp = jsonify(all_users+all_businesses+all_interests+all_offers+all_cities)
    resp.status_code = 200

    return resp
