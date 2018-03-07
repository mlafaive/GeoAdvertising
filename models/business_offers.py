from extensions import db

class Business_Offer(db.Model):
    business_id = db.Column(db.Integer, primary_key=True)
    offer_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, business_id, offer_id):
        self.business_id = business_id
        self.offer_id = offer_id


    def __repr__(self):
        return "<business_id=%d, offer_id=%d>" % \
              (self.business_id, self.offer_id)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'business_id': self.business_id,
           'offer_id': self.offer_id,
       }