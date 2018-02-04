import os

env = dict(
	host = '0.0.0.0',
	port = int(os.environ.get('PORT', 3000)),
)
