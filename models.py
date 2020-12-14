from scrap_app import scrap_app
from extensions import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    data = db.Column(db.JSON)
