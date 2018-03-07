import flask
from flask import *
import controllers
from controllers import *
import api
from api import *
import config

from extensions import *

# Initialize Flask app
app = Flask(__name__)

# Register the controllers
app.register_blueprint(main)
app.register_blueprint(users_api)
app.register_blueprint(offers_api)
app.register_blueprint(businesses_api)

@app.errorhandler(404)
def page_not_found(error=None):
	return not_found(error)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()



db.init_app(app)

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python3 app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
