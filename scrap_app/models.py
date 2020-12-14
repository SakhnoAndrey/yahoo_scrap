from scrap_app.extensions import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    data = db.Column(db.JSON)

    def __repr__(self):
        return "<Company {}>".format(self.name)
