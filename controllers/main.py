from flask import *
import flask

import werkzeug.exceptions as ex
from extensions import connect_to_database

main = Blueprint('main', __name__)

@main.route('/')
def main_hello():
    # db = connect_to_database()
    # cur = db.cursor()

    # cur.execute('SELECT id, name FROM Test')

    # data = cur.fetchall()
    # print(data)
    # resp = jsonify(data)
    # resp.status_code = 200
    # return resp
    return 'hello world'


