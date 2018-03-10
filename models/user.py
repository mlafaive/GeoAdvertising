from extensions import db
from .user_interest import user_interest
import datetime

class User(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)
    last_offer_time = db.Column(db.DateTime, nullable=True)
    businesses = db.relationship('Business', backref='manager', lazy=True)
    interests = db.relationship('Interest', secondary=user_interest, lazy='subquery', backref=db.backref('users',lazy=True))

    def __init__(self, email, name, password, businesses=[], interests=[], last_offer_time=datetime.datetime(2000,1,1, 0,0,0)):
        self.email = email
        self.name = name
        self.password = password
        self.last_offer_time = last_offer_time
        self.businesses = businesses
        self.interests = interests

    def __repr__(self):
        return "<email='%s', name='%s', password='%s', last_offer_time=%r, businesses=%r, interests=%r>" % \
              (self.email, self.name, self.password, self.last_offer_time, [b.id for b in self.businesses], [i.name for i in self.interests])

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
          'email': self.email,
          'name': self.name,
          'last_offer_time': self.last_offer_time.isoformat(),
          'businesses': [b.id for b in self.businesses],
          'interests': [i.name for i in self.interests],
       }
