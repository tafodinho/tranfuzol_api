
from project.server import app, db, bcrypt
from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect
import random
from sqlalchemy.ext.hybrid import hybrid_method

class Deferral(db.Model):

    __tablename__ = "deferrals"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=False)
    reason = db.Column(db.String(100))
    ndefbd = db.Column(db.DateTime())
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now())

    def _asdict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}

    @hybrid_method
    def update_donor_ndefbd(self):
        if self.donor:
            print("UPDATE MASTER")
            self.donor.update_ndefbd(self.ndefbd)
