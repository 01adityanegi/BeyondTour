from flask import render_template, request
from app.blueprints.hotels import bp
from app.extensions import db
from app.models import Hotel, Review
from app.district_cards import get_hotel_location_cards, get_district_search_terms
from app.services.weather import get_weather
from app.services.price_bands import check_price


@bp.route('/')
def index():
    district = request.args.get('district', '').strip()
    hotel_type = request.args.get('type', '').strip()
    budget = request.args.get('budget', '').strip()  # '700-1200' | '1200-2000' | '2000-3000'
    sort = request.args.get('sort', 'price_asc').strip()  # 'price_asc' | 'price_desc' | 'rating'

    # Get all listings to compute location card counts
    all_hotels = Hotel.query.all()
    location_cards = get_hotel_location_cards(all_hotels)

    query = Hotel.query
    if district:
        terms = get_district_search_terms(district)
        conditions = []
        for term in terms:
            conditions.append(Hotel.district.ilike(f'%{term}%'))
            conditions.append(Hotel.name.ilike(f'%{term}%'))
            conditions.append(Hotel.host_story.ilike(f'%{term}%'))
        query = query.filter(db.or_(*conditions))

    # Calculate type counts for the current district context
    base_district_hotels = query.all()
    homestay_count = sum(1 for h in base_district_hotels if h.hotel_type == 'homestay')
    hotel_count = sum(1 for h in base_district_hotels if h.hotel_type == 'hotel')
    restaurant_count = sum(1 for h in base_district_hotels if h.hotel_type in ('restaurant', 'cafe'))
    stays_count = homestay_count + hotel_count
    total_count = len(base_district_hotels)

    if hotel_type:
        if hotel_type in ('restaurant', 'dining'):
            query = query.filter(Hotel.hotel_type.in_(['restaurant', 'cafe']))
        elif hotel_type == 'all_with_dining':
            pass
        else:
            query = query.filter_by(hotel_type=hotel_type)
    else:
        # Default to hotels and homestays so price strictly reflects stays (₹700 - ₹3,000)
        query = query.filter(Hotel.hotel_type.in_(['homestay', 'hotel']))

    if budget:
        if budget == '700-1200':
            query = query.filter(Hotel.price_min <= 1200)
        elif budget == '1200-2000':
            query = query.filter(Hotel.price_min >= 1200, Hotel.price_min <= 2000)
        elif budget == '2000-3000':
            query = query.filter(Hotel.price_min >= 2000, Hotel.price_min <= 3000)

    if sort == 'price_desc':
        query = query.order_by(Hotel.price_min.desc())
    elif sort == 'rating':
        query = query.order_by(Hotel.rating.desc(), Hotel.price_min.asc())
    elif sort == 'featured':
        query = query.order_by(Hotel.featured.desc(), Hotel.price_min.asc())
    else:  # 'price_asc' default
        query = query.order_by(Hotel.price_min.asc(), Hotel.rating.desc())

    hotels = query.all()

    # Attach price-band flags to each hotel for UI badges
    price_flags = {}
    for h in hotels:
        if h.price_min:
            price_flags[h.id] = check_price('hotel', h.district, float(h.price_min))

    return render_template(
        'hotels/index.html',
        hotels=hotels,
        active_type=hotel_type,
        active_district=district,
        active_budget=budget,
        active_sort=sort,
        location_cards=location_cards,
        price_flags=price_flags,
        counts={
            'total': total_count,
            'stays': stays_count,
            'homestay': homestay_count,
            'hotel': hotel_count,
            'restaurant': restaurant_count
        },
        title='Hotels and Homestays in Uttarakhand — Beyond Tour'
    )


@bp.route('/<int:hotel_id>')
def detail(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    # Weather at hotel's location (fall back to destination coords if hotel has none)
    weather = get_weather(
        hotel.lat or (hotel.destination.lat if hotel.destination else None),
        hotel.lng or (hotel.destination.lng if hotel.destination else None),
        f'hotel_{hotel.id}'
    )
    # Price fairness check
    price_flag = check_price('hotel', hotel.district, float(hotel.price_min or 0))
    # Reviews
    reviews = Review.query.filter_by(target_type='hotel', target_id=hotel.id).order_by(Review.created_at.desc()).all()
    return render_template(
        'hotels/detail.html',
        hotel=hotel,
        weather=weather,
        price_flag=price_flag,
        reviews=reviews,
        title=f'{hotel.name} — Beyond Tour'
    )

