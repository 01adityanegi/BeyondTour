from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db, login_manager


# ---------------------------------------------------------------------------
# Base Model for Type Checking & Declarative Support
# ---------------------------------------------------------------------------
class BaseModel(db.Model):
    __abstract__ = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------
class User(BaseModel, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='tourist')  # tourist | business | admin
    auth_provider = db.Column(db.String(20), default='local')
    avatar_url = db.Column(db.String(500))
    email_verified = db.Column(db.Boolean, default=False)
    bio = db.Column(db.Text)
    home_city = db.Column(db.String(100))
    interests = db.Column(db.Text)  # JSON or comma-separated string
    phone_number = db.Column(db.String(20))
    is_active_account = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    trips = db.relationship('Trip', backref='user', lazy='dynamic')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    wishlist_items = db.relationship('Wishlist', backref='user', lazy='dynamic')
    community_posts = db.relationship('CommunityPost', backref='user', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email}>'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------------------------------------------------------------------
# Destinations
# ---------------------------------------------------------------------------
class Destination(BaseModel):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True)
    region = db.Column(db.String(20))  # kumaon | garhwal
    category = db.Column(db.String(50))  # temple | trek | lake | heritage | wildlife
    district = db.Column(db.String(100))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    description = db.Column(db.Text)
    cover_image_url = db.Column(db.String(500))
    gallery_images = db.Column(db.Text)  # JSON array of URLs
    altitude_m = db.Column(db.Integer)
    best_time = db.Column(db.String(200))
    featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    hotels = db.relationship('Hotel', backref='destination', lazy='dynamic')
    reviews = db.relationship('Review',
                              primaryjoin="and_(Review.target_type=='destination', "
                                         "foreign(Review.target_id)==Destination.id)",
                              lazy='dynamic')


# ---------------------------------------------------------------------------
# Culture (Festivals & Art)
# ---------------------------------------------------------------------------
class CultureEntry(BaseModel):
    __tablename__ = 'culture_entries'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(150), unique=True, index=True)
    region = db.Column(db.String(20))        # kumaon | garhwal
    entry_type = db.Column(db.String(20))    # festival | art
    category = db.Column(db.String(50), default='Religious') # Religious | Cultural | Harvest | Fair
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300))
    district = db.Column(db.String(100))
    venue = db.Column(db.String(200))
    deity_or_ritual = db.Column(db.String(200))
    attendance = db.Column(db.String(150))   # e.g. "Est. 50,000+ devotees (illustrative estimate)"
    story_text = db.Column(db.Text)
    travel_tips = db.Column(db.Text)
    when_celebrated = db.Column(db.String(200))
    month_name = db.Column(db.String(50))    # January ... December
    month_number = db.Column(db.Integer)     # for sorting (1-12)
    is_happening_soon = db.Column(db.Boolean, default=False)
    cover_image_url = db.Column(db.String(500))
    gi_tag = db.Column(db.Boolean, default=False)
    unesco = db.Column(db.Boolean, default=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    video_url = db.Column(db.String(500))
    event_date = db.Column(db.String(100))
    guide_id = db.Column(db.Integer, db.ForeignKey('guides.id'), nullable=True)
    guide_name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'slug': self.slug or f'festival-{self.id}',
            'title': self.title,
            'subtitle': self.subtitle or '',
            'district': self.district or 'Uttarakhand',
            'region': self.region or 'kumaon',
            'category': self.category or 'Religious',
            'venue': self.venue or '',
            'deity_or_ritual': self.deity_or_ritual or '',
            'attendance': self.attendance or '',
            'story_text': self.story_text or '',
            'travel_tips': self.travel_tips or '',
            'when_celebrated': self.when_celebrated or '',
            'event_date': self.event_date or '',
            'month_name': self.month_name or '',
            'month_number': self.month_number or 1,
            'is_happening_soon': bool(self.is_happening_soon),
            'cover_image_url': self.cover_image_url or '',
            'video_url': self.video_url or '',
            'guide_id': self.guide_id,
            'guide_name': self.guide_name or '',
            'unesco': bool(self.unesco),
            'gi_tag': bool(self.gi_tag),
            'destination_id': self.destination_id
        }


# ---------------------------------------------------------------------------
# Food
# ---------------------------------------------------------------------------
class FoodItem(BaseModel):
    __tablename__ = 'food_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    region = db.Column(db.String(20))
    category = db.Column(db.String(50))  # main | sweet | snack | beverage
    description = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    where_to_try = db.Column(db.String(300))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))


# ---------------------------------------------------------------------------
# Hotels & Homestays
# ---------------------------------------------------------------------------
class Hotel(BaseModel):
    __tablename__ = 'hotels'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(200), nullable=False)
    hotel_type = db.Column(db.String(20), default='homestay')  # hotel | homestay
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    district = db.Column(db.String(100))
    price_min = db.Column(db.Integer)
    price_max = db.Column(db.Integer)
    amenities = db.Column(db.Text)       # JSON array
    images = db.Column(db.Text)          # JSON array
    cover_image_url = db.Column(db.String(500))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    host_story = db.Column(db.Text)
    host_name = db.Column(db.String(120))
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    featured = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(30), default='live')  # live | pending | changes_requested
    admin_note = db.Column(db.Text)
    # ID Verification (Safety Module)
    id_document_url = db.Column(db.String(500))   # Private/signed Cloudinary URL
    verification_status = db.Column(db.String(20), default='unverified')  # unverified | pending | verified
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Guides
# ---------------------------------------------------------------------------
class Guide(BaseModel):
    __tablename__ = 'guides'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(120), nullable=False)
    specialties = db.Column(db.Text)   # JSON array
    languages = db.Column(db.Text)     # JSON array
    bio = db.Column(db.Text)
    daily_rate = db.Column(db.Integer)
    region = db.Column(db.String(20))
    district = db.Column(db.String(100))
    districts_served = db.Column(db.String(200))
    profile_image = db.Column(db.String(500))
    gallery_images = db.Column(db.Text)  # JSON array of URLs
    availability_dates = db.Column(db.Text)  # JSON array of booked ISO dates
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    verified = db.Column(db.Boolean, default=False)
    years_experience = db.Column(db.Integer, default=1)
    status = db.Column(db.String(30), default='live')  # live | pending | changes_requested
    admin_note = db.Column(db.Text)
    # ID Verification (Safety Module)
    id_document_url = db.Column(db.String(500))   # Private/signed Cloudinary URL
    verification_status = db.Column(db.String(20), default='unverified')  # unverified | pending | verified


# ---------------------------------------------------------------------------
# Trips (AI-generated itineraries)
# ---------------------------------------------------------------------------
class Trip(BaseModel):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(300))
    itinerary_json = db.Column(db.Text)  # Gemini-generated JSON
    days = db.Column(db.Integer)
    budget = db.Column(db.Integer)
    group_type = db.Column(db.String(30))
    interests = db.Column(db.Text)        # JSON array
    start_city = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='draft')  # draft | confirmed | completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Reviews
# ---------------------------------------------------------------------------
class Review(BaseModel):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_type = db.Column(db.String(30))  # destination | hotel | guide
    target_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)  # 1-5
    comment = db.Column(db.Text)
    images = db.Column(db.Text)  # JSON array
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Wishlist
# ---------------------------------------------------------------------------
class Wishlist(BaseModel):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_type = db.Column(db.String(30))
    target_id = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Community Posts
# ---------------------------------------------------------------------------
class CommunityPost(BaseModel):
    __tablename__ = 'community_posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    media_type = db.Column(db.String(30), default='photo')  # photo | video | youtube | youtube_shorts | instagram
    media_url = db.Column(db.String(500))                  # URL for video or Instagram post/reel
    images = db.Column(db.Text)                            # JSON array of photo URLs
    district_tag = db.Column(db.String(100))               # e.g. Nainital, Almora
    destination_tag = db.Column(db.String(200))
    instagram_shortcode = db.Column(db.String(100))
    youtube_id = db.Column(db.String(100))                 # YouTube video or Shorts ID
    video_format = db.Column(db.String(20), default='16:9') # '16:9' (YouTube Video) | '9:16' (YouTube Shorts)
    aspect_ratio = db.Column(db.String(20), default='4:5') # '4:5' (Instagram Portrait) | '1:1' (Instagram Square) | '16:9' | '9:16'
    likes_count = db.Column(db.Integer, default=0)
    is_hidden = db.Column(db.Boolean, default=False)
    is_flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    @property
    def thumbnail_url(self):
        if self.youtube_id:
            return f"https://img.youtube.com/vi/{self.youtube_id}/hqdefault.jpg"
        if self.images:
            try:
                import json as _json
                imgs = _json.loads(self.images)
                if imgs and isinstance(imgs, list) and len(imgs) > 0 and imgs[0]:
                    return imgs[0]
            except Exception:
                pass
        if self.media_url and any(self.media_url.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.webp', '.avif')):
            return self.media_url
        district_thumbs = {
            'nainital': '/static/images/Nanital/lakenanital.png',
            'almora': '/static/images/destinations/binsar.jpg',
            'pithoragarh': '/static/images/destinations/munsiyari.jpg',
            'uttarkashi': '/static/images/destinations/rishikesh.jpg',
        }
        tag = (self.district_tag or 'nainital').lower()
        for k, v in district_thumbs.items():
            if k in tag:
                return v
        return '/static/images/Nanital/lakenanital.png'


class Comment(BaseModel):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    content = db.Column(db.Text, nullable=False)
    is_hidden = db.Column(db.Boolean, default=False)
    is_flagged = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='user_comments')


class PostLike(BaseModel):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('community_posts.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'post_id', name='uq_user_post_like'),)


# ---------------------------------------------------------------------------
# Bookings
# ---------------------------------------------------------------------------
class Booking(BaseModel):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    target_type = db.Column(db.String(20))  # hotel | guide
    target_id = db.Column(db.Integer)
    check_in = db.Column(db.Date)
    check_out = db.Column(db.Date)
    guests = db.Column(db.Integer, default=1)
    total_amount = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')  # pending | confirmed | cancelled
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------------------------------
# Site Content (Editable copy strings for non-technical tourism board staff)
# ---------------------------------------------------------------------------
class SiteContent(BaseModel):
    __tablename__ = 'site_content'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ---------------------------------------------------------------------------
# Audit Logs (Accountability and governance tracking)
# ---------------------------------------------------------------------------
class AuditLog(BaseModel):
    __tablename__ = 'audit_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(50), nullable=False) # create | update | delete | approve | request_changes | hide | restore | sos_trigger | id_verify
    target_type = db.Column(db.String(50), nullable=False) # destination | culture | food | hotel | guide | post | comment | site_content | sos | verification
    target_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='audit_logs')


# ===========================================================================
# NEW TABLES — Weather, Crowd, Safety, Fair-Price (BeyondTour SIH 2024)
# ===========================================================================

# ---------------------------------------------------------------------------
# Weather Cache — stores OpenWeatherMap One Call API responses
# ---------------------------------------------------------------------------
class WeatherCache(BaseModel):
    __tablename__ = 'weather_cache'
    id = db.Column(db.Integer, primary_key=True)
    location_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    forecast_json = db.Column(db.Text, nullable=False)   # Full OWM One Call response
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<WeatherCache {self.location_key}>'


# ---------------------------------------------------------------------------
# Destination Baseline — admin-curated seasonality crowd tiers
# ---------------------------------------------------------------------------
class DestinationBaseline(BaseModel):
    __tablename__ = 'destination_baselines'
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    month = db.Column(db.Integer, nullable=False)           # 1–12
    day_type = db.Column(db.String(10), nullable=False)     # weekday | weekend
    expected_tier = db.Column(db.Integer, nullable=False)   # 1 (very quiet) to 5 (very crowded)

    destination = db.relationship('Destination', backref='baselines')

    __table_args__ = (
        db.UniqueConstraint('destination_id', 'month', 'day_type',
                            name='uq_dest_month_daytype'),
    )


# ---------------------------------------------------------------------------
# Crowd Signals — real-time community check-in signals
# ---------------------------------------------------------------------------
class CrowdSignal(BaseModel):
    __tablename__ = 'crowd_signals'
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    source = db.Column(db.String(30), default='community_post')  # community_post | check_in | manual
    weight = db.Column(db.Float, default=1.0)

    destination = db.relationship('Destination', backref='crowd_signals')


# ---------------------------------------------------------------------------
# Emergency Contacts — user's saved contacts for SOS alerts
# ---------------------------------------------------------------------------
class EmergencyContact(BaseModel):
    __tablename__ = 'emergency_contacts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    relation = db.Column(db.String(50))   # parent | spouse | friend | sibling | other

    user = db.relationship('User', backref='emergency_contacts')


# ---------------------------------------------------------------------------
# SOS Alerts — physical safety distress triggers
# ---------------------------------------------------------------------------
class SosAlert(BaseModel):
    __tablename__ = 'sos_alerts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    district = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default='active')   # active | resolved | false_alarm
    resolved_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    resolved_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)

    user = db.relationship('User', foreign_keys=[user_id], backref='sos_alerts')
    resolver = db.relationship('User', foreign_keys=[resolved_by])


# ---------------------------------------------------------------------------
# Price Bands — computed fair-price ranges per category/district
# ---------------------------------------------------------------------------
class PriceBand(BaseModel):
    __tablename__ = 'price_bands'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30), nullable=False)    # hotel | guide | taxi
    district = db.Column(db.String(100), nullable=False)
    median_price = db.Column(db.Float)
    iqr_low = db.Column(db.Float)    # lower fence: Q1 - 1.5×IQR
    iqr_high = db.Column(db.Float)   # upper fence: Q3 + 1.5×IQR
    sample_count = db.Column(db.Integer, default=0)
    computed_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('category', 'district', name='uq_pricebands_cat_district'),
    )
