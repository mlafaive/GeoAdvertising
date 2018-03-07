from flask import *
import flask
from models import User, Business, Interest, User_Interest, Offer, City, Offer_Interest

import werkzeug.exceptions as ex


main = Blueprint('main', __name__)

@main.route('/')
def main_hello():
    all_users = [i.serialize for i in User.query.all()]
    all_businesses = [i.serialize for i in Business.query.all()]
    all_interests = [i.serialize for i in Interest.query.all()]
    all_user_interests = [i.serialize for i in User_Interest.query.all()]
    all_offers = [i.serialize for i in Offer.query.all()]
    all_cities = [i.serialize for i in City.query.all()]
    all_offints = [i.serialize for i in Offer_Interest.query.all()]

    resp = jsonify(all_users+all_businesses+all_interests+all_user_interests+all_offers+all_cities+all_offints)
    resp.status_code = 200

    return resp
