from extensions import db

class Users(db.Model):
    email_address = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String, nullable=False)
    last_offer_time = db.Column(db.Date, nullable=True)

    def __init__(self, name, user_type, email_address, password, last_offer_time=None):
        self.name = name
        self.user_type = user_type
        self.email_address = email_address
        self.password = password
        self.last_offer_time = last_offer_time

    def __repr__(self):
        return "<name='%s', user_type='%s', email_address='%s', phone_number='%s', dob=%r, password='%s', last_offer_time=%r>" % \
              (self.name, self.user_type, self.email_address, self.phone_number, self.dob, self.password, self.last_offer_time)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name': self.name,
           'user_type': self.user_type,
           'email_address': self.email_address,
           'last_offer_time': self.last_offer_time,
       }
