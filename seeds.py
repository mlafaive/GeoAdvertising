from extensions import *
from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from models import User, Business, Interest, Offer, City
import config
import datetime
from passlib.hash import sha256_crypt
from subprocess import call
import random

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







		user_data = [('jacksmith@gmail.com', 'Jack Smith', sha256_crypt.hash('password1')), ('janedoe@gmail.com', 'Jane Doe', sha256_crypt.hash('password2')), \
					('bubbleisland@gmail.com', 'Bubble Owner', sha256_crypt.hash('bubbles_pass')), ('lawyers@umich.edu', 'Ron LaFlamme', sha256_crypt.hash('moneymoneymoney')), \
					('sarex@umich.edu', 'Sarah Example', sha256_crypt.hash('imastudent')), ('coneyowner@bing.com', 'Coney Owner', sha256_crypt.hash('coneyconey1234'))]
		users = {}
		for user_d in user_data:
			users[user_d[0]] = User(user_d[0], user_d[1], user_d[2])
			db.session.add(users[user_d[0]])
		db.session.commit()





		city_data = [('Ann Arbor', 'Michigan', 'EST', 42.281389, -83.748333), ('North Campus', 'Michigan', 'EST', 42.292126, -83.715819), \
					('Detroit', 'Michigan', 'EST', 42.331598, -83.046528)]
		cities = {}
		for city_d in city_data:
			cities[city_d[0]] = City(city_d[0], city_d[1], city_d[2], city_d[3], city_d[4])
			db.session.add(cities[city_d[0]])
		db.session.commit()
		


		
		
		interest_data = ['Sports', 'Clothing', 'Food', 'Entertainment', 'Technology', 'Home Goods', 'Transportation']
		interests = {}
		for interest_d in interest_data:
			interests[interest_d] = Interest(interest_d)
			db.session.add(interests[interest_d])
		db.session.commit()




		business_data = [("Zingerman's Delicatessen", '422 Detroit St', cities['Ann Arbor'].id, users['jacksmith@gmail.com'].email, 42.2846861, -83.7472546, ['Food']), ("University of Michigan Museum of Natural History", '1109 Geddes Ave', cities['Ann Arbor'].id, users['janedoe@gmail.com'].email, 42.278429, -83.735133, ['Entertainment']), \
						('Bubble Island', '1220 S University Ave #100', cities['Ann Arbor'].id, users['bubbleisland@gmail.com'].email, 42.274919, -83.733405, ['Food']), ('University of Michigan Law School', '625 S State St', cities['Ann Arbor'].id, users['lawyers@umich.edu'].email, 42.274317, -83.740231, ['Entertainment']), \
						('Mujo Cafe', '2281 Bonisteel Blvd', cities['North Campus'].id, users['bubbleisland@gmail.com'].email, 42.291595, -83.715970, ['Food']), ('Woodward Coney Island', '616 Woodward Ave', cities['Detroit'].id, users['coneyowner@bing.com'].email, 42.330873, -83.045599, ['Food']), \
						('Detroit Tigers', '2100 Woodward Ave', cities['Detroit'].id, users['coneyowner@bing.com'].email, 42.338888, -83.048517, ['Food', 'Entertainment', 'Sports']), ('Jimmy John\'s', '600 Packard St', cities['Ann Arbor'].id, users['jacksmith@gmail.com'].email, 42.271592, -83.741702, ['Food']), \
						('Domino\'s Pizza', '716 Packard St', cities['Ann Arbor'].id, users['jacksmith@gmail.com'].email, 42.270431, -83.740315, ['Food']), ('Michigan Ticket Office', '', cities['Ann Arbor'].id, users['lawyers@umich.edu'].email, 42.269460, -83.740768, ['Food','Sports','Entertainment'])]
		businesses = {}
		for business_d in business_data:
			businesses[business_d[0]] = (Business(business_d[0], business_d[1], business_d[2], business_d[3], business_d[4], business_d[5]), business_d[6])
			db.session.add(businesses[business_d[0]][0])
		db.session.commit()





		# Randomly generate offers for businesses
		offer_data = {'Sports': ['Free baseball tickets, first 50 to accept!!', 'Expensive student tickets in the upper bowl!! We love our students ;)', '2 free football tix with purchase of 2 coke zeros!!!!', '75% off baby boomer discount for football tickets in the quiet sections.', '100% discount on all non-revenue sports tickets!!', "Come watch spring training practice!!"]+['Random sports offer #'+str(i) for i in range(250)],
					'Food': ['$5 for 12 inches of bread, meat and lettuce! (legally we can\'t call it a foot long)', '10% off all products expiring in the next 24 hours!!!!', '100% off all dumpster finds! Must pick up before Tuesday.', '42% off all wood-pulp based products.', 'Reuben sandwhiches with 240% markup to cover the cost of our earlier deal!']+['Random food offer #'+str(i) for i in range(100)],
					'Entertainment': ['10% off tickets to loud concert! Sponsored by your local hearing doctors.', '$0.01 off for every insta follower you have.', 'Night at the museum -- Watch as everything comes to life!']+['Random entertainment offer #'+str(i) for i in range(100)],
					}
		timing_data = [(datetime.datetime(2015,2,28, 12,0,0), datetime.datetime(2016,3,28, 16,0,0)), \
						(datetime.datetime(2018,2,28, 12,0,0), datetime.datetime(2019,3,28, 16,0,0)), \
						(datetime.datetime(2019,7,20, 12,0,0), datetime.datetime(2020,3,2, 16,0,0))]
		num_offers = 100
		offers = {}
		for _ in range(num_offers):
			bus_name, bus_obj = random.choice(list(businesses.items()))
			bus_int = random.choice(bus_obj[1])
			off_desc = random.choice(offer_data[bus_int])
			time = random.choice(timing_data)
			offers[_] = Offer(bus_obj[0].id, time[0], time[1], off_desc)
			offers[_].interests.append(interests[bus_int])
			db.session.add(offers[_])
			del offer_data[bus_int][offer_data[bus_int].index(off_desc)]
		db.session.commit()



		# Randomly assign interests to users
		for email, user in users.items():
			num_user_ints = random.randint(0, len(interest_data))
			chosen=[]
			for i in range(num_user_ints):
				rand_int = random.choice(list(set(interest_data)-set(chosen)))
				user.interests.append(interests[rand_int])
				chosen.append(rand_int)
		db.session.commit()


		# Randomly assign interests to users
		for email, user in users.items():
			num_user_ints = random.randint(1, 20)
			chosen=[]
			for i in range(num_user_ints):
				rand_off = random.choice(list(set(offers.values())-set(chosen)))
				user.offers_viewed.append(rand_off)
				user.offers_accepted.append(rand_off)
				chosen.append(rand_off)
		db.session.commit()




		


