from flask import *
import flask
from models import Users, Businesses, Interests, User_Interests, Offers

import werkzeug.exceptions as ex


main = Blueprint('main', __name__)

@main.route('/')
def main_hello():
    all_users = [i.serialize for i in Users.query.all()]
    all_businesses = [i.serialize for i in Businesses.query.all()]
    all_interests = [i.serialize for i in Interests.query.all()]
    all_user_interests = [i.serialize for i in User_Interests.query.all()]
    all_offers = [i.serialize for i in Offers.query.all()]

    resp = jsonify(all_users+all_businesses+all_interests+all_user_interests+all_offers)
    resp.status_code = 200

    return resp


