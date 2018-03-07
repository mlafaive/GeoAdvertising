from extensions import db

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    store_address = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    # Direct access to corresponding manager(user) using Business.manager
    manager_address = db.Column(db.String(50), db.ForeignKey('user.email_address'), nullable=False)

    # Direct access to corresponding city(city) using Business.city
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)


    offers = db.relationship('Offer', backref='business', lazy=True)

    def __init__(self, name, store_address, city_id, manager_address, latitude, longitude, offers=[]):
        self.name = name
        self.store_address = store_address
        self.city_id = city_id
        self.manager_address = manager_address
        self.latitude = latitude
        self.longitude = longitude
        self.offers = offers

        


    def __repr__(self):
        return "<name='%s', store_address='%s', city_id=%d, manager_address='%s', latitude=%f, longitude=%f, offers=%r>" \
                % (self.name, self.store_address, self.city_id, self.manager_address, self.latitude, self.longitude, [o.id for o in self.offers])

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'store_address': self.store_address,
           'city_id': self.city_id,
           'manager': self.manager.serialize,
           'latitude': self.latitude,
           'longitude': self.longitude,
           'offers': [o.id for o in self.offers]
       }

