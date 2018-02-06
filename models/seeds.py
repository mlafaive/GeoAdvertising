from .user import *

db.create_all()
db.session.commit()

user1 = User('Jack Smith')
user2 = User('Jane Doe')
db.session.add(user1)
db.session.add(user2)
db.session.commit()