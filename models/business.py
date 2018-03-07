from extensions import db

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    store_address = db.Column(db.String(50), nullable=False)
    unit_number = db.Column(db.String(10), nullable=True)
    city_id = db.Column(db.Integer, nullable=False)
    email_address = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    manager_address = db.Column(db.String(50), db.ForeignKey('user.email_address'), nullable=False)

    def __init__(self, name, business_type, store_address, city_id, email_address, phone_number, latitude, longitude, manager_address,  unit_number=None):
        self.name = name
        self.business_type = business_type
        self.store_address = store_address
        self.city_id = city_id
        self.email_address = email_address
        self.phone_number = phone_number
        self.latitude = latitude
        self.longitude = longitude
        self.manager_address = manager_address
        self.unit_number = unit_number


    def __repr__(self):
        return "<name='%s', business_type='%s', store_address='%s', unit_number='%s', city_id=%d, email_address='%s', phone_number='%s', manager_address=%d, latitude=%f, longitude=%f>" \
                % (self.name, self.business_type, self.store_address, self.unit_number, self.city_id, self.email_address, self.phone_number, self.manager_address, self.latitude, self.longitude)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'name': self.name,
           'business_type': self.business_type,
           'store_address': self.store_address,
           'unit_number': self.unit_number,
           'city_id': self.city_id,
           'email_address': self.email_address,
           'phone_number': self.phone_number,
           'manager_address': self.manager_address,
           'latitude': self.latitude,
           'longitude': self.longitude
       }

