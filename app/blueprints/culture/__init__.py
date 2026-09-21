from flask import Blueprint
bp = Blueprint('culture', __name__)
from app.blueprints.culture import routes  # noqa
