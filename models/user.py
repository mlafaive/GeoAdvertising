from extensions import db
import datetime

class User(db.Model):
    email_address = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)
    last_offer_time = db.Column(db.DateTime, nullable=True)
    businesses = db.relationship('Business', backref='user', lazy=True)

    def __init__(self, email_address, name, password, businesses=[], last_offer_time=datetime.datetime(2000,1,1, 0,0,0)):
        self.email_address = email_address
        self.name = name
        self.password = password
        self.last_offer_time = last_offer_time
        self.businesses = businesses

    def __repr__(self):
        return "<email_address='%s', name='%s', password='%s', last_offer_time=%r, businesses=%r>" % \
              (self.email_address, self.name, self.password, self.last_offer_time, [b.id for b in self.businesses])

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
          'email_address': self.email_address,
          'name': self.name,
          'password': self.password,
          'last_offer_time': self.last_offer_time,
          'businesses': [b.id for b in self.businesses],
       }
