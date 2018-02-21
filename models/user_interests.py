from extensions import db

class User_Interests(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    interest_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, user_id, interest_id):
        self.user_id = user_id
        self.interest_id = interest_id


    def __repr__(self):
        return "<user_id=%d, interest_id=%d>" % (self.user_id, self.interest_id)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'user_id': self.user_id,
           'interest_id': self.interest_id,
       }

