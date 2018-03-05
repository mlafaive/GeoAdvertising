import os
env = dict(
	host = '0.0.0.0',
	port = int(os.environ.get('PORT', 3000)),
	local_db_url = 'postgresql://localhost/geo_adv_db'
)
