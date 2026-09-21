import json
from datetime import datetime, date
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.blueprints.guides import bp
from app.extensions import db
from app.models import Guide, Booking, Review, CultureEntry

from app.district_cards import get_guide_location_cards, get_district_search_terms

@bp.route('/')
def index():
    region = request.args.get('region', '').strip()
    district = request.args.get('district', '').strip()

    all_guides = Guide.query.all()
    location_cards = get_guide_location_cards(all_guides)

    query = Guide.query
    if region:
        query = query.filter_by(region=region)
    if district:
        terms = get_district_search_terms(district)
        conditions = []
        for term in terms:
            conditions.append(Guide.district.ilike(f'%{term}%'))
            conditions.append(Guide.districts_served.ilike(f'%{term}%'))
            conditions.append(Guide.bio.ilike(f'%{term}%'))
            conditions.append(Guide.name.ilike(f'%{term}%'))
        query = query.filter(db.or_(*conditions))
    guides = query.order_by(Guide.verified.desc(), Guide.rating.desc()).all()

    return render_template(
        'guides/index.html',
        guides=guides,
        active_region=region,
        active_district=district,
        location_cards=location_cards,
        title='Local Guides — Beyond Tour'
    )



@bp.route('/<int:guide_id>')
def detail(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    
    # Parse JSON fields safely
    try:
        specialties = json.loads(guide.specialties) if guide.specialties else []
    except Exception:
        specialties = [s.strip() for s in guide.specialties.split(',')] if guide.specialties else []

    try:
        languages = json.loads(guide.languages) if guide.languages else []
    except Exception:
        languages = [l.strip() for l in guide.languages.split(',')] if guide.languages else []

    try:
        gallery_images = json.loads(guide.gallery_images) if guide.gallery_images else []
    except Exception:
        gallery_images = []

    try:
        booked_dates = json.loads(guide.availability_dates) if guide.availability_dates else []
    except Exception:
        booked_dates = []

    # Get reviews for this guide
    reviews = Review.query.filter_by(target_type='guide', target_id=guide.id).order_by(Review.created_at.desc()).all()

    # Check if current user has an existing booking with this guide
    confirmed_booking = False
    if current_user.is_authenticated:
        confirmed_booking = Booking.query.filter_by(
            user_id=current_user.id, target_type='guide', target_id=guide.id
        ).first() is not None

    # Festivals & Events curated by this guide
    curated_festivals = CultureEntry.query.filter(
        db.or_(CultureEntry.guide_id == guide.id, CultureEntry.guide_name == guide.name),
        CultureEntry.entry_type == 'festival'
    ).order_by(CultureEntry.created_at.desc()).all()

    return render_template(
        'guides/detail.html',
        guide=guide,
        specialties=specialties,
        languages=languages,
        gallery_images=gallery_images,
        booked_dates=booked_dates,
        reviews=reviews,
        curated_festivals=curated_festivals,
        confirmed_booking=confirmed_booking,
        title=f'{guide.name} — Verified Mountain Guide | Beyond Tour'
    )


@bp.route('/<int:guide_id>/book', methods=['POST'])
@login_required
def book_guide(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    start_date_str = (request.form.get('start_date') or '').strip()
    end_date_str = (request.form.get('end_date') or '').strip()
    guests = request.form.get('guests', 1, type=int)
    message = (request.form.get('message') or '').strip()
    experiences = request.form.getlist('experiences')
    destinations = request.form.getlist('destinations')

    is_ajax = bool(
        request.headers.get('HX-Request') or
        request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('Accept', '')
    )

    if not start_date_str:
        if is_ajax:
            return jsonify({'error': 'Please select a start date for your trek or tour.'}), 400
        flash('Please select a start date for your trek/tour.', 'warning')
        return redirect(url_for('guides.detail', guide_id=guide.id))

    check_in = None
    check_out = None
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y'):
        try:
            check_in = datetime.strptime(start_date_str, fmt).date()
            break
        except ValueError:
            pass

    if not check_in:
        if is_ajax:
            return jsonify({'error': 'Invalid start date format. Please select a valid date.'}), 400
        flash('Invalid start date format selected.', 'danger')
        return redirect(url_for('guides.detail', guide_id=guide.id))

    if end_date_str:
        for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m/%d/%Y'):
            try:
                check_out = datetime.strptime(end_date_str, fmt).date()
                break
            except ValueError:
                pass

    if not check_out or check_out < check_in:
        check_out = check_in

    num_days = max(1, (check_out - check_in).days + 1)
    total_amount = num_days * (guide.daily_rate or 2400)

    # Build structured requirements from checklist
    sections = []
    if experiences:
        sections.append("Desired Experiences:\n" + "\n".join(f"• {e}" for e in experiences))
    if destinations:
        sections.append("Target Destinations:\n" + "\n".join(f"• {d}" for d in destinations))
    if message:
        sections.append("Traveler Notes & Pace:\n" + message)

    full_message = "\n\n".join(sections) if sections else (message or "Mountain trek / tour inquiry")

    booking = Booking(
        user_id=current_user.id,
        target_type='guide',
        target_id=guide.id,
        check_in=check_in,
        check_out=check_out,
        guests=guests,
        total_amount=total_amount,
        status='pending',
        message=full_message
    )
    db.session.add(booking)
    db.session.commit()

    if is_ajax:
        return jsonify({
            'status': 'success',
            'guide_name': guide.name,
            'booking_id': booking.id,
            'check_in': check_in.strftime('%b %d, %Y'),
            'check_out': check_out.strftime('%b %d, %Y'),
            'num_days': num_days,
            'total_amount': total_amount,
            'experiences': experiences,
            'destinations': destinations,
            'message': f"Your request has been forwarded directly to {guide.name}. Reference ID: #{booking.id}."
        })

    flash(f'Booking request sent to {guide.name}! Reference ID: #{booking.id}.', 'success')
    return redirect(url_for('guides.detail', guide_id=guide.id))
