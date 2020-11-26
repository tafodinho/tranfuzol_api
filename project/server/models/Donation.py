
from project.server import app, db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_method

class Donation(db.Model):

    __tablename__ = "donations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)

    volume_of_blood = db.Column(db.Integer)
    onset_time = db.Column(db.DateTime())
    termination_time = db.Column(db.DateTime())
    torfru = db.Column(db.DateTime())

    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

        
    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in db.inspect(self).mapper.column_attrs}
    
    @hybrid_method
    def update_donor_dolbd(self):
        if self.donor:
            self.donor.update_dolbd(self.created_at)
    


    
