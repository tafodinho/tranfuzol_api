from project.server import app, db, bcrypt
from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect

DONOR_MATCH = {
    'O-': ['O-'], 
    'O+': ['O-', 'O+'],
    'B-': ['O-', 'B-'],
    'B+': ['O-', 'O+', 'B-', 'B+'],
    'A-': ['O-', 'A-'], 
    'A+': ['O-', 'O+', 'A-', 'A+'], 
    'AB-': ['O-', 'B-', 'A-', 'AB-'], 
    'AB+': ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+']
}

class Subscriber(db.Model):

    __tablename__ = "subscribers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sn = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    transfusions = db.relationship('Transfusion', backref='subscriber', lazy=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    medical_conditions = db.Column(db.String(100))
    current_medications = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    home_address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    phone1 = db.Column(db.String(100))
    phone2 = db.Column(db.String(100))
    cni = db.Column(db.String(100))
    cni_doi = db.Column(db.DateTime())
    cni_poi = db.Column(db.String())
    dob = db.Column(db.DateTime())
    pob = db.Column(db.String(100))
    gender = db.Column(db.String(100))
    blood_group = db.Column(db.String(100))
    rhesus_factor = db.Column(db.String(100))
    allergies = db.Column(db.String(100))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self):
        self.active = True

    # def __init__(self, email, first_name, middle_name, last_name, home_address, 
    #             city, phone1, phone2, cni, cni_doi, cni_poi, dob, 
    #             pob, gender, blood_group, active=True):
    #     self.email = email
    #     self.first_name = first_name
    #     self.middle_name = middle_name
    #     self.last_name = last_name
    #     self.home_address = home_address
    #     self.city = city
    #     self.phone1 = phone1
    #     self.phone2 = phone2
    #     self.cni = cni
    #     self.cni_doi = cni_doi
    #     self.cni_poi = cni_poi
    #     self.dob = dob
    #     self.pob = pob
    #     self.gender = gender
    #     self.blood_group = blood_group
    #     self.active = active
        
    def generate_sn(self):
        self.sn = "DN"+self.first_name[0]+self.middle_name[0]+str(random.randint(10000, 99999))

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
    
    def _return_data(self):
        from project.server.models.Donor import Donor
        sub_arr = self._asdict()
        sub_arr['transfusions'] = [trans._asdict() for trans in self.transfusions]
        for j in range(len(self.transfusions)):
            sub_arr['transfusions'][j]['hospital'] = self.transfusions[j].hospital._asdict()
        match = Donor().query.filter(Donor.blood_group.in_(DONOR_MATCH[sub_arr['blood_group']])).all()
        sub_arr['match'] = [bg._asdict() for bg in match]
        sub_arr['done_at'] = self.done_at._asdict()

        return sub_arr