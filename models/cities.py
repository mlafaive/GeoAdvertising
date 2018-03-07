from extensions import db

class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city_name = db.Column(db.String(50), nullable=False)
    state_name = db.Column(db.String(50), nullable=False)
    time_zone = db.Column(db.String(10), nullable=False)

    def __init__(self, city_name, state_name, time_zone):
        self.city_name = city_name
        self.state_name = state_name
        self.time_zone = time_zone


    def __repr__(self):
        return "<city_name='%s', state_name='%s', time_zone='%s'>" % \
              (self.city_name, self.state_name, self.time_zone)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'id': self.id,
           'city_name': self.city_name,
           'state_name': self.state_name,
           'time_zone': self.time_zone,
       }