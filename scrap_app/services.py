import json
from models import Company
from extensions import db


def save_company_data(name: str, data: json):
    company = Company()
    company.name = name
    company.data = data
    db.session.add(company)
    db.session.commit()
