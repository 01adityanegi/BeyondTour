from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.blueprints.my_trips import bp
from app.models import Trip

@bp.route('/')
@login_required
def index():
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    return render_template('my_trips/index.html', trips=trips, title='My Trips — Beyond Tour')

@bp.route('/<int:trip_id>')
@login_required
def detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('my_trips.index'))
    return render_template('my_trips/detail.html', trip=trip, title=f'{trip.title} — Beyond Tour')
