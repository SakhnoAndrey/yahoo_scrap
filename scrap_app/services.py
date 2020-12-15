import json
from scrap_app.models import Company
from scrap_app.extensions import db
from datetime import datetime


def save_company_data(name: str, data: json):
    company = Company.query.filter_by(name=name).first()
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
    company = (
        Company.query.filter_by(name=name).order_by(Company.created.desc()).first()
    )
    if company:
        return company.data
    else:
        return "Company not found"
