from flask import render_template, current_app, make_response
from app.blueprints.main import bp
from app.models import Destination, CultureEntry, FoodItem, Hotel


@bp.route('/')
def index():
    featured_destinations = Destination.query.filter_by(featured=True).limit(6).all()
    recent_festivals = CultureEntry.query.filter_by(entry_type='festival').limit(4).all()
    featured_foods = FoodItem.query.limit(6).all()
    featured_hotels = Hotel.query.filter_by(featured=True).limit(3).all()
    return render_template(
        'main/index.html',
        destinations=featured_destinations,
        festivals=recent_festivals,
        foods=featured_foods,
        hotels=featured_hotels,
        title='Beyond Tour — Go Beyond the Guidebook'
    )


@bp.route('/about')
def about():
    return render_template('main/about.html', title='About — Beyond Tour')


@bp.route('/offline')
def offline():
    return render_template('offline.html', title='Offline Mode — Beyond Tour')


@bp.route('/trip-planner')
@bp.route('/trip-planner/')
@bp.route('/trip_planner')
@bp.route('/trip_planner/')
@bp.route('/trip_planner/<path:subpath>')
@bp.route('/trip-planner/<path:subpath>')
def trip_planner_alias(subpath=None):
    from flask import redirect, url_for, request
    qs = f"?{request.query_string.decode('utf-8')}" if request.query_string else ""
    if subpath:
        return redirect(f"/plan/{subpath}{qs}")
    return redirect(f"/plan/{qs}")


@bp.route('/sw.js')
def service_worker():
    response = make_response(current_app.send_static_file('sw.js'))
    response.headers['Content-Type'] = 'application/javascript'
    response.headers['Service-Worker-Allowed'] = '/'
    return response
