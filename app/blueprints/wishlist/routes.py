from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.blueprints.wishlist import bp
from app.extensions import db
from app.models import Wishlist, Destination, Hotel

@bp.route('/')
@login_required
def index():
    items = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist/index.html', items=items, title='Wishlist — Beyond Tour')

@bp.route('/toggle', methods=['POST'])
@login_required
def toggle():
    target_type = request.form.get('target_type')
    target_id = int(request.form.get('target_id', 0))
    existing = Wishlist.query.filter_by(
        user_id=current_user.id, target_type=target_type, target_id=target_id
    ).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        if request.headers.get('HX-Request'):
            return render_template('wishlist/_button.html', saved=False, target_type=target_type, target_id=target_id)
        return jsonify({'saved': False})
    item = Wishlist(user_id=current_user.id, target_type=target_type, target_id=target_id)
    db.session.add(item)
    db.session.commit()
    if request.headers.get('HX-Request'):
        return render_template('wishlist/_button.html', saved=True, target_type=target_type, target_id=target_id)
    return jsonify({'saved': True})
