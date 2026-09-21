from flask import render_template, request, jsonify, abort, redirect, url_for
from app.blueprints.destinations import bp
from app.models import Destination, Hotel, CultureEntry, FoodItem, Review, Guide
from app.services.weather import get_weather
from app.services.crowd import compute_crowd_score
from app.services.best_time import compute_best_time

from app.extensions import db
from app.district_cards import get_district_search_terms

DISTRICTS_DATA = {
    'almora': {
        'slug': 'almora',
        'name': 'Almora',
        'region': 'Kumaon',
        'tagline': 'The Cultural Heart of Kumaon, Ancient Temple Clusters & Geomagnetic Energy Ridge',
        'overview': 'Perched on a horse-saddle shaped ridge between the Kosi and Suyal rivers, Almora has been the intellectual and cultural capital of Kumaon since the Chand dynasty. Famed for its ancient sanctuaries including Jageshwar Dham, Kasar Devi, Chitai Golu Devta, Nanda Devi, Vriddha Jageshwar, and Dandeshwar, its historic cobblestone bazaars, and its unbroken heritage of ritual Aipan art.',
        'hero_image': '/static/images/Almora/almora.png',
        'altitude': '1,604 m – 2,200 m',
        'best_time': 'Year-round; March–May for blooms & Sep–Nov for crystalline Himalayan views',
        'lat': 29.5892, 'lng': 79.6467,
        'key_highlights': ['124 Deodar Shrines of Jageshwar Dham', 'Kasar Devi Geomagnetic Energy Ridge', 'Chitai Golu Devta Temple of Justice', 'Historic Nanda Devi Temple', 'Vriddha Jageshwar Himalayan Vista', 'Dandeshwar Ancient Katyuri Shrines']
    },
    'nainital': {
        'slug': 'nainital',
        'name': 'Nainital',
        'region': 'Kumaon',
        'tagline': 'Emerald Lakes, Colonial Heritage and Himalayan Ridge Vistas',
        'overview': 'Surrounding the emerald green Naini Lake at 2,084m, Nainital was founded amidst sacred legends of Goddess Sati. Beyond the bustling lakeside mall road lie sacred shrines like Naina Devi, the highest ridge of Naini Peak (2,615m), and the historic viewpoint of Tiffin Top.',
        'hero_image': '/static/images/Nanital/Nanital_city.png',
        'altitude': '2,084 m – 2,615 m',
        'best_time': 'March–June & Sep–Nov (Clear skies, ideal boating & panoramic Himalayan ridge walks)',
        'lat': 29.3919, 'lng': 79.4542,
        'key_highlights': ['Emerald Naini Lake & Boating', 'Sacred Naina Devi Shakti Peeth', 'Historic Lakeside Mall Road', 'Panoramic Naini Peak (2,615m)', 'Tiffin Top & Dorothy\'s Seat']
    },
    'pithoragarh': {
        'slug': 'pithoragarh',
        'name': 'Pithoragarh',
        'region': 'Kumaon',
        'tagline': 'Sojourn in the Soar Valley and Gateway to the Panchachuli Glaciers',
        'overview': 'Bordering Tibet and Nepal, Pithoragarh is Kumaon\'s eastern frontier of towering peaks and deep glacial gorges. Known as "Mini Kashmir," the fertile Soar Valley sits crowned by the historic Pithoragarh Fort, while its northern reaches lead to Munsiyari, the five peaks of Panchachuli, and ancient Bhotia trading paths.',
        'hero_image': '/static/images/destinations/pithoragarh_fort.jpg',
        'altitude': '1,645 m – 2,200 m',
        'best_time': 'April–June & Sep–Nov (Peak visibility of Panchachuli snow peaks and trekking weather)',
        'lat': 29.5830, 'lng': 80.2180,
        'key_highlights': ['Panchachuli Five Glacier Peaks', 'Historic Pithoragarh Fort', 'Bhotia Tribal Wool Weaving', 'Milam and Ralam Glacier Treks']
    },
    'uttarkashi': {
        'slug': 'uttarkashi',
        'name': 'Uttarkashi',
        'region': 'Garhwal',
        'tagline': 'Sacred Bhagirathi Valley, Harsil Orchards & Gangotri Gateway',
        'overview': 'Gateway to Gangotri and Yamunotri, cradled along the sacred Bhagirathi River. Uttarkashi is renowned for the historic Nehru Institute of Mountaineering, the fairy-tale apple orchards of Harsil, and ancient timber-crafted temples of Barkot.',
        'hero_image': '/static/images/destinations/uttarkashi.jpg',
        'altitude': '1,158 m – 3,415 m',
        'best_time': 'April–June & Sep–Nov (Ideal for pilgrimage, apple harvest and high-altitude hiking)',
        'lat': 30.7268, 'lng': 78.4354,
        'key_highlights': ['Harsil Valley Apple Orchards', 'Historic Kashi Vishwanath Temple', 'Gartang Gali Cliffside Boardwalk', 'Dayara Bugyal Alpine Meadows']
    }
}

LEGACY_DISTRICT_MAP = {
    'champawat': 'pithoragarh',
    'bageshwar': 'almora',
    'chamoli': 'uttarkashi',
    'rudraprayag': 'uttarkashi',
    'tehri': 'uttarkashi',
    'dehradun': 'uttarkashi',
    'haridwar': 'uttarkashi'
}

DISTRICT_LOOKUP = {
    'almora': ['almora', 'jageshwar', 'kasar', 'kasar devi', 'bageshwar', 'kausani', 'ranikhet', 'binsar'],
    'nainital': ['nainital', 'bhimtal', 'pangot', 'naini', 'mukteshwar', 'sattal', 'bhowali'],
    'pithoragarh': ['pithoragarh', 'munsiyari', 'munsyari', 'panchachuli', 'champawat'],
    'uttarkashi': ['uttarkashi', 'harsil', 'barkot', 'gangotri', 'yamunotri', 'dayara bugyal', 'chamoli', 'chopta']
}


@bp.route('/')
def index():
    region = request.args.get('region', '').strip()
    category = request.args.get('category', '').strip()
    district = request.args.get('district', '').strip()
    q = request.args.get('q', '').strip()

    query = Destination.query
    if region:
        query = query.filter_by(region=region)
    if category:
        query = query.filter_by(category=category)

    if district:
        # Match district or aliases
        dist_key = district.lower().replace('&', ' ').replace('-', ' ').strip()
        matched_terms = [district]
        for key, terms in DISTRICT_LOOKUP.items():
            if key in dist_key or dist_key in key:
                matched_terms.extend(terms)
        conditions = []
        for term in set(matched_terms):
            conditions.append(Destination.district.ilike(f'%{term}%'))
            conditions.append(Destination.name.ilike(f'%{term}%'))
            conditions.append(Destination.description.ilike(f'%{term}%'))
        query = query.filter(db.or_(*conditions))

    if q:
        query = query.filter((Destination.name.ilike(f'%{q}%')) | (Destination.description.ilike(f'%{q}%')) | (Destination.district.ilike(f'%{q}%')))

    if region:
        query = query.filter_by(region=region)
    if category:
        query = query.filter_by(category=category)
    if q:
        query = query.filter((Destination.name.ilike(f'%{q}%')) | (Destination.description.ilike(f'%{q}%')) | (Destination.district.ilike(f'%{q}%')))
    destinations = query.order_by(Destination.featured.desc()).all()

    # Compute crowd scores for all destinations
    crowd_scores = {}
    for dest in destinations:
        try:
            crowd_scores[dest.id] = compute_crowd_score(dest.id, dest.district)
        except Exception:
            crowd_scores[dest.id] = None

    # HTMX partial response
    if request.headers.get('HX-Request'):
        return render_template('destinations/_grid.html', destinations=destinations,
                               crowd_scores=crowd_scores)

    return render_template(
        'destinations/index.html',
        destinations=destinations,
        active_region=region,
        active_category=category,
        districts=DISTRICTS_DATA,
        crowd_scores=crowd_scores,
        title='Destinations — Beyond Tour'
    )


@bp.route('/<int:dest_id>')
def detail(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    nearby_hotels = Hotel.query.filter(
        (Hotel.destination_id == dest.id) | (Hotel.district == dest.district)
    ).limit(4).all()

    # Weather layer
    weather = get_weather(dest.lat, dest.lng, f'dest_{dest.id}')

    # Crowd indicator
    crowd = compute_crowd_score(dest.id, dest.district)

    # Best Time to Visit
    best_time_info = compute_best_time(
        dest.id, dest.district,
        weather_daily=weather.get('daily', [])
    )

    # Reviews
    reviews = Review.query.filter_by(target_type='destination', target_id=dest.id).order_by(Review.created_at.desc()).all()

    # Verified local guides from the 4 provided guides
    nearby_guides = Guide.query.filter(
        (Guide.district.ilike(f'%{dest.district}%')) |
        (Guide.districts_served.ilike(f'%{dest.district}%'))
    ).order_by(Guide.rating.desc()).limit(2).all()
    if not nearby_guides:
        nearby_guides = Guide.query.order_by(Guide.rating.desc()).limit(2).all()

    return render_template(
        'destinations/detail.html',
        dest=dest,
        nearby_hotels=nearby_hotels,
        nearby_guides=nearby_guides,
        weather=weather,
        crowd=crowd,
        best_time_info=best_time_info,
        reviews=reviews,
        title=f'{dest.name} — Beyond Tour'
    )


@bp.route('/districts/<slug>')
@bp.route('/district/<slug>')
def district_detail(slug):
    slug = slug.lower()
    if slug in LEGACY_DISTRICT_MAP:
        return redirect(url_for('destinations.district_detail', slug=LEGACY_DISTRICT_MAP[slug]))
    if slug not in DISTRICTS_DATA:
        abort(404)
    district_info = DISTRICTS_DATA[slug]
    district_name = district_info['name']
    region_key = district_info.get('region', 'kumaon').lower()

    # Search terms for this district & all its sub-destinations
    terms = get_district_search_terms(slug)
    matched_slugs = set(terms)
    matched_slugs.add(slug)
    matched_slugs.add(district_name.lower())

    # Filter top attractions for this district using all aliases
    conditions = []
    for term in matched_slugs:
        conditions.append(Destination.district.ilike(f'%{term}%'))
        conditions.append(Destination.name.ilike(f'%{term}%'))
        conditions.append(Destination.slug.ilike(f'%{term}%'))
    attractions = Destination.query.filter(db.or_(*conditions)).all()

    # If few attractions match exact district, fall back to region attractions
    if len(attractions) < 2:
        extra = Destination.query.filter_by(region=region_key).limit(3).all()
        attractions = attractions + [a for a in extra if a not in attractions]

    # Crowd scores for attractions
    crowd_scores = {}
    for a in attractions:
        try:
            crowd_scores[a.id] = compute_crowd_score(a.id, a.district)
        except Exception:
            crowd_scores[a.id] = None

    # Filter culture & food callouts for this district and region
    culture_conditions = [CultureEntry.region == region_key]
    for term in matched_slugs:
        culture_conditions.append(CultureEntry.district.ilike(f'%{term}%'))
    culture_callouts = CultureEntry.query.filter(db.or_(*culture_conditions)).limit(4).all()

    food_callouts = FoodItem.query.filter_by(region=region_key).limit(4).all()

    # Hotels & homestays in this district using all aliases
    hotel_conds = []
    for term in matched_slugs:
        hotel_conds.append(Hotel.district.ilike(f'%{term}%'))
        hotel_conds.append(Hotel.name.ilike(f'%{term}%'))
        hotel_conds.append(Hotel.host_story.ilike(f'%{term}%'))
    hotels = Hotel.query.filter(db.or_(*hotel_conds)).all()

    # If no hotels found with aliases, fall back to all stays
    if not hotels:
        hotels = Hotel.query.limit(4).all()

    # District weather
    lat = district_info.get('lat')
    lng = district_info.get('lng')
    weather = get_weather(lat, lng, f'district_{slug}')

    # District crowd & best time guidance
    ref_dest_id = attractions[0].id if attractions else 1
    district_crowd = compute_crowd_score(ref_dest_id, slug)
    best_time_info = compute_best_time(ref_dest_id, slug, weather_daily=weather.get('daily', []))

    # Verified local mountain guides in this district (filtered from the 4 provided guides)
    guide_conds = []
    for term in matched_slugs:
        guide_conds.append(Guide.district.ilike(f'%{term}%'))
        guide_conds.append(Guide.districts_served.ilike(f'%{term}%'))
    district_guides = Guide.query.filter(db.or_(*guide_conds)).order_by(Guide.rating.desc()).all()

    return render_template(
        'destinations/district_detail.html',
        district=district_info,
        attractions=attractions,
        culture_callouts=culture_callouts,
        food_callouts=food_callouts,
        hotels=hotels,
        district_guides=district_guides,
        weather=weather,
        crowd_scores=crowd_scores,
        district_crowd=district_crowd,
        best_time_info=best_time_info,
        title=f'{district_name} District — Beyond Tour'
    )
