from flask import Blueprint
bp = Blueprint('tourism_dashboard', __name__)
from app.blueprints.tourism_dashboard import routes  # noqa
