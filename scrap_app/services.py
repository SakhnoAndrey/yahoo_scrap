import json
from scrap_app.models import Company
from scrap_app.extensions import db
from datetime import datetime


def save_company_data(name: str, data: json):
    # company = Company()
    # company.name = name
    # company.data = data
    # db.session.add(company)
    # db.session.commit()
    company = Company.objects.filter_by(name=name).first()
    if company:
        company.data = data
        company.created = datetime.now().utcnow()
    else:
        company = Company()
        company.name = name
        company.data = data
        db.session.add(company)
    db.session.commit()


def get_company_data(name: str):
    company = Company.objects.filter_by(name=name).order_by("-created").first()
    if company:
        return company.data
    else:
        return "Data not found"
