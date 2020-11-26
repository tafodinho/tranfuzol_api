
from project.server.app import app, db, bcrypt

class Hospital(db.Model):

    __tablename__ = "hospitals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    address = db.Column(db.String(100))
    phone1 = db.Column(db.String(100))
    phone2 = db.Column(db.String(100))
    unit_blood_pile = db.Column(db.Integer)
    transfusions = db.relationship('Transfusion', backref='hospital', lazy=True)
    donations = db.relationship('Donation', backref='hospital', lazy=True)
    donors = db.relationship('Donor', backref='done_at', lazy=True)
    subscribers = db.relationship('Subscriber', backref='done_at', lazy=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in db.inspect(self).mapper.column_attrs}

    def _return_data(self):
        hosp_arr = self._asdict()
        hosp_arr['transfusions'] = [tran._asdict() for tran in self.transfusions]
        hosp_arr['donations'] = [don._asdict() for don in self.donations]
        hosp_arr['donors'] = [don._asdict() for don in self.donors]
        hosp_arr['subscribers'] = [sub._asdict() for sub in self.subscribers]
        for j in range(len(self.transfusions)):
            hosp_arr['transfusions'][j]['subscriber'] = self.transfusions[j].subscriber._asdict()
            hosp_arr['transfusions'][j]['hospital'] = self.transfusions[j].hospital._asdict()
        for j in range(len(self.donations)):
            hosp_arr['donations'][j]['donor'] = self.donations[j].donor._asdict()
            hosp_arr['donations'][j]['hospital'] = self.donations[j].hospital._asdict()
        


        return hosp_arr