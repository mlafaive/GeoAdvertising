from app import db

user1 = User('John Doe')
app.db.session.add(user1)
user2 = User('Jane Smith')
app.db.session.add(user2)
db.session.commit()