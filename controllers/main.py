from flask import *
import flask
import werkzeug.exceptions as ex
from extensions import connect_to_database

main = Blueprint('main', __name__)

app = flask.Flask(__name__)


@main.route('/')
def main_hello():
    db = connect_to_database()
    cur = db.cursor()

    cur.execute('SELECT id, name FROM Test')

    results = cur.fetchall()
    print(results)
    print_str = "<table>"
    for result in results:
        print_str += "<tr><td>%s</td><td>%s</td><tr>" % (result['id'], result['name'])
    print_str += "</table>"
    return print_str


