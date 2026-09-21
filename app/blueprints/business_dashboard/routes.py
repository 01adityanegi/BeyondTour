import os
import re
import base64
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, jsonify, current_app, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app.blueprints.business_dashboard import bp
from app.extensions import db
from app.models import Hotel, Guide, Booking, Review, Destination, AuditLog, CultureEntry


def slugify(text):
    text = re.sub(r'[^\w\s-]', '', (text or '').lower()).strip()
    return re.sub(r'[-\s]+', '-', text)


def log_audit(action, target_type, target_id, details=None):
    try:
        log = AuditLog(
            user_id=current_user.id if current_user.is_authenticated else None,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details
        )
        db.session.add(log)
        db.session.commit()
    except Exception:
        db.session.rollback()


@bp.route('/')
@login_required
def index():
    if current_user.role not in ['business', 'admin']:
        flash('Business account required.', 'warning')
        return redirect(url_for('main.index'))

    hotels = Hotel.query.filter_by(owner_id=current_user.id).all()
    hotel_ids = [h.id for h in hotels]
    recent_bookings = Booking.query.filter(
        Booking.target_type == 'hotel',
        Booking.target_id.in_(hotel_ids)
    ).order_by(Booking.created_at.desc()).limit(10).all() if hotel_ids else []
    total_revenue = sum(b.total_amount or 0 for b in recent_bookings if b.status == 'confirmed')

    # Also check if user has a guide profile
    guide = Guide.query.filter(db.or_(Guide.user_id == current_user.id, Guide.name == current_user.name)).first()
    festivals = []
    if guide:
        festivals = CultureEntry.query.filter_by(guide_id=guide.id).order_by(CultureEntry.created_at.desc()).all()
    if not festivals:
        festivals = CultureEntry.query.filter_by(guide_name=current_user.name).order_by(CultureEntry.created_at.desc()).all()
    if not festivals and current_user.role == 'admin':
        festivals = CultureEntry.query.filter_by(entry_type='festival').order_by(CultureEntry.created_at.desc()).limit(8).all()

    return render_template(
        'business_dashboard/index.html',
        title='Vendor Dashboard — Beyond Tour',
        hotels=hotels,
        guide=guide,
        festivals=festivals,
        bookings=recent_bookings,
        total_revenue=total_revenue
    )


@bp.route('/hotel/new', methods=['POST'])
@login_required
def hotel_new():
    if current_user.role not in ['business', 'admin']:
        abort(403)

    default_dest = Destination.query.first()
    hotel = Hotel(
        owner_id=current_user.id,
        name=f"New Himalayan Homestay",
        hotel_type='homestay',
        district='Almora',
        destination_id=default_dest.id if default_dest else None,
        price_min=1200,
        price_max=2500,
        host_name=current_user.name,
        status='pending',
        cover_image_url='https://images.unsplash.com/photo-1587061949409-02df41d5e562?w=800&q=80'
    )
    db.session.add(hotel)
    db.session.commit()
    log_audit('create', 'hotel', hotel.id, f"Created new hotel draft #{hotel.id}")
    flash("New homestay profile created. Complete the steps below to submit for live approval.", "success")
    return redirect(url_for('business_dashboard.hotel_edit', hotel_id=hotel.id))


@bp.route('/hotel/<int:hotel_id>/edit')
@login_required
def hotel_edit(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.owner_id != current_user.id and current_user.role != 'admin':
        abort(403)

    lang = request.args.get('lang', 'en').lower()
    destinations = Destination.query.order_by(Destination.name.asc()).all()

    return render_template(
        'business_dashboard/hotel_edit.html',
        hotel=hotel,
        destinations=destinations,
        lang=lang,
        title=f"Edit {hotel.name} — Vendor Self-Service"
    )


@bp.route('/hotel/<int:hotel_id>/autosave', methods=['POST'])
@login_required
def hotel_autosave(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.owner_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json(silent=True) or request.form.to_dict()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    field = data.get('field')
    value = data.get('value')

    allowed_fields = {
        'name': str,
        'district': str,
        'hotel_type': str,
        'destination_id': int,
        'price_min': int,
        'price_max': int,
        'host_name': str,
        'host_story': str,
        'amenities': str,
        'address': str,
        'cover_image_url': str
    }

    if field in allowed_fields:
        try:
            val_type = allowed_fields[field]
            if val_type == int:
                clean_val = int(value) if value else None
            else:
                clean_val = str(value).strip() if value else None
            setattr(hotel, field, clean_val)
            # If property was changes_requested, editing fields switches back to pending
            if hotel.status == 'changes_requested':
                hotel.status = 'pending'
            db.session.commit()
            log_audit('update', 'hotel', hotel.id, f"Autosaved field {field}")
            return jsonify({
                'status': 'saved',
                'field': field,
                'hotel_status': hotel.status,
                'time': datetime.now().strftime('%H:%M:%S')
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Field not recognized'}), 400


@bp.route('/hotel/<int:hotel_id>/upload-photo', methods=['POST'])
@login_required
def hotel_upload_photo(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    if hotel.owner_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json(silent=True)
    if not data or 'data_url' not in data:
        return jsonify({'error': 'No image data'}), 400

    data_url = data['data_url']
    try:
        # Save base64 image data to static uploads
        header, encoded = data_url.split(',', 1)
        image_data = base64.b64decode(encoded)
        ext = 'webp' if 'webp' in header else 'jpg'
        filename = f"hotel_{hotel.id}_{int(datetime.utcnow().timestamp())}.{ext}"
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        with open(file_path, 'wb') as f:
            f.write(image_data)

        hotel.cover_image_url = f"/static/uploads/{filename}"
        db.session.commit()
        log_audit('update', 'hotel', hotel.id, f"Uploaded new compressed photo: {filename}")
        return jsonify({
            'status': 'success',
            'image_url': hotel.cover_image_url
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@bp.route('/guide/edit')
@login_required
def guide_edit():
    guide = Guide.query.filter_by(name=current_user.name).first()
    if not guide:
        # Create initial guide draft for user
        guide = Guide(
            name=current_user.name,
            district='Chamoli',
            daily_rate=2000,
            years_experience=2,
            languages='Hindi, English, Garhwali',
            specialties='High altitude treks, valley temple lore',
            status='pending',
            verified=False,
            profile_image='https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&q=80'
        )
        db.session.add(guide)
        db.session.commit()
        log_audit('create', 'guide', guide.id, f"Created guide profile draft for {guide.name}")

    lang = request.args.get('lang', 'en').lower()
    return render_template(
        'business_dashboard/guide_edit.html',
        guide=guide,
        lang=lang,
        title=f"Guide Profile — {guide.name}"
    )


@bp.route('/guide/<int:guide_id>/autosave', methods=['POST'])
@login_required
def guide_autosave(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    if guide.name != current_user.name and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json(silent=True) or request.form.to_dict()
    if not data:
        return jsonify({'error': 'No data received'}), 400

    field = data.get('field')
    value = data.get('value')

    allowed_fields = {
        'name': str,
        'district': str,
        'districts_served': str,
        'daily_rate': int,
        'years_experience': int,
        'languages': str,
        'specialties': str,
        'bio': str,
        'profile_image': str
    }

    if field in allowed_fields:
        try:
            val_type = allowed_fields[field]
            clean_val = int(value) if val_type == int else (str(value).strip() if value else None)
            setattr(guide, field, clean_val)
            if guide.status == 'changes_requested':
                guide.status = 'pending'
            db.session.commit()
            log_audit('update', 'guide', guide.id, f"Autosaved guide field {field}")
            return jsonify({
                'status': 'saved',
                'field': field,
                'guide_status': guide.status,
                'time': datetime.now().strftime('%H:%M:%S')
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400

    return jsonify({'error': 'Field not recognized'}), 400


# ---------------------------------------------------------------------------
# Cultural Festivals & Events (Guide Portal)
# ---------------------------------------------------------------------------

MONTH_MAP = {
    'january': 1, 'february': 2, 'march': 3, 'april': 4,
    'may': 5, 'june': 6, 'july': 7, 'august': 8,
    'september': 9, 'october': 10, 'november': 11, 'december': 12
}

ALLOWED_IMG_EXTS = {'jpg', 'jpeg', 'png', 'webp'}
ALLOWED_VID_EXTS = {'mp4', 'webm', 'mov', 'm4v'}


@bp.route('/festivals/upload-media', methods=['POST'])
@login_required
def festival_upload_media():
    if current_user.role not in ['business', 'admin']:
        return jsonify({'error': 'Guide or business account required'}), 403

    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'festivals')
    os.makedirs(upload_folder, exist_ok=True)

    # 1. Direct file upload via FormData (from file input or drag-and-drop)
    if 'file' in request.files:
        uploaded_file = request.files['file']
        if not uploaded_file or uploaded_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        original_filename = secure_filename(uploaded_file.filename)
        ext = original_filename.rsplit('.', 1)[-1].lower() if '.' in original_filename else ''

        if ext in ALLOWED_IMG_EXTS:
            media_type = 'image'
        elif ext in ALLOWED_VID_EXTS:
            media_type = 'video'
        else:
            return jsonify({'error': f"Unsupported file type: .{ext}. Allowed: JPG, PNG, WEBP, MP4, WEBM"}), 400

        timestamp = int(datetime.utcnow().timestamp())
        safe_name = f"fest_{current_user.id}_{timestamp}_{original_filename}"
        dest_path = os.path.join(upload_folder, safe_name)
        uploaded_file.save(dest_path)

        url = f"/static/uploads/festivals/{safe_name}"
        return jsonify({
            'status': 'success',
            'url': url,
            'media_type': media_type,
            'filename': safe_name
        })

    # 2. Base64 JSON upload
    data = request.get_json(silent=True)
    if data and 'data_url' in data:
        data_url = data['data_url']
        try:
            header, encoded = data_url.split(',', 1)
            file_data = base64.b64decode(encoded)
            is_vid = 'video' in header or 'mp4' in header
            ext = 'mp4' if is_vid else ('webp' if 'webp' in header else ('png' if 'png' in header else 'jpg'))
            media_type = 'video' if is_vid else 'image'
            timestamp = int(datetime.utcnow().timestamp())
            safe_name = f"fest_{current_user.id}_{timestamp}.{ext}"
            dest_path = os.path.join(upload_folder, safe_name)
            with open(dest_path, 'wb') as f:
                f.write(file_data)
            url = f"/static/uploads/festivals/{safe_name}"
            return jsonify({
                'status': 'success',
                'url': url,
                'media_type': media_type,
                'filename': safe_name
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'No file received'}), 400


@bp.route('/festivals/new', methods=['GET', 'POST'])
@login_required
def festival_new():
    if current_user.role not in ['business', 'admin']:
        flash('Guide credentials required to publish cultural festivals and events.', 'warning')
        return redirect(url_for('main.index'))

    guide = Guide.query.filter(db.or_(Guide.user_id == current_user.id, Guide.name == current_user.name)).first()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if not title:
            flash('Festival or event title is required.', 'error')
            return redirect(url_for('business_dashboard.festival_new'))

        subtitle = request.form.get('subtitle', '').strip()
        district = request.form.get('district', 'Almora').strip()
        if district not in ['Almora', 'Nainital', 'Pithoragarh', 'Uttarkashi']:
            district = 'Almora'
        region = 'garhwal' if district.lower() == 'uttarkashi' else 'kumaon'

        category = request.form.get('category', 'Religious').strip()
        venue = request.form.get('venue', '').strip()
        deity_or_ritual = request.form.get('deity_or_ritual', '').strip()
        attendance = request.form.get('attendance', '').strip()
        story_text = request.form.get('story_text', '').strip()
        travel_tips = request.form.get('travel_tips', '').strip()
        when_celebrated = request.form.get('when_celebrated', '').strip()
        event_date = request.form.get('event_date', '').strip()
        month_name = request.form.get('month_name', 'October').strip()
        month_number = MONTH_MAP.get(month_name.lower(), 10)
        is_happening_soon = request.form.get('is_happening_soon') in ('1', 'true', 'on', 'yes')

        cover_image_url = request.form.get('cover_image_url', '').strip()
        video_url = request.form.get('video_url', '').strip()

        # Fallback file upload from traditional multipart POST
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'festivals')
        os.makedirs(upload_folder, exist_ok=True)
        timestamp = int(datetime.utcnow().timestamp())

        if 'cover_image_file' in request.files and request.files['cover_image_file'].filename:
            f = request.files['cover_image_file']
            fn = secure_filename(f.filename)
            safe_name = f"fest_cover_{current_user.id}_{timestamp}_{fn}"
            f.save(os.path.join(upload_folder, safe_name))
            cover_image_url = f"/static/uploads/festivals/{safe_name}"

        if 'video_file' in request.files and request.files['video_file'].filename:
            vf = request.files['video_file']
            vfn = secure_filename(vf.filename)
            safe_vname = f"fest_vid_{current_user.id}_{timestamp}_{vfn}"
            vf.save(os.path.join(upload_folder, safe_vname))
            video_url = f"/static/uploads/festivals/{safe_vname}"

        if not cover_image_url:
            cover_image_url = 'https://images.unsplash.com/photo-1609137144822-473180424578?w=800&q=80'

        # Generate unique slug
        base_slug = slugify(title)
        slug = base_slug
        existing = CultureEntry.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{base_slug}-{int(datetime.utcnow().timestamp())}"

        matched_dest = Destination.query.filter(Destination.district.ilike(f"%{district}%")).first()

        guide_id = guide.id if guide else None
        guide_name = guide.name if guide else current_user.name

        entry = CultureEntry(
            slug=slug,
            region=region,
            entry_type='festival',
            category=category,
            title=title,
            subtitle=subtitle or f"Traditional Himalayan Festival in {district}",
            district=district,
            venue=venue or f"{district} Cultural Grounds",
            deity_or_ritual=deity_or_ritual,
            attendance=attendance or "Regional gathering of devotees & travelers",
            story_text=story_text or f"Celebrated with sacred mountain rituals and traditional folk melodies in {district}.",
            travel_tips=travel_tips or "Respect sacred shrines, carry warm layers for night rituals, and ask permission before recording close ceremonies.",
            when_celebrated=when_celebrated or (event_date if event_date else f"Every year in {month_name}"),
            event_date=event_date or when_celebrated,
            month_name=month_name,
            month_number=month_number,
            is_happening_soon=is_happening_soon,
            cover_image_url=cover_image_url,
            video_url=video_url,
            guide_id=guide_id,
            guide_name=guide_name,
            destination_id=matched_dest.id if matched_dest else None
        )

        db.session.add(entry)
        db.session.commit()

        log_audit('create', 'festival', entry.id, f"Guide {guide_name} added festival '{title}' in {district}")
        flash(f"Cultural festival '{title}' has been successfully published on Beyond Tour!", "success")
        return redirect(url_for('culture.festival_by_slug', slug=entry.slug))

    destinations = Destination.query.order_by(Destination.name.asc()).all()
    default_district = guide.district if (guide and guide.district) else 'Almora'

    return render_template(
        'business_dashboard/festival_form.html',
        guide=guide,
        destinations=destinations,
        default_district=default_district,
        title='Add Regional Culture Festival / Event — Guide Portal'
    )


@bp.route('/festivals/<int:festival_id>/delete', methods=['POST'])
@login_required
def festival_delete(festival_id):
    entry = CultureEntry.query.get_or_404(festival_id)
    guide = Guide.query.filter(db.or_(Guide.user_id == current_user.id, Guide.name == current_user.name)).first()

    is_owner = (guide and entry.guide_id == guide.id) or (entry.guide_name == current_user.name)
    if not is_owner and current_user.role != 'admin':
        abort(403)

    title = entry.title
    db.session.delete(entry)
    db.session.commit()

    log_audit('delete', 'festival', festival_id, f"Deleted festival '{title}'")
    flash(f"Festival '{title}' has been removed.", "info")
    return redirect(request.referrer or url_for('business_dashboard.index'))

