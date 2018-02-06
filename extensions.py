import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db_url():
	print(os.environ['DATABASE_URL'])
	return os.environ['DATABASE_URL']