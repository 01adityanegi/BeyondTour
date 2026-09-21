from flask import Blueprint
bp = Blueprint('hotels', __name__)
from app.blueprints.hotels import routes  # noqa
