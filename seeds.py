from app import db
from models import User

user1 = User('John Doe')
db.session.add(user1)
user2 = User('Jane Smith')
db.session.add(user2)
db.session.commit()