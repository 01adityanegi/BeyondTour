import json
from flask import render_template, request, jsonify, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.blueprints.trip_planner import bp
from app.extensions import db
from app.models import Trip, Destination
from app.blueprints.trip_planner.generator import parse_natural_trip_query, generate_itinerary


@bp.route('/', methods=['GET', 'POST'])
def index():
    # Natural language query from search bar or URL parameter
    q = request.args.get('q', '').strip()
    is_htmx = bool(request.headers.get('HX-Request'))

    if request.method == 'POST':
        prompt = request.form.get('prompt', '').strip()
        try:
            days = int(request.form.get('days', 3))
        except (ValueError, TypeError):
            days = 3

        try:
            budget = int(request.form.get('budget', 25000))
        except (ValueError, TypeError):
            budget = 25000

        budget_type = request.form.get('budget_type', 'total')
        try:
            members = int(request.form.get('members', 2))
        except (ValueError, TypeError):
            members = 2

        transport_mode = request.form.get('transport_mode', 'personal_car')
        group_type = request.form.get('group_type', 'couple')
        interests = request.form.getlist('interests') or ['culture', 'nature']
        start_city = request.form.get('start_city', 'Delhi')
        destination = request.form.get('destination', '').strip()

        # If user typed a prompt inside the form, parse it to enrich parameters
        parsed = None
        if prompt:
            parsed = parse_natural_trip_query(prompt)
            if not destination or destination == 'nainital' or (parsed['destination'] and parsed['destination'] != 'nainital'):
                destination = parsed['destination']
            if parsed.get('days_explicit') or not request.form.get('days'):
                days = parsed['days']
            if parsed.get('budget') and (not request.form.get('budget') or budget == 25000 or budget != parsed.get('budget')):
                budget = parsed['budget']
                budget_type = parsed['budget_type']
            if parsed.get('members') and (not request.form.get('members') or members == 2):
                members = parsed['members']
            if parsed.get('transport_mode'):
                transport_mode = parsed['transport_mode']

        if not destination:
            destination = 'almora'

        itinerary = generate_itinerary(
            days=days,
            budget=budget,
            group_type=group_type,
            interests=interests,
            start_city=start_city,
            destination=destination,
            prompt=prompt,
            members=members,
            budget_type=budget_type,
            transport_mode=transport_mode
        )

        parsed_info = parsed or {
            'days': days,
            'budget': budget,
            'budget_type': budget_type,
            'members': members,
            'transport_mode': transport_mode,
            'destination': destination,
            'group_type': group_type
        }

        # Save trip if logged in
        trip = None
        if current_user.is_authenticated:
            trip = Trip(
                user_id=current_user.id,
                title=itinerary.get('title', f'{days}-Day {destination.title()} Trip'),
                itinerary_json=json.dumps(itinerary),
                days=days,
                budget=budget,
                group_type=group_type,
                interests=json.dumps(interests),
                start_city=start_city
            )
            db.session.add(trip)
            db.session.commit()

        return render_template(
            'trip_planner/result.html',
            itinerary=itinerary,
            trip=trip,
            query_prompt=prompt,
            parsed_info=parsed_info,
            is_htmx=is_htmx,
            title=f"{itinerary.get('title', 'Your Itinerary')} — Beyond Tour"
        )

    elif q:
        # User submitted query via hero search bar or GET link
        parsed = parse_natural_trip_query(q)
        days = parsed['days']
        budget = parsed['budget']
        destination = parsed['destination']
        group_type = parsed['group_type']
        interests = parsed['interests']
        start_city = parsed.get('start_city', 'Delhi')
        members = parsed['members']
        budget_type = parsed['budget_type']
        transport_mode = parsed['transport_mode']

        itinerary = generate_itinerary(
            days=days,
            budget=budget,
            group_type=group_type,
            interests=interests,
            start_city=start_city,
            destination=destination,
            prompt=q,
            members=members,
            budget_type=budget_type,
            transport_mode=transport_mode
        )

        trip = None
        if current_user.is_authenticated:
            trip = Trip(
                user_id=current_user.id,
                title=itinerary.get('title', f'{days}-Day {destination.title()} Trip'),
                itinerary_json=json.dumps(itinerary),
                days=days,
                budget=budget,
                group_type=group_type,
                interests=json.dumps(interests),
                start_city=start_city
            )
            db.session.add(trip)
            db.session.commit()

        return render_template(
            'trip_planner/result.html',
            itinerary=itinerary,
            trip=trip,
            query_prompt=q,
            parsed_info=parsed,
            is_htmx=is_htmx,
            title=f"{itinerary.get('title', 'Your Itinerary')} — Beyond Tour"
        )

    # Pre-populate form_data from query arguments if available (e.g. from Customize / Change Filters or links)
    form_data = {
        'prompt': request.args.get('prompt', '').strip(),
        'destination': request.args.get('destination', 'nainital').strip().lower(),
        'days': request.args.get('days', 3, type=int),
        'budget': request.args.get('budget', 25000, type=int),
        'budget_type': request.args.get('budget_type', 'total').strip().lower(),
        'members': request.args.get('members', 2, type=int),
        'transport_mode': request.args.get('transport_mode', 'personal_car').strip().lower(),
        'group_type': request.args.get('group_type', 'couple').strip().lower(),
        'interests': request.args.getlist('interests') or ['culture', 'nature'],
        'start_city': request.args.get('start_city', 'Delhi').strip()
    }

    return render_template(
        'trip_planner/index.html',
        form_data=form_data,
        initial_prompt=form_data['prompt'],
        title='AI Trip Planner — Beyond Tour'
    )


@bp.route('/route')
def smart_route():
    trip_id = request.args.get('trip_id', type=int)
    day_num = request.args.get('day', type=int)
    stops_param = request.args.get('stops', '').strip()
    destination_param = request.args.get('destination', '').strip().lower()
    custom_title = request.args.get('title', '').strip()

    trip = None
    trip_days = []
    initial_stops = []

    if trip_id:
        trip = Trip.query.get(trip_id)
        if trip and trip.itinerary_json:
            try:
                itin = json.loads(trip.itinerary_json)
                trip_days = itin.get('days', [])
                if day_num and 1 <= day_num <= len(trip_days):
                    selected_day = trip_days[day_num - 1]
                    initial_stops = [s.get('place') for s in selected_day.get('stops', []) if s.get('place')]
                    if not custom_title:
                        custom_title = f"{trip.title} — Day {day_num}: {selected_day.get('theme', '')}"
                elif trip_days:
                    # Collect stops from all days or key stops
                    for d in trip_days:
                        for s in d.get('stops', []):
                            p = s.get('place')
                            if p and p not in initial_stops:
                                initial_stops.append(p)
                            if len(initial_stops) >= 5:
                                break
                        if len(initial_stops) >= 5:
                            break
                    if not custom_title:
                        custom_title = trip.title
            except Exception:
                pass

    if not initial_stops and stops_param:
        initial_stops = [s.strip() for s in stops_param.split(',') if s.strip()]

    if not initial_stops and destination_param:
        presets = {
            'nainital': ['Haldwani', 'Naini Lake', "Tiffin Top (Dorothy's Seat)", 'Snow View Point', 'Eco Cave Gardens'],
            'almora': ['Kathgodam', 'Almora Heritage Town', 'Kasar Devi Temple', 'Chitai Golu Devta Temple', 'Binsar Wildlife Sanctuary'],
            'pithoragarh': ['Almora', 'Berinag', 'Munsiyari', 'Panchachuli Base'],
            'uttarkashi': ['Rishikesh', 'Tehri Lake & Dam', 'Uttarkashi', 'Chopta & Tungnath'],
        }
        initial_stops = presets.get(destination_param, ['Haldwani', 'Nainital', 'Almora', 'Munsiyari'])

    if not initial_stops:
        initial_stops = ['Haldwani', 'Nainital', 'Almora', 'Munsiyari']

    # Pre-aggregate known Uttarakhand mountain locations for geocoding fallback
    known_places = {}
    try:
        destinations = Destination.query.all()
        for d in destinations:
            if d.lat and d.lng:
                known_places[d.name.lower()] = {
                    'name': d.name,
                    'lat': d.lat,
                    'lng': d.lng,
                    'district': d.district or '',
                    'category': d.category or '',
                    'altitude_m': d.altitude_m or 0
                }
    except Exception:
        pass

    # Gateway transit hubs and notable mountain checkpoints
    gateways = {
        'haldwani': {'name': 'Haldwani', 'lat': 29.2183, 'lng': 79.5130, 'district': 'Nainital', 'category': 'transit', 'altitude_m': 424},
        'kathgodam': {'name': 'Kathgodam', 'lat': 29.2717, 'lng': 79.5377, 'district': 'Nainital', 'category': 'transit', 'altitude_m': 554},
        'nainital': {'name': 'Nainital', 'lat': 29.3919, 'lng': 79.4542, 'district': 'Nainital', 'category': 'lake', 'altitude_m': 2084},
        'almora': {'name': 'Almora', 'lat': 29.5969, 'lng': 79.6538, 'district': 'Almora', 'category': 'heritage', 'altitude_m': 1604},
        'munsiyari': {'name': 'Munsiyari', 'lat': 30.0668, 'lng': 80.2369, 'district': 'Pithoragarh', 'category': 'trek', 'altitude_m': 2200},
        'snow view point': {'name': 'Snow View Point', 'lat': 29.3989, 'lng': 79.4589, 'district': 'Nainital', 'category': 'viewpoint', 'altitude_m': 2270},
        'eco cave gardens': {'name': 'Eco Cave Gardens', 'lat': 29.3879, 'lng': 79.4442, 'district': 'Nainital', 'category': 'nature', 'altitude_m': 2020},
        'tiffin top': {'name': "Tiffin Top (Dorothy's Seat)", 'lat': 29.3833, 'lng': 79.4417, 'district': 'Nainital', 'category': 'trek', 'altitude_m': 2292},
        "tiffin top (dorothy's seat)": {'name': "Tiffin Top (Dorothy's Seat)", 'lat': 29.3833, 'lng': 79.4417, 'district': 'Nainital', 'category': 'trek', 'altitude_m': 2292},
        "tiffin top (dorothy's seat) trek": {'name': "Tiffin Top (Dorothy's Seat)", 'lat': 29.3833, 'lng': 79.4417, 'district': 'Nainital', 'category': 'trek', 'altitude_m': 2292},
        'snow view point & aerial ropeway': {'name': 'Snow View Point & Aerial Ropeway', 'lat': 29.3989, 'lng': 79.4589, 'district': 'Nainital', 'category': 'viewpoint', 'altitude_m': 2270},
        'naini lake boating': {'name': 'Naini Lake', 'lat': 29.3919, 'lng': 79.4542, 'district': 'Nainital', 'category': 'lake', 'altitude_m': 2084},
        'naina devi shakti peeth': {'name': 'Naina Devi Temple', 'lat': 29.3950, 'lng': 79.4510, 'district': 'Nainital', 'category': 'temple', 'altitude_m': 2088},
        'mall road & tibetan bhotia bazaar': {'name': 'Mall Road Nainital', 'lat': 29.3900, 'lng': 79.4580, 'district': 'Nainital', 'category': 'heritage', 'altitude_m': 2080},
        'bhimtal': {'name': 'Bhimtal', 'lat': 29.3500, 'lng': 79.5667, 'district': 'Nainital', 'category': 'lake', 'altitude_m': 1370},
        'sattal': {'name': 'Sattal', 'lat': 29.3622, 'lng': 79.5350, 'district': 'Nainital', 'category': 'lake', 'altitude_m': 1370},
        'mukteshwar': {'name': 'Mukteshwar', 'lat': 29.4722, 'lng': 79.6479, 'district': 'Nainital', 'category': 'viewpoint', 'altitude_m': 2171},
        'ranikhet': {'name': 'Ranikhet', 'lat': 29.6434, 'lng': 79.4322, 'district': 'Almora', 'category': 'heritage', 'altitude_m': 1869},
        'kausani': {'name': 'Kausani', 'lat': 29.8378, 'lng': 79.5960, 'district': 'Bageshwar', 'category': 'viewpoint', 'altitude_m': 1890},
        'rishikesh': {'name': 'Rishikesh', 'lat': 30.0869, 'lng': 78.2676, 'district': 'Dehradun', 'category': 'heritage', 'altitude_m': 372},
        'haridwar': {'name': 'Haridwar', 'lat': 29.9457, 'lng': 78.1642, 'district': 'Haridwar', 'category': 'pilgrimage', 'altitude_m': 314},
        'devprayag': {'name': 'Devprayag', 'lat': 30.1459, 'lng': 78.5989, 'district': 'Tehri Garhwal', 'category': 'pilgrimage', 'altitude_m': 830},
        'rudraprayag': {'name': 'Rudraprayag', 'lat': 30.2844, 'lng': 78.9811, 'district': 'Rudraprayag', 'category': 'pilgrimage', 'altitude_m': 895},
        'joshimath': {'name': 'Joshimath', 'lat': 30.5564, 'lng': 79.5668, 'district': 'Chamoli', 'category': 'pilgrimage', 'altitude_m': 1890},
        'badrinath': {'name': 'Badrinath', 'lat': 30.7433, 'lng': 79.4938, 'district': 'Chamoli', 'category': 'temple', 'altitude_m': 3300},
        'kedarnath': {'name': 'Kedarnath', 'lat': 30.7346, 'lng': 79.0669, 'district': 'Rudraprayag', 'category': 'temple', 'altitude_m': 3583},
    }
    for k, v in gateways.items():
        if k not in known_places:
            known_places[k] = v

    google_maps_api_key = current_app.config.get('GOOGLE_MAPS_API_KEY', '')

    return render_template(
        'trip_planner/smart_route.html',
        trip=trip,
        trip_days=trip_days,
        active_day=day_num,
        initial_stops=initial_stops,
        custom_title=custom_title,
        google_maps_api_key=google_maps_api_key,
        known_places=known_places,
        title='AI Smart Route & Mountain Map — Beyond Tour'
    )
