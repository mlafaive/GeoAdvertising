import os
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()

def get_db_url():
	return os.environ.get('DATABASE_URL', config.env['local_db_url'])