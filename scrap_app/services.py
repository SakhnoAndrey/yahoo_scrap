def load_last_file_as_json(filename) -> list[dict]:
    pass


def save_company_data(name: str, data: list[dict]):
    company = Company()
    company.name = ...
    company.data = data
    db.session.add(company)
    db.session.commit()
