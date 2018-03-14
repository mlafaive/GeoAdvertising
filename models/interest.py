from extensions import db

class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)


    __table_args__=(db.UniqueConstraint('name',name='_interest_name_uc'),)

    def __init__(self, name):
        self.name = name


    def __repr__(self):
        return "<name='%s'>" % self.name

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
       }
