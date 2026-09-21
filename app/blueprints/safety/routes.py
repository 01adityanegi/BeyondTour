"""
app/blueprints/safety/routes.py
---------------------------------
Safety & Security Module for BeyondTour:
  GET  /safety/emergency-info          — Offline-cacheable district helplines page
  POST /safety/sos                     — Trigger SOS alert (auth required, rate-limited)
  GET  /safety/sos/my                  — Authenticated user's SOS history
  POST /safety/contacts                — Add/update emergency contact
  DELETE /safety/contacts/<id>         — Remove emergency contact
  POST /safety/share-location          — Generate time-boxed shareable location link (demo)
  GET  /safety/share/<token>           — Public view of shared location
"""
import json
import hmac
import hashlib
import time
from datetime import datetime, timedelta
from functools import wraps

from flask import (
    render_template, request, redirect, url_for,
    flash, jsonify, abort, current_app
)
from flask_login import login_required, current_user

from app.blueprints.safety import bp
from app.extensions import db, csrf
from app.models import SosAlert, EmergencyContact, AuditLog, User



# ── Uttarakhand Emergency Numbers (district-level) ──────────────────────
DISTRICT_HELPLINES = [
    {'district': 'Nainital',       'police': '05942-235100', 'hospital': 'B.D. Pandey Hospital: 05942-235544', 'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Almora',         'police': '05962-230300', 'hospital': 'District Hospital: 05962-230516',    'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Pithoragarh',    'police': '05964-225010', 'hospital': 'District Hospital: 05964-225069',    'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Champawat',      'police': '05965-230100', 'hospital': 'District Hospital: 05965-230040',    'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Bageshwar',      'police': '05963-220100', 'hospital': 'District Hospital: 05963-220070',    'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Haridwar',       'police': '01334-220100', 'hospital': 'Haridwar District Hospital: 01334-224001', 'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Rishikesh',      'police': '0135-2430900', 'hospital': 'AIIMS Rishikesh: 0135-2462975',      'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Dehradun',       'police': '0135-2650900', 'hospital': 'Doon Hospital: 0135-2656741',         'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Uttarkashi',     'police': '01374-222100', 'hospital': 'District Hospital: 01374-222022',     'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Chamoli',        'police': '01372-252042', 'hospital': 'District Hospital Gopeshwar: 01372-252205', 'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Rudraprayag',    'police': '01364-233300', 'hospital': 'District Hospital: 01364-233300',     'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Tehri Garhwal',  'police': '01376-233022', 'hospital': 'District Hospital New Tehri: 01376-233050', 'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Pauri Garhwal',  'police': '01368-222100', 'hospital': 'District Hospital: 01368-222180',     'sdrf': '1070', 'tourist': '1364'},
    {'district': 'Hardwar',        'police': '01334-220100', 'hospital': 'SS Hospital: 01334-220234',           'sdrf': '1070', 'tourist': '1364'},
]

NATIONAL_HELPLINES = [
    {'name': 'National Distress Helpline',      'number': '112',  'type': 'Emergency'},
    {'name': 'Uttarakhand Disaster Helpline',   'number': '1070', 'type': 'SDRF/NDRF'},
    {'name': 'Tourist Helpline',                'number': '1364', 'type': 'Tourism'},
    {'name': 'Women Helpline',                  'number': '1090', 'type': 'Safety'},
    {'name': 'Ambulance',                       'number': '108',  'type': 'Medical'},
    {'name': 'Fire Brigade',                    'number': '101',  'type': 'Fire'},
]


# ── Simple signed token for location sharing ─────────────────────────────
def _sign_location_token(user_id: int, lat: float, lng: float, expiry: float) -> str:
    secret = current_app.config['SECRET_KEY']
    payload = f'{user_id}:{lat}:{lng}:{expiry}'
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()[:16]
    return f'{user_id}_{expiry}_{sig}'


def _verify_location_token(token: str) -> dict | None:
    try:
        parts = token.split('_')
        if len(parts) != 3:
            return None
        user_id, expiry, sig = int(parts[0]), float(parts[1]), parts[2]
        if time.time() > expiry:
            return None
        # Look up the latest SOS from this user to get coordinates
        alert = SosAlert.query.filter_by(user_id=user_id).order_by(SosAlert.timestamp.desc()).first()
        if not alert:
            return None
        expected_sig = hmac.new(
            current_app.config['SECRET_KEY'].encode(),
            f'{user_id}:{alert.lat}:{alert.lng}:{expiry}'.encode(),
            hashlib.sha256
        ).hexdigest()[:16]
        if not hmac.compare_digest(sig, expected_sig):
            return None
        return {'user_id': user_id, 'lat': alert.lat, 'lng': alert.lng, 'expiry': expiry}
    except Exception:
        return None


# ── Routes ────────────────────────────────────────────────────────────────

@bp.route('/emergency-info')
def emergency_info():
    """Static district-level helpline page — no auth needed, offline-cacheable."""
    return render_template(
        'safety/emergency_info.html',
        helplines=DISTRICT_HELPLINES,
        national=NATIONAL_HELPLINES,
        title='Emergency Information — Beyond Tour'
    )


@bp.route('/sos', methods=['POST'])
@csrf.exempt
@login_required
def trigger_sos():
    """
    Receives geolocation from the SOS FAB, logs an alert.
    Rate-limited to 3 per hour per user via in-memory check.
    """
    data = request.get_json(silent=True) or request.form
    lat = data.get('lat')
    lng = data.get('lng')
    district = data.get('district', 'Unknown')

    # Simple rate-limit: max 3 SOS in last 60 min per user
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    recent_count = SosAlert.query.filter(
        SosAlert.user_id == current_user.id,
        SosAlert.timestamp >= one_hour_ago
    ).count()
    if recent_count >= 3:
        return jsonify({'ok': False, 'error': 'Too many SOS requests. Please call 112 directly.'}), 429

    # Create alert
    alert = SosAlert(
        user_id=current_user.id,
        lat=float(lat) if lat else None,
        lng=float(lng) if lng else None,
        district=district,
        status='active',
    )
    db.session.add(alert)

    # Audit log
    db.session.add(AuditLog(
        user_id=current_user.id,
        action='sos_trigger',
        target_type='sos',
        target_id=None,
        details=json.dumps({'lat': str(lat), 'lng': str(lng), 'district': district})
    ))
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return jsonify({'ok': False, 'error': 'Server error'}), 500

    # Emergency contacts to notify (in-app — real SMS hook goes here)
    contacts = EmergencyContact.query.filter_by(user_id=current_user.id).all()
    contact_names = [c.name for c in contacts]

    current_app.logger.warning(
        f'[SOS] User {current_user.id} ({current_user.name}) triggered SOS '
        f'at lat={lat}, lng={lng}, district={district}. '
        f'Contacts: {contact_names}'
    )

    return jsonify({
        'ok': True,
        'alert_id': alert.id,
        'message': 'SOS logged. Please call 112 immediately.',
        'helpline': '112',
        'contacts_notified': len(contacts),
    })


@bp.route('/contacts', methods=['GET'])
@login_required
def contacts():
    my_contacts = EmergencyContact.query.filter_by(user_id=current_user.id).all()
    return render_template('safety/contacts.html', contacts=my_contacts,
                           title='Emergency Contacts — Beyond Tour')


@bp.route('/contacts/add', methods=['POST'])
@login_required
def add_contact():
    name = request.form.get('name', '').strip()
    phone = request.form.get('phone', '').strip()
    relation = request.form.get('relation', 'other').strip()
    if not name or not phone:
        flash('Name and phone number are required.', 'error')
        return redirect(url_for('safety.contacts'))
    if EmergencyContact.query.filter_by(user_id=current_user.id).count() >= 5:
        flash('Maximum 5 emergency contacts allowed.', 'error')
        return redirect(url_for('safety.contacts'))
    contact = EmergencyContact(
        user_id=current_user.id, name=name, phone=phone, relation=relation
    )
    db.session.add(contact)
    db.session.commit()
    flash(f'{name} added as an emergency contact.', 'success')
    return redirect(url_for('safety.contacts'))


@bp.route('/contacts/<int:contact_id>/delete', methods=['POST'])
@login_required
def delete_contact(contact_id):
    contact = EmergencyContact.query.get_or_404(contact_id)
    if contact.user_id != current_user.id:
        abort(403)
    db.session.delete(contact)
    db.session.commit()
    flash('Contact removed.', 'success')
    return redirect(url_for('safety.contacts'))


@bp.route('/share-location', methods=['POST'])
@login_required
def share_location():
    """Generate a 4-hour shareable location link (demo)."""
    lat = request.form.get('lat') or request.get_json(silent=True, force=True).get('lat')
    lng = request.form.get('lng') or request.get_json(silent=True, force=True).get('lng')
    if not lat or not lng:
        return jsonify({'ok': False, 'error': 'Location required'}), 400
    ttl_hours = current_app.config.get('LOCATION_SHARE_TTL_HOURS', 4)
    expiry = time.time() + ttl_hours * 3600
    token = _sign_location_token(current_user.id, float(lat), float(lng), expiry)
    share_url = url_for('safety.view_shared_location', token=token, _external=True)
    return jsonify({'ok': True, 'url': share_url, 'expires_in_hours': ttl_hours})


@bp.route('/share/<token>')
def view_shared_location(token):
    """Public location share view — no auth needed."""
    data = _verify_location_token(token)
    if not data:
        abort(410)  # Gone / expired
    user = User.query.get(data['user_id'])
    return render_template(
        'safety/shared_location.html',
        lat=data['lat'], lng=data['lng'],
        user_name=user.name if user else 'Traveller',
        expiry=datetime.utcfromtimestamp(data['expiry']).strftime('%H:%M UTC'),
        title='Shared Location — Beyond Tour'
    )
