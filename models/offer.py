from extensions import db

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)

    # Direct access to corresponding offer(offer) using Business
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)

    def __init__(self, business_id, start_time, end_time, title, description):
        self.business_id = business_id
        self.start_time = start_time
        self.end_time = end_time
        self.title = title
        self.description = description


    def __repr__(self):
        return "<business_id=%d, start_time=%r, end_time=%r, title='%s', description='%s'>" % \
        		(self.business_id, self.start_time, self.end_time, self.title, self.description)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'business_id': self.business_id,
           'start_time': self.start_time,
           'end_time': self.end_time,
           'title': self.title,
           'description': self.description,
       }

