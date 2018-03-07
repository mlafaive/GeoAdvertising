from extensions import *
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import User, Business, Interest, User_Interest, Offer, City, Business_Offer, Offer_Interest
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
			
		
		# name, user_type, email_address, phone_number, dob, password, salt, last_offer_time
		user1 = User('Jack Smith', 'consumer', 'jacksmith@gmail.com', 'password1')
		user2 = User('Jane Doe', 'manager', 'janedoe@gmail.com', 'password2')

		db.session.add(user1)
		db.session.add(user2)

		cit1 = City('Ann Arbor', 'Michigan', 'EST')
		db.session.add(cit1)

		#                  name,    business_type, store_address,          city_id, email_address,    phone_number, latitude,   longitude, manager_id,  unit_number=None
		bis1 = Business('Google', 'Technology', '1600 Ampitheatre Parkway', 1, 'google@gmail.com', '12345678901', 37.421512, -122.084101, 'jacksmith@gmail.com')
		db.session.add(bis1)

		its1 = Interest('Sporting Goods')
		db.session.add(its1)

		uist1 = User_Interest(1,1)
		db.session.add(uist1)



		db.session.commit()


		off1 = Offer(bis1.id, datetime.datetime(2018,2,21, 0,0,0), datetime.datetime(2018,2,21, 23,59,59), 'Greatest Offer EVER!!! CASH CASH CASH', 'This is the description of the greatest offer og all time.')
		db.session.add(off1)

		offint1 = Offer_Interest(1,1)
		db.session.add(offint1)

		bisoff1 = Business_Offer(1,1)
		db.session.add(bisoff1)



		db.session.commit()
