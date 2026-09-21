import re
from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import current_user
from app.extensions import db
from app.blueprints.admin import bp
from app.models import (
    User, Destination, CultureEntry, FoodItem, Hotel, Guide,
    CommunityPost, Comment, AuditLog, SiteContent, Booking, Review, Wishlist
)
from app.forms import (
    AdminDestinationForm, AdminCultureForm, AdminFoodForm, SiteContentForm
)


KUMAON_DISTRICTS = {'almora', 'nainital', 'pithoragarh', 'bageshwar', 'champawat', 'udham singh nagar'}


def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text.lower()).strip()
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
    except Exception as e:
        db.session.rollback()


# ---------------------------------------------------------------------------
# Dashboard Overview
# ---------------------------------------------------------------------------
@bp.route('/')
def index():
    pending_hotels_count = Hotel.query.filter_by(status='pending').count()
    pending_guides_count = Guide.query.filter_by(status='pending').count()
    flagged_posts_count = CommunityPost.query.filter_by(is_flagged=True).count()
    total_live_hotels = Hotel.query.filter_by(status='live').count()
    total_live_guides = Guide.query.filter_by(status='live').count()
    total_destinations = Destination.query.count()
    total_culture = CultureEntry.query.count()

    recent_logs = AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8).all()
    pending_hotels = Hotel.query.filter_by(status='pending').order_by(Hotel.created_at.desc()).limit(5).all()
    flagged_posts = CommunityPost.query.filter_by(is_flagged=True).order_by(CommunityPost.created_at.desc()).limit(5).all()

    return render_template(
        'admin/index.html',
        pending_hotels_count=pending_hotels_count,
        pending_guides_count=pending_guides_count,
        flagged_posts_count=flagged_posts_count,
        total_live_hotels=total_live_hotels,
        total_live_guides=total_live_guides,
        total_destinations=total_destinations,
        total_culture=total_culture,
        recent_logs=recent_logs,
        pending_hotels=pending_hotels,
        flagged_posts=flagged_posts,
        title='Administration Overview — Beyond Tour'
    )


# ---------------------------------------------------------------------------
# Destinations Management
# ---------------------------------------------------------------------------
@bp.route('/destinations')
def destinations():
    q = request.args.get('q', '').strip()
    query = Destination.query
    if q:
        query = query.filter(
            db.or_(
                Destination.name.ilike(f'%{q}%'),
                Destination.district.ilike(f'%{q}%'),
                Destination.region.ilike(f'%{q}%')
            )
        )
    items = query.order_by(Destination.name.asc()).all()
    return render_template('admin/destinations.html', destinations=items, query=q, title='Destinations — Admin')


@bp.route('/destinations/new', methods=['GET', 'POST'])
def destination_new():
    form = AdminDestinationForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip() if form.slug.data else slugify(form.name.data)
        existing = Destination.query.filter_by(slug=slug).first()
        if existing:
            slug = f"{slug}-{int(datetime.utcnow().timestamp())}"

        dest = Destination(
            name=form.name.data.strip(),
            slug=slug,
            region=form.region.data,
            district=form.district.data,
            category=form.category.data,
            lat=form.lat.data,
            lng=form.lng.data,
            altitude_m=form.altitude_m.data,
            best_time=form.best_time.data,
            description=form.description.data,
            cover_image_url=form.cover_image_url.data,
            featured=form.featured.data
        )
        db.session.add(dest)
        db.session.commit()
        log_audit('create', 'destination', dest.id, f"Created destination {dest.name}")
        flash(f"Destination '{dest.name}' created successfully.", 'success')
        return redirect(url_for('admin.destinations'))

    return render_template('admin/destination_form.html', form=form, destination=None, title='New Destination — Admin')


@bp.route('/destinations/<int:dest_id>/edit', methods=['GET', 'POST'])
def destination_edit(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    form = AdminDestinationForm(obj=dest)
    if form.validate_on_submit():
        form.populate_obj(dest)
        db.session.commit()
        log_audit('update', 'destination', dest.id, f"Updated destination {dest.name}")
        flash(f"Destination '{dest.name}' updated successfully.", 'success')
        return redirect(url_for('admin.destinations'))

    return render_template('admin/destination_form.html', form=form, destination=dest, title=f'Edit {dest.name} — Admin')


@bp.route('/destinations/<int:dest_id>/delete', methods=['POST'])
def destination_delete(dest_id):
    dest = Destination.query.get_or_404(dest_id)
    name = dest.name
    db.session.delete(dest)
    db.session.commit()
    log_audit('delete', 'destination', dest_id, f"Deleted destination {name}")
    flash(f"Destination '{name}' deleted.", 'info')
    return redirect(url_for('admin.destinations'))


# ---------------------------------------------------------------------------
# Culture & Festivals Management
# ---------------------------------------------------------------------------
@bp.route('/culture')
def culture():
    q = request.args.get('q', '').strip()
    entry_type = request.args.get('type', 'all').strip()
    query = CultureEntry.query
    if q:
        query = query.filter(
            db.or_(
                CultureEntry.title.ilike(f'%{q}%'),
                CultureEntry.district.ilike(f'%{q}%'),
                CultureEntry.venue.ilike(f'%{q}%')
            )
        )
    if entry_type != 'all':
        query = query.filter_by(entry_type=entry_type)

    items = query.order_by(CultureEntry.month_number.asc(), CultureEntry.title.asc()).all()
    return render_template('admin/culture.html', culture_entries=items, query=q, entry_type=entry_type, title='Culture & Festivals — Admin')


@bp.route('/culture/new', methods=['GET', 'POST'])
def culture_new():
    form = AdminCultureForm()
    if form.validate_on_submit():
        slug = form.slug.data.strip() if form.slug.data else slugify(form.title.data)
        # Auto-derive region based on district
        district_val = (form.district.data or '').lower().strip()
        region_derived = 'kumaon' if district_val in KUMAON_DISTRICTS else 'garhwal'

        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        month_num = month_map.get(form.month_name.data, 1)

        entry = CultureEntry(
            title=form.title.data.strip(),
            slug=slug,
            subtitle=form.subtitle.data,
            entry_type=form.entry_type.data,
            category=form.category.data,
            region=region_derived,
            district=form.district.data,
            venue=form.venue.data,
            deity_or_ritual=form.deity_or_ritual.data,
            when_celebrated=form.when_celebrated.data,
            month_name=form.month_name.data or None,
            month_number=month_num,
            attendance=form.attendance.data,
            story_text=form.story_text.data,
            travel_tips=form.travel_tips.data,
            cover_image_url=form.cover_image_url.data,
            is_happening_soon=form.is_happening_soon.data,
            unesco=form.unesco.data,
            gi_tag=form.gi_tag.data
        )
        db.session.add(entry)
        db.session.commit()
        log_audit('create', 'culture', entry.id, f"Created culture entry {entry.title} ({region_derived})")
        flash(f"Culture entry '{entry.title}' created successfully.", 'success')
        return redirect(url_for('admin.culture'))

    return render_template('admin/culture_form.html', form=form, entry=None, title='New Culture Entry — Admin')


@bp.route('/culture/<int:entry_id>/edit', methods=['GET', 'POST'])
def culture_edit(entry_id):
    entry = CultureEntry.query.get_or_404(entry_id)
    form = AdminCultureForm(obj=entry)
    if form.validate_on_submit():
        form.populate_obj(entry)
        district_val = (entry.district or '').lower().strip()
        entry.region = 'kumaon' if district_val in KUMAON_DISTRICTS else 'garhwal'
        month_map = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        if form.month_name.data:
            entry.month_number = month_map.get(form.month_name.data, entry.month_number)
        db.session.commit()
        log_audit('update', 'culture', entry.id, f"Updated culture entry {entry.title}")
        flash(f"Culture entry '{entry.title}' updated successfully.", 'success')
        return redirect(url_for('admin.culture'))

    return render_template('admin/culture_form.html', form=form, entry=entry, title=f'Edit {entry.title} — Admin')


@bp.route('/culture/<int:entry_id>/delete', methods=['POST'])
def culture_delete(entry_id):
    entry = CultureEntry.query.get_or_404(entry_id)
    title = entry.title
    db.session.delete(entry)
    db.session.commit()
    log_audit('delete', 'culture', entry_id, f"Deleted culture entry {title}")
    flash(f"Culture entry '{title}' deleted.", 'info')
    return redirect(url_for('admin.culture'))


# ---------------------------------------------------------------------------
# Local Food Management
# ---------------------------------------------------------------------------
@bp.route('/food')
def food():
    region = request.args.get('region', 'all').strip().lower()
    query = FoodItem.query
    if region in ('kumaon', 'garhwal'):
        query = query.filter_by(region=region)
    foods = query.order_by(FoodItem.name.asc()).all()
    return render_template('admin/food.html', foods=foods, region=region, title='Local Food Items — Admin')


@bp.route('/food/new', methods=['GET', 'POST'])
def food_new():
    form = AdminFoodForm()
    if form.validate_on_submit():
        item = FoodItem(
            name=form.name.data.strip(),
            region=form.region.data,
            category=form.category.data,
            description=form.description.data,
            ingredients=form.ingredients.data,
            where_to_try=form.where_to_try.data,
            image_url=form.image_url.data
        )
        db.session.add(item)
        db.session.commit()
        log_audit('create', 'food', item.id, f"Created food item {item.name}")
        flash(f"Food item '{item.name}' created successfully.", 'success')
        return redirect(url_for('admin.food'))

    return render_template('admin/food_form.html', form=form, food=None, title='New Food Item — Admin')


@bp.route('/food/<int:food_id>/edit', methods=['GET', 'POST'])
def food_edit(food_id):
    item = FoodItem.query.get_or_404(food_id)
    form = AdminFoodForm(obj=item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.commit()
        log_audit('update', 'food', item.id, f"Updated food item {item.name}")
        flash(f"Food item '{item.name}' updated successfully.", 'success')
        return redirect(url_for('admin.food'))

    return render_template('admin/food_form.html', form=form, food=item, title=f'Edit {item.name} — Admin')


@bp.route('/food/<int:food_id>/delete', methods=['POST'])
def food_delete(food_id):
    item = FoodItem.query.get_or_404(food_id)
    name = item.name
    db.session.delete(item)
    db.session.commit()
    log_audit('delete', 'food', food_id, f"Deleted food item {name}")
    flash(f"Food item '{name}' deleted.", 'info')
    return redirect(url_for('admin.food'))


# ---------------------------------------------------------------------------
# Hotels & Homestays Approval Queue
# ---------------------------------------------------------------------------
@bp.route('/hotels')
def hotels():
    status_filter = request.args.get('status', 'all').strip()
    query = Hotel.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    hotel_list = query.order_by(Hotel.created_at.desc()).all()
    return render_template(
        'admin/hotels.html',
        hotels=hotel_list,
        status_filter=status_filter,
        title='Hotels & Homestays Approval — Admin'
    )


@bp.route('/hotels/<int:hotel_id>/approve', methods=['POST'])
def hotel_approve(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    hotel.status = 'live'
    hotel.admin_note = None
    db.session.commit()
    log_audit('approve', 'hotel', hotel.id, f"Approved hotel {hotel.name} to live status")
    if request.headers.get('HX-Request'):
        return render_template('admin/_hotel_status_cell.html', hotel=hotel)
    flash(f"Hotel '{hotel.name}' has been approved and is now live.", 'success')
    return redirect(request.referrer or url_for('admin.hotels'))


@bp.route('/hotels/<int:hotel_id>/request-changes', methods=['POST'])
def hotel_request_changes(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    note = request.form.get('admin_note', '').strip()
    hotel.status = 'changes_requested'
    hotel.admin_note = note if note else 'Please verify your pricing and license information.'
    db.session.commit()
    log_audit('request_changes', 'hotel', hotel.id, f"Requested changes on hotel {hotel.name}: {hotel.admin_note}")
    if request.headers.get('HX-Request'):
        return render_template('admin/_hotel_status_cell.html', hotel=hotel)
    flash(f"Changes requested for '{hotel.name}'. Vendor has been notified.", 'warning')
    return redirect(request.referrer or url_for('admin.hotels'))


@bp.route('/hotels/<int:hotel_id>/delete', methods=['POST'])
def hotel_delete(hotel_id):
    hotel = Hotel.query.get_or_404(hotel_id)
    name = hotel.name

    # Clean up associated reviews, wishlists, and bookings
    Review.query.filter_by(target_type='hotel', target_id=hotel_id).delete()
    Wishlist.query.filter_by(target_type='hotel', target_id=hotel_id).delete()
    Booking.query.filter_by(target_type='hotel', target_id=hotel_id).delete()

    db.session.delete(hotel)
    db.session.commit()

    log_audit('delete', 'hotel', hotel_id, f"Permanently deleted stay '{name}' from platform")

    if request.headers.get('HX-Request'):
        return '', 200

    flash(f"Stay '{name}' has been permanently deleted from the site.", 'info')
    return redirect(request.referrer or url_for('admin.hotels'))


# ---------------------------------------------------------------------------
# Guides Approval Queue
# ---------------------------------------------------------------------------
@bp.route('/guides')
def guides():
    status_filter = request.args.get('status', 'all').strip()
    query = Guide.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    guide_list = query.order_by(Guide.id.desc()).all()
    return render_template(
        'admin/guides.html',
        guides=guide_list,
        status_filter=status_filter,
        title='Local Guides Approval — Admin'
    )


@bp.route('/guides/<int:guide_id>/approve', methods=['POST'])
def guide_approve(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    guide.status = 'live'
    guide.admin_note = None
    db.session.commit()
    log_audit('approve', 'guide', guide.id, f"Approved guide {guide.name} to live status")
    if request.headers.get('HX-Request'):
        return render_template('admin/_guide_status_cell.html', guide=guide)
    flash(f"Guide '{guide.name}' has been approved.", 'success')
    return redirect(request.referrer or url_for('admin.guides'))


@bp.route('/guides/<int:guide_id>/request-changes', methods=['POST'])
def guide_request_changes(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    note = request.form.get('admin_note', '').strip()
    guide.status = 'changes_requested'
    guide.admin_note = note if note else 'Please update your guide license and emergency certification.'
    db.session.commit()
    log_audit('request_changes', 'guide', guide.id, f"Requested changes for guide {guide.name}: {guide.admin_note}")
    if request.headers.get('HX-Request'):
        return render_template('admin/_guide_status_cell.html', guide=guide)
    flash(f"Changes requested for guide '{guide.name}'.", 'warning')
    return redirect(request.referrer or url_for('admin.guides'))


@bp.route('/guides/<int:guide_id>/toggle-verified', methods=['POST'])
def guide_toggle_verified(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    guide.verified = not guide.verified
    db.session.commit()
    status_str = 'verified' if guide.verified else 'unverified'
    log_audit('update', 'guide', guide.id, f"Set guide {guide.name} as {status_str}")
    if request.headers.get('HX-Request'):
        return render_template('admin/_guide_status_cell.html', guide=guide)
    flash(f"Guide '{guide.name}' is now {status_str}.", 'info')
    return redirect(request.referrer or url_for('admin.guides'))


@bp.route('/guides/<int:guide_id>/delete', methods=['POST'])
def guide_delete(guide_id):
    guide = Guide.query.get_or_404(guide_id)
    name = guide.name

    # Unlink any culture entries created by this guide so cultural content remains intact
    CultureEntry.query.filter_by(guide_id=guide_id).update({
        'guide_id': None,
        'guide_name': f"{name} (Past Guide)"
    })

    # Clean up associated reviews, wishlists, and bookings
    Review.query.filter_by(target_type='guide', target_id=guide_id).delete()
    Wishlist.query.filter_by(target_type='guide', target_id=guide_id).delete()
    Booking.query.filter_by(target_type='guide', target_id=guide_id).delete()

    db.session.delete(guide)
    db.session.commit()

    log_audit('delete', 'guide', guide_id, f"Permanently deleted guide '{name}' from platform")

    if request.headers.get('HX-Request'):
        return '', 200

    flash(f"Guide '{name}' has been permanently deleted from the site.", 'info')
    return redirect(request.referrer or url_for('admin.guides'))


# ---------------------------------------------------------------------------
# Community Moderation Queue
# ---------------------------------------------------------------------------
@bp.route('/community')
def community():
    filter_mode = request.args.get('filter', 'all').strip()
    query = CommunityPost.query
    if filter_mode == 'flagged':
        query = query.filter_by(is_flagged=True)
    posts = query.order_by(CommunityPost.created_at.desc()).all()
    return render_template(
        'admin/community.html',
        posts=posts,
        filter_mode=filter_mode,
        title='Community Content Moderation — Admin'
    )


@bp.route('/community/post/<int:post_id>/toggle-hidden', methods=['POST'])
def community_toggle_hidden(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    post.is_hidden = not post.is_hidden
    db.session.commit()
    state = 'hidden' if post.is_hidden else 'restored'
    log_audit('hide' if post.is_hidden else 'restore', 'community_post', post.id, f"{state.capitalize()} post #{post.id}")
    if request.headers.get('HX-Request'):
        return render_template('admin/_community_post_row.html', post=post)
    flash(f"Post #{post.id} has been {state}.", 'info')
    return redirect(request.referrer or url_for('admin.community'))


@bp.route('/community/post/<int:post_id>/unflag', methods=['POST'])
def community_unflag(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    post.is_flagged = False
    db.session.commit()
    log_audit('unflag', 'community_post', post.id, f"Dismissed flags on post #{post.id}")
    if request.headers.get('HX-Request'):
        return render_template('admin/_community_post_row.html', post=post)
    flash(f"Flags cleared for post #{post.id}.", 'success')
    return redirect(request.referrer or url_for('admin.community'))


# ---------------------------------------------------------------------------
# Festival Calendar Timeline
# ---------------------------------------------------------------------------
@bp.route('/calendar')
def calendar():
    entries = CultureEntry.query.filter_by(entry_type='festival').order_by(CultureEntry.month_number.asc()).all()
    months_data = {}
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    for idx, name in enumerate(month_names, start=1):
        months_data[name] = [e for e in entries if e.month_number == idx or e.month_name == name]

    return render_template(
        'admin/calendar.html',
        months_data=months_data,
        month_names=month_names,
        title='Himalayan Festival Calendar — Admin'
    )


# ---------------------------------------------------------------------------
# Site Content Editable Strings
# ---------------------------------------------------------------------------
DEFAULT_STRINGS = [
    ('hero_tagline', 'Go Beyond the Guidebook: Authentic Uttarakhand', 'Hero banner headline on the homepage'),
    ('hero_subtitle', 'Curated Himalayan journeys across Kumaon & Garhwal — authentic cultural immersion, verified homestays, and sacred festivals.', 'Hero banner secondary description'),
    ('culture_badge', 'GI-Tagged Living Himalayan Crafts & Sacred Fairs', 'Pill badge over Culture index header'),
    ('vendor_commission_notice', '100% Direct Village Support · 0% Commission Platform', 'Artisan and homestay direct cooperative banner note')
]


@bp.route('/site-content')
def site_content():
    # Seed default strings if empty
    for key, val, desc in DEFAULT_STRINGS:
        if not SiteContent.query.filter_by(key=key).first():
            db.session.add(SiteContent(key=key, value=val, description=desc))
    db.session.commit()

    items = SiteContent.query.order_by(SiteContent.key.asc()).all()
    form = SiteContentForm()
    return render_template('admin/site_content.html', items=items, form=form, title='Site Copy Strings — Admin')


@bp.route('/site-content/update', methods=['POST'])
def site_content_update():
    form = SiteContentForm()
    if form.validate_on_submit():
        item = SiteContent.query.filter_by(key=form.key.data).first()
        if not item:
            item = SiteContent(key=form.key.data)
            db.session.add(item)
        item.value = form.value.data
        if form.description.data:
            item.description = form.description.data
        db.session.commit()
        log_audit('update', 'site_content', item.id, f"Updated site copy for key '{item.key}'")
        flash(f"Copy string for '{item.key}' saved.", 'success')
    else:
        flash("Failed to update copy string. Please check required fields.", 'danger')
    return redirect(url_for('admin.site_content'))


# ---------------------------------------------------------------------------
# Audit Log History
# ---------------------------------------------------------------------------
@bp.route('/audit-log')
def audit_log():
    page = request.args.get('page', 1, type=int)
    logs = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=25)
    return render_template('admin/audit_log.html', logs=logs, title='Audit Trail & System Logs — Admin')
