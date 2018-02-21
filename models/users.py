from extensions import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    email_address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    salt = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    last_offer_time = db.Column(db.Date, nullable=True)

    def __init__(self, name, user_type, email_address, phone_number, password, salt, dob=None, last_offer_time=None):
        self.name = name
        self.user_type = user_type
        self.email_address = email_address
        self.phone_number = phone_number
        self.dob = dob
        self.password = password
        self.salt = salt
        self.last_offer_time = last_offer_time

    def __repr__(self):
        return "<name='%s', user_type='%s', email_address='%s', phone_number='%s', dob=%r, password='%s', salt='%s', last_offer_time=%r>" % \
              (self.name, self.user_type, self.email_address, self.phone_number, self.dob, self.password, self.salt, self.last_offer_time)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'user_type': self.user_type,
           'email_address': self.email_address,
           'phone_number': self.phone_number,
           'dob': self.dob,
           'password': self.password,
           'salt': self.salt,
           'last_offer_time': self.last_offer_time,
       }