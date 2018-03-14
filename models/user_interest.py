from extensions import db


user_interest = db.Table('user_interest',
                          db.Column('user_address', db.String(50), db.ForeignKey('user.email'), primary_key=True),
                          db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'), primary_key=True)
                        )