
from project.server import app, db, bcrypt

class Transfusion(db.Model):

    __tablename__ = "transfusions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=False)
    diagnosis = db.Column(db.String(100))
    hosp_unit = db.Column(db.String(100))
    medical_conditions = db.Column(db.String(100))
    hem_level = db.Column(db.String(100))
    bp_requested = db.Column(db.String(100))
    bp_received = db.Column(db.String(100))
    ubpt = db.Column(db.String(100))
    id_ut = db.Column(db.String(100))
    onset_time = db.Column(db.Time())
    termination_time = db.Column(db.Time())
    effect_of_transfusion = db.Column(db.String(100))
    date_requested = db.Column(db.String(100))
    date_delivered = db.Column(db.String(100))
    patient_end_status = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    # def __init__(self, diagnosis, hosp_unit, medical_condition, hem_level, bp_requested, 
    #             bp_received, id_ut, onset_time, eo_transfusion, tt, eot, date_requested, date_delivered, 
    #             pe_status):
        # self.email = email
        # self.first_name = first_name
        # self.middle_name = middle_name
        # self.last_name = last_name
        # self.home_address = home_address
        # self.city = city
        # self.phone1 = phone1
        # self.phone2 = phone2
        # self.cni = cni
        # self.cni_doi = cni_doi
        # self.cni_poi = cni_poi
        # self.dob = dob
        # self.pob = pob
        # self.gender = gender
        # self.blood_group = blood_group
        # self.active = active
        
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in db.inspect(self).mapper.column_attrs}
    
    def _return_data(self):
        data = self._asdict()
        data['hospital'] = self.hospital._asdict()
        data['subscriber'] = self.subscriber._asdict()

        return data