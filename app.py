import flask
from flask import *
import flask_restful
import flask_jwt_extended
import controllers
from controllers import *
import api
from api import *
import endpoint
from endpoint import *
import config

from extensions import *

# Initialize Flask and Flask_Restful apps
app = Flask(__name__)
api = flask_restful.Api(app)

# Register Flask Restful resources
api.add_resource(UserCreate, '/api/user')
api.add_resource(UserLogin, '/api/user/login')
api.add_resource(UserDML, '/api/user/<string:_email>')

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
app.config['BUNDLE_ERRORS'] = True
app.config['JWT_SECRET_KEY'] = b'\xbf\xe2r)\xa8A\xf1\xafa\xcc\xb6\x05i\xda\xf0v\x91\xc8\xd9p\xb8\xe3-\x9cs]\xb4^\x13\x8a\x8d\xdf'

# Initialize JWT
jwt = flask_jwt_extended.JWTManager(app)


db.init_app(app)

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python3 app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
