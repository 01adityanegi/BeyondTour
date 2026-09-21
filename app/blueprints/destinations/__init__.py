from flask import Blueprint
bp = Blueprint('destinations', __name__)
from app.blueprints.destinations import routes  # noqa
