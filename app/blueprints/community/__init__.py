from flask import Blueprint
bp = Blueprint('community', __name__)
from app.blueprints.community import routes  # noqa
