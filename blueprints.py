from flask import Blueprint
from scrap_app import services

bp_rest = Blueprint("bp_rest", __name__)


@bp_rest.route("/company/<name>")
def get_company_data(name):
    return services.get_company_data(name=name)
