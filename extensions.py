import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def get_db_url():
	return os.environ['DATABASE_URL']