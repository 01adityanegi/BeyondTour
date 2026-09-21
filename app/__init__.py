from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate, csrf, limiter


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.login_message = 'Please log in to access this page.'

    # Custom Jinja2 filters
    import json as _json
    @app.template_filter('from_json')
    def from_json_filter(value):
        if not value:
            return []
        if isinstance(value, (list, dict)):
            return value
        if isinstance(value, str):
            val_strip = value.strip()
            if (val_strip.startswith('[') and val_strip.endswith(']')) or \
               (val_strip.startswith('{') and val_strip.endswith('}')):
                try:
                    return _json.loads(val_strip)
                except Exception:
                    pass
            # Comma-separated fallback
            if ',' in val_strip:
                return [x.strip() for x in val_strip.split(',') if x.strip()]
            return [val_strip] if val_strip else []
        return []

    @app.template_filter('clean_label')
    def clean_label_filter(value):
        if not value:
            return ''
        return str(value).replace('-', ' ').replace('_', ' ').title()


    @app.template_filter('format_number')
    def format_number_filter(value):
        try:
            return '{:,.0f}'.format(float(value))
        except Exception:
            return str(value)

    # Register blueprints
    from app.blueprints.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.blueprints.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.blueprints.culture import bp as culture_bp
    app.register_blueprint(culture_bp, url_prefix='/culture')

    from app.blueprints.destinations import bp as destinations_bp
    app.register_blueprint(destinations_bp, url_prefix='/destinations')

    from app.blueprints.hotels import bp as hotels_bp
    app.register_blueprint(hotels_bp, url_prefix='/hotels')

    from app.blueprints.guides import bp as guides_bp
    app.register_blueprint(guides_bp, url_prefix='/guides')

    from app.blueprints.community import bp as community_bp
    app.register_blueprint(community_bp, url_prefix='/community')

    from app.blueprints.trip_planner import bp as planner_bp
    app.register_blueprint(planner_bp, url_prefix='/plan')

    from app.blueprints.wishlist import bp as wishlist_bp
    app.register_blueprint(wishlist_bp, url_prefix='/wishlist')

    from app.blueprints.my_trips import bp as trips_bp
    app.register_blueprint(trips_bp, url_prefix='/my-trips')

    from app.blueprints.reviews import bp as reviews_bp
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    from app.blueprints.tourism_dashboard import bp as tourism_bp
    app.register_blueprint(tourism_bp, url_prefix='/dashboard/tourism')

    from app.blueprints.business_dashboard import bp as business_bp
    app.register_blueprint(business_bp, url_prefix='/dashboard/business')

    from app.blueprints.admin import bp as admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.blueprints.safety import bp as safety_bp
    app.register_blueprint(safety_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        from flask import render_template
        return render_template('errors/404.html', title='Page Not Found (404) — Beyond Tour'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        from flask import render_template
        return render_template('errors/500.html', title='Server Error (500) — Beyond Tour'), 500

    # Create tables (dev convenience)
    with app.app_context():
        db.create_all()
        _seed_new_tables()

    return app


def _seed_new_tables():
    """One-time seeding of new intelligence tables if they're empty."""
    try:
        from app.models import DestinationBaseline, Destination
        if DestinationBaseline.query.count() == 0:
            _seed_baselines()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f'Baseline seeding skipped: {e}')

    try:
        from app.models import PriceBand
        if PriceBand.query.count() == 0:
            from app.services.price_bands import compute_price_bands
            compute_price_bands()
    except Exception as e:
        import logging
        logging.getLogger(__name__).warning(f'Price band seeding skipped: {e}')


def _seed_baselines():
    """Seed crowd baselines with Uttarakhand seasonality data."""
    from app.extensions import db
    from app.models import DestinationBaseline, Destination

    # Tier guide: 1=very quiet, 2=quiet, 3=moderate, 4=busy, 5=very crowded
    # Pattern: peak season Sep-Nov + Mar-May weekends are tier 4-5
    #          monsoon Jun-Aug = tier 2-3; winter Dec-Feb = tier 1-2
    def tier(month, is_weekend):
        if month in (3, 4, 5):    # Spring bloom
            return 4 if is_weekend else 3
        elif month in (6, 7, 8):  # Monsoon
            return 3 if is_weekend else 2
        elif month in (9, 10, 11):  # Peak Himalayan season
            return 5 if is_weekend else 4
        elif month in (12, 1, 2):  # Winter
            return 2 if is_weekend else 1
        return 3

    destinations = Destination.query.all()
    rows = []
    for dest in destinations:
        for month in range(1, 13):
            for day_type, is_wknd in [('weekday', False), ('weekend', True)]:
                rows.append(DestinationBaseline(
                    destination_id=dest.id,
                    month=month,
                    day_type=day_type,
                    expected_tier=tier(month, is_wknd)
                ))
    db.session.bulk_save_objects(rows)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
