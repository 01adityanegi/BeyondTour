from flask import Blueprint
bp = Blueprint('guides', __name__)
from app.blueprints.guides import routes  # noqa
