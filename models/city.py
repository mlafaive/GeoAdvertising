from extensions import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(50), nullable=False)
    state_name = db.Column(db.String(50), nullable=False)
    time_zone = db.Column(db.String(10), nullable=False)
    businesses = db.relationship('Business', backref='city', lazy=True)

    def __init__(self, city_name, state_name, time_zone, businesses=[]):
        self.city_name = city_name
        self.state_name = state_name
        self.time_zone = time_zone
        self.businesses = businesses


    def __repr__(self):
        return "<city_name='%s', state_name='%s', time_zone='%s', businesses=%r>" % \
              (self.city_name, self.state_name, self.time_zone, [b.id for b in self.businesses])

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'city_name': self.city_name,
           'state_name': self.state_name,
           'time_zone': self.time_zone,
           'businesses': [b.id for b in self.businesses],
       }