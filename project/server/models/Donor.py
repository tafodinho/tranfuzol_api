
from project.server import app, db, bcrypt
from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect
import random
import datetime
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy import event

RECEIVE_MATCH = {
    'O-': ['O-', 'O+', 'B-', 'B+', 'A-', 'A+', 'AB-', 'AB+'], 
    'O+': ['O+', 'B+', 'A+', 'AB+'],
    'B-': ['B-', 'B+', 'AB-', 'AB+'],
    'B+': ['B+','AB+'],
    'A-': ['B+', 'AB+'], 
    'A+': ['A+', 'AB+'], 
    'AB-': ['AB-', 'AB+'], 
    'AB+': ['AB+']
}

class Donor(db.Model):

    __tablename__ = "donors"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sn = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    donations = db.relationship('Donation', backref='donor', lazy=False)
    deferrals = db.relationship('Deferral', backref='donor', lazy=False)
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
    allergies = db.Column(db.String(100))
    rhesus_factor = db.Column(db.String(100))
    dolbd = db.Column(db.DateTime())
    ndefbd = db.Column(db.DateTime())
    status = db.Column(db.String(100))

    referrer_id = db.Column(db.Integer, db.ForeignKey('donors.id'))
    referrees = db.relationship('Donor', backref=(db.backref('referrer', remote_side=[id])))
    active = db.Column(db.Boolean(), default=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self):
        """intitialization here"""
        
    def generate_sn(self):
        self.sn = "DN"+self.first_name[0]+self.middle_name[0]+str(random.randint(10000, 99999))
    
    def update_active(self):
        self.active = True if (self.ndefbd - datetime.datetime.now()).days <= 0 else False

    def update_status(self):
        if self.referrees and self.donations:
            if len(self.referrees) < 2 and len(self.donations) < 2: 
                self.status = "Bronze"
            elif len(self.referrees) < 6  and len(self.donations) < 3:
                self.status = "Silver"
            elif len(self.referrees) >= 6  and len(self.donations) >= 3:
                self.status = "Gold"
        else:
            self.status = "Bronze"
        
        db.session.add(self)
        db.session.commit()
    
    def update_dolbd(self, value):
        self.dolbd = value
        self.update_ndefbd()
        self.update_status()

        db.session.add(self)
        db.session.commit()

    def update_ndefbd(self, ndefbd_t=""):
        if  ndefbd_t == "":
            self.ndefbd = self.dolbd + datetime.timedelta(days=90)
            self.update_active()
        else: 
            self.ndefbd = ndefbd_t
            self.update_active()
        
        db.session.add(self)
        db.session.commit()

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}
    
    def _return_data(self):
        from project.server.models.Subscriber import Subscriber
        donor_data = self._asdict()
        print("TESTING", donor_data)
        donor_data['donations'] = [don._asdict() for don in self.donations]
        for j in range(len(self.donations)):
            donor_data['donations'][j]['hospital'] = self.donations[j].hospital._asdict()
        match = Subscriber().query.filter(Subscriber.blood_group.in_(RECEIVE_MATCH[donor_data['blood_group']])).all()
        donor_data['match'] = [bg._asdict() for bg in match]
        donor_data['referrer'] = self.referrer._asdict() if self.referrer else None
        donor_data['deferrals'] = [deferral._asdict() for deferral in self.deferrals]
        donor_data['referrees'] = [ref._asdict() for ref in self.referrees]
        donor_data['done_at'] = self.done_at._asdict()

        return donor_data
    


