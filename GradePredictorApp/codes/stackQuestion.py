db = SQLAlchemy()

class Sites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    site_code = db.Column(db.String(10))
    site_type = db.Column(db.String(100))
    datas = db.relationship("Data", uselist=False, back_populates="sites_codes")

    def __init__(self, name, site_code, site_type):
        self.name = name
        self.site_code = site_code
        self.site_type = site_type

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_code = db.Column(db.Integer, db.ForeignKey('sites.site_code'))
    time = db.Column(db.String(100))
    site_type = db.Column(db.String(100))
    site_codes = db.relationship("Sites", back_populates="datas")


    def __init__(self, site_code, site_type, temperature, name):
        self.name = name
        self.site_code = site_code
        self.site_type = site_type
        self.temperature = temperature
