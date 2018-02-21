from extensions import *
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import Users, Businesses
import config

if __name__ == '__main__':
	DB_URL = get_db_url()
	reset_db = DB_URL == config.env['local_db_url']
	# Initialize Flask app
	app = Flask(__name__)

	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL

	with app.app_context():
		db.init_app(app)

		if reset_db:
			if database_exists(DB_URL):
			    print('Deleting database.')
			    drop_database(DB_URL)
			if not database_exists(DB_URL):
			    print('Creating database.')
			    create_database(DB_URL)
			db.create_all()
			db.session.commit()
		else:
			db.create_all()
			db.session.commit()

			User.query.delete()
			print('To reset ids run reset from heroku account')
			
		

		user1 = Users('Jack Smith')
		user2 = Users('Jane Doe')
		db.session.add(user1)
		db.session.add(user2)

		#                  name,    business_type, store_address,          city_id, email_address,    phone_number, latitude,   longitude, manager_id,  unit_number=None
		bis1 = Businesses('Google', 'Technology', '1600 Ampitheatre Parkway', 1, 'google@gmail.com', '12345678901', 37.421512, -122.084101, 1)
		db.session.add(bis1)

		db.session.commit()
