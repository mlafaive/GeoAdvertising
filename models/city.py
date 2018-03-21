from extensions import db

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(50), nullable=False)
    state_name = db.Column(db.String(50), nullable=False)
    timezone = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    businesses = db.relationship('Business', backref='city', lazy=True)
    

    def __init__(self, city_name, state_name, timezone, latitude, longitude, businesses=[]):
        self.city_name = city_name
        self.state_name = state_name
        self.timezone = timezone
        self.latitude = latitude
        self.longitude = longitude
        self.businesses = businesses


    def __repr__(self):
        return "<city_name='%s', state_name='%s', timezone='%s', latitude=%f, longitude=%f, businesses=%r>" % \
              (self.city_name, self.state_name, self.timezone, self.latitude, self.longitude, [b.id for b in self.businesses])

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'city_name': self.city_name,
           'state_name': self.state_name,
           'timezone': self.timezone,
           'latitude': self.latitude,
           'longitude': self.longitude,
       }