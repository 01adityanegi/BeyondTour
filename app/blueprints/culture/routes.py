import json
from flask import render_template, request, abort
from app.extensions import db
from app.blueprints.culture import bp
from app.models import CultureEntry, FoodItem, Hotel
from app.blueprints.culture.kumaon_festivals import get_kumaon_festivals, get_kumaon_festival_by_slug
from app.blueprints.culture.festival_data import (
    get_all_festivals,
    get_festival_by_slug,
    get_living_culture,
    get_traditional_arts,
    get_art_by_id,
    get_map_locations,
    get_nanda_raj_jat_yatra
)


@bp.route('/')
@bp.route('/festivals')
def index():
    region = request.args.get('region', 'all').strip().lower()
    query_text = request.args.get('q', '').strip()
    district = request.args.get('district', 'all').strip()
    month = request.args.get('month', 'all').strip()
    category = request.args.get('category', 'all').strip()
    soon = request.args.get('soon', '0').strip().lower() in ('1', 'true', 'on', 'yes')

    # Load 12 Featured Cultural Experiences + Guide-contributed festivals
    all_featured_festivals = list(get_all_festivals())
    existing_slugs = {f.get('slug') for f in all_featured_festivals}

    # Guide-contributed cultural festivals from database
    db_festivals = CultureEntry.query.filter_by(entry_type='festival').order_by(CultureEntry.created_at.desc()).all()
    for ge in db_festivals:
        if ge.slug and ge.slug not in existing_slugs:
            guide_fest_dict = {
                'id': ge.slug or f"fest-{ge.id}",
                'slug': ge.slug or f"fest-{ge.id}",
                'title': ge.title,
                'subtitle': ge.subtitle or f"Traditional Himalayan Gathering in {ge.district}",
                'region': (ge.region or 'kumaon').lower(),
                'region_name': (ge.region or 'kumaon').capitalize(),
                'district': ge.district or 'Almora',
                'location': ge.venue or f"{ge.district} Cultural Grounds",
                'map_location_key': (ge.district or 'almora').lower(),
                'category': ge.category or 'Traditional Fair & Trade Heritage',
                'type_key': 'fairs' if 'fair' in (ge.category or '').lower() else 'festivals',
                'season': 'autumn' if (ge.month_number or 10) in [9, 10, 11] else ('winter' if (ge.month_number or 10) in [12, 1, 2] else 'summer'),
                'season_name': ge.month_name or 'October',
                'date_display': ge.event_date or ge.when_celebrated or f"Annually in {ge.month_name}",
                'date_note': ge.when_celebrated or 'Local mountain celebration',
                'verified': True,
                'guide_id': ge.guide_id,
                'guide_name': ge.guide_name,
                'video_url': ge.video_url or '',
                'image': ge.cover_image_url or '/static/images/festivals/bada_haat_mela.jpg',
                'cover_image_url': ge.cover_image_url or '/static/images/festivals/bada_haat_mela.jpg',
                'image_attribution': f"Curated by Guide {ge.guide_name}" if ge.guide_name else "Uttarakhand Cultural Heritage",
                'short_story': (ge.story_text[:280] + '...') if len(ge.story_text or '') > 280 else (ge.story_text or ''),
                'full_story': ge.story_text or '',
                'story_text': ge.story_text or '',
                'venue': ge.venue or f"{ge.district} Cultural Grounds",
                'when_celebrated': ge.when_celebrated or ge.event_date or f"Annually in {ge.month_name}",
                'visitor_experience': [
                    ge.venue or f"{ge.district} heritage grounds",
                    ge.deity_or_ritual or "Sacred mountain rituals and prayers",
                    ge.travel_tips or "Respect local sacred customs",
                    f"Curated by local guide {ge.guide_name}" if ge.guide_name else "Living mountain folklore"
                ],
                'is_guide_curated': True,
                'is_happening_soon': bool(ge.is_happening_soon)
            }
            all_featured_festivals.insert(0, guide_fest_dict)
            existing_slugs.add(ge.slug)

    enriched_featured = []
    for fest in all_featured_festivals:
        item = dict(fest)
        d_key = fest.get('map_location_key') or fest.get('district', '').lower()
        matched_hotels = Hotel.query.filter(
            db.or_(
                Hotel.district.ilike(f'%{d_key}%'),
                Hotel.name.ilike(f'%{d_key}%')
            )
        ).limit(3).all()
        if not matched_hotels:
            reg = fest.get('region', 'kumaon')
            matched_hotels = Hotel.query.filter(Hotel.district.ilike(f'%{reg}%')).limit(3).all()
        if not matched_hotels:
            matched_hotels = Hotel.query.limit(3).all()

        item['hotels'] = [
            {
                'id': h.id,
                'name': h.name,
                'hotel_type': h.hotel_type,
                'district': h.district,
                'price_min': h.price_min,
                'rating': h.rating,
                'review_count': h.review_count,
                'cover_image_url': h.cover_image_url,
                'host_name': h.host_name
            } for h in matched_hotels
        ]
        enriched_featured.append(item)

    living_culture = get_living_culture()
    traditional_arts = get_traditional_arts()
    map_locations = get_map_locations()
    nanda_yatra = get_nanda_raj_jat_yatra()

    # Legacy database festivals for directory reference
    legacy_query = CultureEntry.query.filter_by(entry_type='festival')
    legacy_festivals = legacy_query.order_by(CultureEntry.month_number.asc()).all()
    legacy_data = [f.to_dict() for f in legacy_festivals]

    initial_config = {
        'festivals': enriched_featured,
        'legacyFestivals': legacy_data,
        'searchQuery': query_text,
        'selectedRegion': region if region in ('kumaon', 'garhwal') else 'all',
        'selectedDistrict': district.lower() if district else 'all',
        'selectedCategory': category.lower() if category else 'all',
        'selectedMonth': month if month else 'all',
        'happeningSoon': bool(soon),
    }

    return render_template(
        'culture/index.html',
        featured_festivals=enriched_featured,
        living_culture=living_culture,
        traditional_arts=traditional_arts,
        map_locations=map_locations,
        nanda_yatra=nanda_yatra,
        featured_festivals_json=json.dumps(enriched_featured),
        living_culture_json=json.dumps(living_culture),
        traditional_arts_json=json.dumps(traditional_arts),
        map_locations_json=json.dumps(map_locations),
        nanda_yatra_json=json.dumps(nanda_yatra),
        initial_config_json=json.dumps(initial_config),
        active_region=region,
        active_district=district,
        active_month=month,
        active_category=category,
        happening_soon=soon,
        query_text=query_text,
        title='Festivals, Melas & Living Culture of Uttarakhand — Beyond Tour'
    )


@bp.route('/festivals/<slug>')
def festival_by_slug(slug):
    slug_clean = str(slug).lower().strip()
    # Check festival_data dataset first
    fest_dict = get_festival_by_slug(slug_clean)
    db_fest = CultureEntry.query.filter_by(slug=slug_clean, entry_type='festival').first()

    if not db_fest and not fest_dict:
        # Check known common variants
        if slug_clean in ('nanda-devi-mela-nainital', 'nanda-devi-fair-almora'):
            fest_dict = get_festival_by_slug('nanda-devi-mela')
        elif slug_clean in ('uttarayani-fair', 'uttarayani-fair-bageshwar'):
            fest_dict = get_festival_by_slug('uttarayani-kauthig')

    if not db_fest and not fest_dict:
        abort(404)

    # Use fest_dict as target or adapt db_fest
    if fest_dict:
        target_festival = dict(fest_dict)
        if db_fest:
            if db_fest.video_url:
                target_festival['video_url'] = db_fest.video_url
            if db_fest.guide_name:
                target_festival['guide_name'] = db_fest.guide_name
                target_festival['is_guide_curated'] = True
        district_search = (fest_dict.get('district') or 'almora').split('/')[0].strip()
        region = fest_dict.get('region') or 'kumaon'
    else:
        target_festival = db_fest.to_dict()
        target_festival['image'] = db_fest.cover_image_url or '/static/images/festivals/bada_haat_mela.jpg'
        target_festival['cover_image_url'] = db_fest.cover_image_url or '/static/images/festivals/bada_haat_mela.jpg'
        target_festival['full_story'] = db_fest.story_text or ''
        target_festival['short_story'] = db_fest.subtitle or ''
        target_festival['location'] = db_fest.venue or f"{db_fest.district} Cultural Grounds"
        target_festival['date_display'] = db_fest.event_date or db_fest.when_celebrated or f"Annually in {db_fest.month_name}"
        target_festival['date_note'] = db_fest.when_celebrated or ''
        target_festival['is_guide_curated'] = bool(db_fest.guide_id or db_fest.guide_name)
        target_festival['guide_name'] = db_fest.guide_name
        target_festival['video_url'] = db_fest.video_url or ''
        district_search = (db_fest.district or 'almora').split('/')[0].strip()
        region = db_fest.region or 'kumaon'

    kumaon_data = get_kumaon_festival_by_slug(slug_clean)

    # Connected Hotels & Homestays in this location
    hotels = Hotel.query.filter(
        db.or_(
            Hotel.district.ilike(f'%{district_search}%'),
            Hotel.name.ilike(f'%{district_search}%')
        )
    ).limit(4).all()
    if not hotels:
        hotels = Hotel.query.filter(Hotel.district.ilike(f'%{region}%')).limit(4).all()
    if not hotels:
        hotels = Hotel.query.limit(4).all()

    # Related festivals from dataset
    all_fests = get_all_festivals()
    related = [
        f for f in all_fests
        if f.get('slug') != slug_clean and (f.get('region') == region or district_search.lower() in f.get('district', '').lower())
    ][:3]
    if not related:
        related = [f for f in all_fests if f.get('slug') != slug_clean][:3]

    if request.headers.get('HX-Request') and request.args.get('modal'):
        return render_template('culture/_festival_modal.html', festival=target_festival, kumaon_data=kumaon_data, hotels=hotels)

    return render_template(
        'culture/festival_detail.html',
        festival=target_festival,
        kumaon_data=kumaon_data,
        hotels=hotels,
        district_search=district_search,
        related_festivals=related,
        title=f"{target_festival.get('title', 'Festival')} — Beyond Tour"
    )


@bp.route('/festival/<int:entry_id>')
def festival_detail(entry_id):
    entry = CultureEntry.query.get_or_404(entry_id)
    if entry.slug:
        return festival_by_slug(entry.slug)
    return render_template('culture/festival_detail.html', festival=entry, title=f'{entry.title} — Beyond Tour')


@bp.route('/art')
def art():
    region = request.args.get('region', 'all').lower()
    traditional_arts = get_traditional_arts()
    if region in ('kumaon', 'garhwal'):
        filtered_arts = [a for a in traditional_arts if region in a.get('region', '').lower()]
    else:
        filtered_arts = traditional_arts

    return render_template(
        'culture/art.html',
        traditional_arts=filtered_arts,
        all_traditional_arts=traditional_arts,
        traditional_arts_json=json.dumps(traditional_arts),
        active_region=region,
        title='Arts, Crafts & Master Artisans of Uttarakhand — Beyond Tour'
    )


@bp.route('/food')
def food():
    region = request.args.get('region', 'all')
    if region == 'all':
        foods = FoodItem.query.all()
    else:
        foods = FoodItem.query.filter_by(region=region).all()
    return render_template(
        'culture/food.html',
        foods=foods,
        active_region=region,
        title='Local Food — Beyond Tour'
    )
