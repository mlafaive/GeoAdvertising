from flask import *
import flask
from models import Users, Businesses, Interests

import werkzeug.exceptions as ex


main = Blueprint('main', __name__)

@main.route('/')
def main_hello():
    all_users = Users.query.all()
    all_businesses = Businesses.query.all()
    all_interests = Interests.query.all()
    resp = jsonify([i.serialize for i in all_users]+[j.serialize for j in all_businesses]+[k.serialize for k in all_interests])
    resp.status_code = 200

    return resp


