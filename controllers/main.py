from flask import *
import flask
from models import User

import werkzeug.exceptions as ex

main = Blueprint('main', __name__)

@main.route('/')
def main_hello():
    all_users = User.query.all()
    resp = jsonify(data)
    resp.status_code = 200
    return resp


