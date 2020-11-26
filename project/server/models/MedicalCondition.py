
# from project.server.app import app, db, bcrypt
# from sqlalchemy import Column, Date, Integer, Text, create_engine, inspect
# import random

# class MedicalCondition(db.Model):

#     __tablename__ = "donors"

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     donor_id = db.Column(db.Integer, db.ForeignKey('donors.id'), nullable=True)
#     subscriber_id = db.Column(db.Integer, db.ForeignKey('subscribers.id'), nullable=True)
#     name = db.Column(db.String(100))

#     created_at = db.Column(db.DateTime, default=db.func.now())
#     updated_at = db.Column(db.DateTime, default=db.func.now())

#     def _asdict(self):
#         return {c.key: getattr(self, c.key)
#                 for c in inspect(self).mapper.column_attrs}