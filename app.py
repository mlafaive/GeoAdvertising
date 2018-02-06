from flask import *
import controllers
from controllers import main
import config

from extensions import *

# Initialize Flask app
app = Flask(__name__)

# Register the controllers
app.register_blueprint(main)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = get_db_url()

db.init_app(app) 

# Listen on external IPs
# For us, listen to port 3000 so you can just run 'python app.py' to start the server
if __name__ == '__main__':
    # listen on external IPs
    app.run(host=config.env['host'], port=config.env['port'], debug=True)
