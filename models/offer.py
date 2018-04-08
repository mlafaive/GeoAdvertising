from extensions import db
from .offer_interest import offer_interest
from dateutil.tz import *

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    end_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # Direct access to corresponding offer(offer) using Business
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    interests = db.relationship('Interest', secondary=offer_interest, lazy='subquery', backref=db.backref('offers',lazy=True))

    __table_args__=(db.UniqueConstraint('description','business_id',name='_offer_description_business_uc'),)

    def __init__(self, business_id, start_time, end_time, description, interests=[]):
        self.business_id = business_id
        self.start_time = start_time
        self.end_time = end_time
        self.description = description
        self.interests = interests


    def __repr__(self):
        return "<business_id=%d, start_time=%r, end_time=%r, description='%s', interests=%r>" % \
        		(self.business_id, self.start_time, self.end_time, self.description, [i.name for i in self.interests])

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'business': {
            'id': self.business.id,
            'name': self.business.name
           },
           'start_time': self.start_time.isoformat(),
           'end_time': self.end_time.isoformat(),
           'description': self.description,
           'interests': [i.serialize for i in self.interests],
           'views': len(self.users_viewed),
           'accepts': len(self.users_accepted),
       }
