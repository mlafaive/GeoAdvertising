from models import User
from extensions import db

db.drop_all()

db.create_all()

user1 = User('Jack Smith')
user2 = User('Jane Doe')
db.session.add(user1)
db.session.add(user2)
db.session.commit()