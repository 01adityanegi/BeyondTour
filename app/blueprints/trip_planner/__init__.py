from flask import Blueprint
bp = Blueprint('trip_planner', __name__)
from app.blueprints.trip_planner import routes  # noqa
