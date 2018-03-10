from extensions import db
from .offer_interest import offer_interest

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # Direct access to corresponding offer(offer) using Business
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    interests = db.relationship('Interest', secondary=offer_interest, lazy='subquery', backref=db.backref('offers',lazy=True))

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
           'business_id': self.business_id,
           'start_time': self.start_time.isoformat(),
           'end_time': self.end_time.isoformat(),
           'description': self.description,
           'interests': [i.name for i in self.interests],
       }
