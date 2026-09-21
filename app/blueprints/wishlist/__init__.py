from flask import Blueprint
bp = Blueprint('wishlist', __name__)
from app.blueprints.wishlist import routes  # noqa
