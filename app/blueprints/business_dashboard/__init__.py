from flask import Blueprint
bp = Blueprint('business_dashboard', __name__)
from app.blueprints.business_dashboard import routes  # noqa
