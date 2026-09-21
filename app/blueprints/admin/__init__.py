from flask import Blueprint, abort, redirect, url_for, request
from flask_login import current_user

bp = Blueprint('admin', __name__)


@bp.before_request
def require_admin():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login', next=request.url))
    if current_user.role not in ('admin', 'tourism_board'):
        abort(403)


from app.blueprints.admin import routes
