from .extensions import db
from datetime import datetime


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    data = db.Column(db.JSON)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Company {}>".format(self.name)
