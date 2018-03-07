from extensions import db

class Offer_Interests(db.Model):
    offer_id = db.Column(db.Integer, primary_key=True)
    interest_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, offer_id, interest_id):
        self.offer_id = offer_id
        self.interest_id = interest_id


    def __repr__(self):
        return "<offer_id=%d, interest_id=%d>" % \
              (self.offer_id, self.interest_id)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'offer_id': self.offer_id,
           'interest_id': self.interest_id,
       }