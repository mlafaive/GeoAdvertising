from extensions import *
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import User, Business, Interest, Offer, City
import config
import datetime
from passlib.hash import sha256_crypt
from subprocess import call

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


		# name, user_type, email, phone_number, dob, password, salt, last_offer_time
		user1 = User('jacksmith@gmail.com', 'Jack Smith', sha256_crypt.hash('password1'))
		user2 = User('janedoe@gmail.com', 'Jane Doe', sha256_crypt.hash('password2'))
		user3 = User('bubbleisland@gmail.com', 'Bubble Owner', sha256_crypt.hash('bubbles_pass'))
		user4 = User('lawyers@umich.edu', 'Ron LaFlamme', sha256_crypt.hash('moneymoneymoney'))
		user5 = User('sarex@umich.edu', 'Sarah Example', sha256_crypt.hash('imastudent'))
		user6 = User('coneyowner@bing.com', 'Coney Owner', sha256_crypt.hash('coneyconey1234'))

		db.session.add(user1)
		db.session.add(user2)
		db.session.add(user3)
		db.session.add(user4)
		db.session.add(user5)
		db.session.add(user6)

		db.session.commit()


		cit1 = City('Ann Arbor', 'Michigan', 'EST', 42.281389, -83.748333)
		cit2 = City('North Campus', 'Michigan', 'EST', 42.292126, -83.715819)
		cit3 = City('Detroit', 'Michigan', 'EST', 42.331598, -83.046528)

		db.session.add(cit1)
		db.session.add(cit2)
		db.session.add(cit3)

		db.session.commit()
		

		#                  name,    business_type, store_address,          city_id, email,    phone_number, latitude,   longitude, manager_id,  unit_number=None
		bis1 = Business("Zingerman's Delicatessen", '422 Detroit St', cit1.id, user1.email, 42.2846861, -83.7472546)
		bis2 = Business("University of Michigan Museum of Natural History", '1109 Geddes Ave', cit1.id, user2.email, 42.278429, -83.735133)
		bis3 = Business('Bubble Island', '1220 S University Ave #100', cit1.id, user3.email, 42.274919, -83.733405)
		bis4 = Business('University of Michigan Law School', '625 S State St', cit1.id, user4.email, 42.274317, -83.740231)
		bis5 = Business('Mujo Cafe', '2281 Bonisteel Blvd', cit2.id, user3.email, 42.291595, -83.715970)
		bis6 = Business('Woodward Coney Island', '616 Woodward Ave', cit3.id, user6.email, 42.330873, -83.045599)
		bis7 = Business('Detroit Tigers', '2100 Woodward Ave', cit3.id, user6.email, 42.338888, -83.048517)

		db.session.add(bis1)
		db.session.add(bis2)
		db.session.add(bis3)
		db.session.add(bis4)
		db.session.add(bis5)
		db.session.add(bis6)
		db.session.add(bis7)

		db.session.commit()

		
		


		its1 = Interest('Sports')
		db.session.add(its1)

		its2 = Interest('Clothing')
		db.session.add(its2)

		its3 = Interest('Food')
		db.session.add(its3)

		its4 = Interest('Entertainment')
		db.session.add(its4)

		its5 = Interest('Technology')
		db.session.add(its5)

		its6 = Interest('Home Goods')
		db.session.add(its6)

		its7 = Interest('Transportation')
		db.session.add(its7)

		user1.interests.append(its3)
		user1.interests.append(its4)

		user5.interests.append(its3)
		user5.interests.append(its4)
		user5.interests.append(its1)

		user6.interests.append(its1)
		user6.interests.append(its3)
		user6.interests.append(its4)



		db.session.commit()


		off1 = Offer(bis1.id, datetime.datetime(2016,3,28, 12,0,0), datetime.datetime(2019,3,28, 16,0,0), 'Free reuben sandwhiches until 4:00pm EST!!!')
		off2 = Offer(bis1.id, datetime.datetime(2016,3,28, 16,0,0), datetime.datetime(2019,3,28, 23,59,59), 'Reuben sandwhiches with 240% markup to cover the cost of our earlier deal!')
		off3 = Offer(bis2.id, datetime.datetime(2016,3,28, 20,0,0), datetime.datetime(2019,3,29, 5,0,0), 'Night at the museum -- Watch as everything comes to life!')
		off4 = Offer(bis3.id, datetime.datetime(2016,3,28, 1,0,0), datetime.datetime(2019,3,29, 23,59,59), '2 for the price of 1 discount on green flavored bubbles :)')
		off5 = Offer(bis4.id, datetime.datetime(2016,3,28, 12,0,0), datetime.datetime(2019,3,29, 16,30,0), "Free legal advice . . . JK it'll cost you")
		off6 = Offer(bis7.id, datetime.datetime(2016,3,28, 0,0,0), datetime.datetime(2019,3,29, 23,59,59), "Come watch spring training practice!!")


		off1.interests.append(its3)
		off2.interests.append(its3)
		off3.interests.append(its4)
		off4.interests.append(its3)
		off5.interests.append(its5)
		off6.interests.append(its1)
		off6.interests.append(its4)

		db.session.add(off1)
		db.session.add(off2)
		db.session.add(off3)
		db.session.add(off4)
		db.session.add(off5)
		db.session.add(off6)

		




		db.session.commit()
