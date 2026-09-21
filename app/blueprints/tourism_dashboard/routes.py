from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from app.blueprints.tourism_dashboard import bp
from app.models import Destination, Review, Trip, Hotel, CommunityPost
from app.extensions import db
from sqlalchemy import func


@bp.route('/')
@login_required
def index():
    if current_user.role not in ['admin', 'tourism_board']:
        flash('Access restricted to verified tourism board administrators.', 'warning')
        return redirect(url_for('main.index'))

    # Analytics data for charts
    total_destinations = Destination.query.count()
    total_reviews = Review.query.count()
    total_trips = Trip.query.count()
    total_hotels = Hotel.query.count()

    # Most visited destinations (by wishlist count — proxy)
    top_destinations = Destination.query.order_by(Destination.name).limit(8).all()

    # Region distribution
    kumaon_count = Destination.query.filter_by(region='kumaon').count()
    garhwal_count = Destination.query.filter_by(region='garhwal').count()

    # Recent reviews
    recent_reviews = Review.query.order_by(Review.created_at.desc()).limit(5).all()

    return render_template(
        'tourism_dashboard/index.html',
        title='Tourism Dashboard — Beyond Tour',
        total_destinations=total_destinations,
        total_reviews=total_reviews,
        total_trips=total_trips,
        total_hotels=total_hotels,
        top_destinations=top_destinations,
        kumaon_count=kumaon_count,
        garhwal_count=garhwal_count,
        recent_reviews=recent_reviews
    )
