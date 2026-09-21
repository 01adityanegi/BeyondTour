from flask import Blueprint
bp = Blueprint('my_trips', __name__)
from app.blueprints.my_trips import routes  # noqa
