import os

env = dict(
	host = '0.0.0.0',
	port = int(os.environ.get('PORT', 3000)),
	user = 'postgres', 
	password = 'password',
	db = 'geo_adv_db'
)
