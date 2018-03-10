from extensions import *
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import User, Business, Interest, Offer, City
import config
import datetime

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


		# name, user_type, email, phone_number, dob, password, salt, last_offer_time
		user1 = User('jacksmith@gmail.com', 'Jack Smith', 'password1')
		user2 = User('janedoe@gmail.com', 'Jane Doe', 'password2')

		db.session.add(user1)
		db.session.add(user2)

		cit1 = City('Ann Arbor', 'Michigan', 'EST')
		db.session.add(cit1)

		#                  name,    business_type, store_address,          city_id, email,    phone_number, latitude,   longitude, manager_id,  unit_number=None
		bis1 = Business('Google', '1600 Ampitheatre Parkway', 1, 'jacksmith@gmail.com', 37.421512, -122.084101)
		db.session.add(bis1)

		its1 = Interest('Sporting Goods')
		db.session.add(its1)
		user1.interests.append(its1)



		db.session.commit()


		off1 = Offer(bis1.id, datetime.datetime(2018,2,21, 0,0,0), datetime.datetime(2018,2,21, 23,59,59), 'This is the description of the greatest offer og all time.')
		db.session.add(off1)

		off1.interests.append(its1)




		db.session.commit()
