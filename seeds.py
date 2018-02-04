from models import User, db

db.create_all()
db.session.commit()

admin = User('admin', 'admin@example.com', 'admin1', 'admin1@example.com')
guest = User('admi2', 'admin@ex1ample.com', 'admin', 'admin2@example.com')
db.session.add(admin)
db.session.add(guest)
db.session.commit()