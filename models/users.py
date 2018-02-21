from extensions import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    email_address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(50), nullable=False)
    last_offer_time = db.Column(db.Date, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<name='%s', user_type='%s', email_address='%s'>" % self.name

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
       }