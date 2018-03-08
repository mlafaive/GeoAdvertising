from extensions import db


offer_interest = db.Table('offer_interest',
                          db.Column('offer_id', db.Integer, db.ForeignKey('offer.id'), primary_key=True),
                          db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'), primary_key=True)
                        )