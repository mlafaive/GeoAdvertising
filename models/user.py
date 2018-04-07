from extensions import db
from .user_interest import user_interest
from .user_accepted_offer import user_accepted_offer
from .user_viewed_offer import user_viewed_offer
import datetime

class User(db.Model):
    email = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String, nullable=False)
    last_offer_time = db.Column(db.TIMESTAMP(timezone=True), nullable=True)
    businesses = db.relationship('Business', backref='manager', lazy=True, cascade='all, delete-orphan')
    interests = db.relationship('Interest', secondary=user_interest, lazy='subquery', backref=db.backref('users',lazy=True))
    offers_viewed = db.relationship('Offer', secondary=user_viewed_offer, lazy='subquery', backref=db.backref('users_viewed',lazy=True))
    offers_accepted = db.relationship('Offer', secondary=user_accepted_offer, lazy='subquery', backref=db.backref('users_accepted',lazy=True))

    def __init__(self, email, name, password, businesses=[], interests=[], offers_accepted=[], offers_viewed=[], last_offer_time=datetime.datetime.now(datetime.timezone.utc)):
        self.email = email
        self.name = name
        self.password = password
        self.last_offer_time = last_offer_time
        self.businesses = businesses
        self.interests = interests
        self.offers_accepted = offers_accepted
        self.offers_viewed = offers_viewed

    def __repr__(self):
        return "<email='%s', name='%s', password='%s', last_offer_time=%r, businesses=%r, interests=%r, offers_accepted=%r, offers_viewed=%r>" % \
              (self.email, self.name, self.password, self.last_offer_time, [b.id for b in self.businesses], [i.name for i in self.interests], [o.name for o in self.offers_accepted], [o.name for o in self.offers_viewed])

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
          'email': self.email,
          'name': self.name,
          'last_offer_time': self.last_offer_time.isoformat(),
          'interests': [i.serialize for i in self.interests],
          'offers_accepted': [o.serialize for o in self.offers_accepted],
          'offers_viewed': [o.serialize for o in self.offers_viewed],
       }
