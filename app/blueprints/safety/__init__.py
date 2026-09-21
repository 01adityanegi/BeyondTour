from flask import Blueprint
bp = Blueprint('safety', __name__, url_prefix='/safety')
from app.blueprints.safety import routes  # noqa: F401, E402
