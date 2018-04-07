from extensions import db


user_accepted_offer = db.Table('user_accepted_offer',
                          db.Column('user_address', db.String(50), db.ForeignKey('user.email'), primary_key=True),
                          db.Column('offer_id', db.Integer, db.ForeignKey('offer.id'), primary_key=True)
                        )