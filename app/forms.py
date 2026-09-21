from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, IntegerField, FloatField,
    TextAreaField, SelectField, SubmitField, DateField, HiddenField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, Optional, NumberRange
)


class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired(message='Please enter your email address.'),
        Email(message='Please provide a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password.')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    name = StringField('Full Name', validators=[
        DataRequired(message='Please provide your full name.'),
        Length(min=2, max=100, message='Name must be between 2 and 100 characters.')
    ])
    email = StringField('Email Address', validators=[
        DataRequired(message='Please provide your email address.'),
        Email(message='Please provide a valid email address.')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required.'),
        Length(min=6, message='Password must be at least 6 characters.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password.'),
        EqualTo('password', message='Passwords must match.')
    ])
    role = SelectField('Account Type', choices=[
        ('tourist', 'Traveler / Explorer'),
        ('business', 'Local Homestay Host or Guide')
    ], default='tourist')
    submit = SubmitField('Create Account')


class BookingRequestForm(FlaskForm):
    target_type = HiddenField('Target Type', validators=[DataRequired()])
    target_id = HiddenField('Target ID', validators=[DataRequired()])
    check_in = DateField('Check-in Date', validators=[DataRequired(message='Please select a start date.')])
    check_out = DateField('Check-out Date', validators=[Optional()])
    guests = IntegerField('Number of Travelers', default=1, validators=[
        DataRequired(),
        NumberRange(min=1, max=20, message='Guests must be between 1 and 20.')
    ])
    message = TextAreaField('Special Requests or Requirements', validators=[
        Optional(),
        Length(max=500, message='Message cannot exceed 500 characters.')
    ])
    submit = SubmitField('Send Booking Request')


class ReviewForm(FlaskForm):
    target_type = HiddenField('Target Type', validators=[DataRequired()])
    target_id = HiddenField('Target ID', validators=[DataRequired()])
    rating = IntegerField('Rating (1-5)', validators=[
        DataRequired(message='Please choose a rating from 1 to 5.'),
        NumberRange(min=1, max=5, message='Rating must be between 1 and 5.')
    ])
    comment = TextAreaField('Your Review & Story', validators=[
        DataRequired(message='Please write your feedback.'),
        Length(min=10, max=1000, message='Review must be between 10 and 1,000 characters.')
    ])
    submit = SubmitField('Submit Review')


class CommunityCommentForm(FlaskForm):
    post_id = HiddenField('Post ID', validators=[DataRequired()])
    content = TextAreaField('Write a comment', validators=[
        DataRequired(message='Comment cannot be empty.'),
        Length(min=2, max=500, message='Comment must be between 2 and 500 characters.')
    ])
    submit = SubmitField('Post Comment')


class VendorHotelForm(FlaskForm):
    name = StringField('Property / Homestay Name', validators=[
        DataRequired(message='Property name is required.'),
        Length(max=200)
    ])
    district = SelectField('District', choices=[
        ('Nainital', 'Nainital'),
        ('Almora', 'Almora'),
        ('Bageshwar', 'Bageshwar'),
        ('Pithoragarh', 'Pithoragarh'),
        ('Champawat', 'Champawat'),
        ('Chamoli', 'Chamoli'),
        ('Uttarkashi', 'Uttarkashi'),
        ('Dehradun', 'Dehradun & Rishikesh'),
        ('Haridwar', 'Haridwar'),
        ('Rudraprayag', 'Rudraprayag & Chopta'),
        ('Tehri Garhwal', 'Tehri Garhwal')
    ], validators=[DataRequired()])
    hotel_type = SelectField('Stay Category', choices=[
        ('homestay', 'Village Homestay'),
        ('hotel', 'Mountain Lodge or Hotel'),
        ('restaurant', 'Local Dining / Cafe')
    ], default='homestay')
    price_min = IntegerField('Starting Rate Per Night (INR)', validators=[
        DataRequired(message='Starting price is required.'),
        NumberRange(min=500, max=15000, message='Price must be between 500 and 15,000.')
    ])
    price_max = IntegerField('Peak Rate Per Night (INR)', validators=[
        DataRequired(message='Peak price is required.'),
        NumberRange(min=500, max=25000, message='Price must be between 500 and 25,000.')
    ])
    host_name = StringField('Host / Manager Name', validators=[
        DataRequired(message='Host name is required.'),
        Length(max=120)
    ])
    host_story = TextAreaField('Host Story & Heritage Description', validators=[
        Optional(),
        Length(max=1500)
    ])
    amenities = StringField('Amenities (comma-separated)', validators=[Optional()])
    cover_image_url = StringField('Primary Cover Photo URL', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Changes')


class VendorGuideForm(FlaskForm):
    name = StringField('Guide Full Name', validators=[
        DataRequired(message='Guide name is required.'),
        Length(max=120)
    ])
    district = SelectField('Home District', choices=[
        ('Nainital', 'Nainital'),
        ('Almora', 'Almora'),
        ('Bageshwar', 'Bageshwar'),
        ('Pithoragarh', 'Pithoragarh'),
        ('Champawat', 'Champawat'),
        ('Chamoli', 'Chamoli'),
        ('Uttarkashi', 'Uttarkashi'),
        ('Dehradun', 'Dehradun & Rishikesh'),
        ('Haridwar', 'Haridwar'),
        ('Rudraprayag', 'Rudraprayag & Chopta'),
        ('Tehri Garhwal', 'Tehri Garhwal')
    ], validators=[DataRequired()])
    districts_served = StringField('Districts Served (comma-separated)', validators=[Optional(), Length(max=200)])
    daily_rate = IntegerField('Daily Guiding Rate (INR)', validators=[
        DataRequired(message='Daily rate is required.'),
        NumberRange(min=500, max=10000, message='Rate must be between 500 and 10,000.')
    ])
    years_experience = IntegerField('Years of Experience', default=1, validators=[
        DataRequired(),
        NumberRange(min=1, max=50)
    ])
    languages = StringField('Languages Spoken (comma-separated)', validators=[Optional()])
    specialties = StringField('Specialties / Trek Routes (comma-separated)', validators=[Optional()])
    bio = TextAreaField('Guide Biography & Lore Knowledge', validators=[Optional(), Length(max=1500)])
    profile_image = StringField('Profile Photo URL', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Profile')


class AdminDestinationForm(FlaskForm):
    name = StringField('Destination Name', validators=[DataRequired(), Length(max=200)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=200)])
    region = SelectField('Region', choices=[('kumaon', 'Kumaon'), ('garhwal', 'Garhwal')], validators=[DataRequired()])
    district = SelectField('District', choices=[
        ('Nainital', 'Nainital'),
        ('Almora', 'Almora'),
        ('Bageshwar', 'Bageshwar'),
        ('Pithoragarh', 'Pithoragarh'),
        ('Champawat', 'Champawat'),
        ('Chamoli', 'Chamoli'),
        ('Uttarkashi', 'Uttarkashi'),
        ('Dehradun', 'Dehradun & Rishikesh'),
        ('Haridwar', 'Haridwar'),
        ('Rudraprayag', 'Rudraprayag & Chopta'),
        ('Tehri Garhwal', 'Tehri Garhwal')
    ], validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('temple', 'Temple & Sacred Shrine'),
        ('trek', 'High Altitude Trek'),
        ('lake', 'Lake & Waterbody'),
        ('heritage', 'Historic Fort & Architecture'),
        ('wildlife', 'Wildlife & Meadow')
    ], default='heritage')
    lat = FloatField('Latitude', validators=[Optional()])
    lng = FloatField('Longitude', validators=[Optional()])
    altitude_m = IntegerField('Altitude (meters)', validators=[Optional()])
    best_time = StringField('Best Time to Visit', validators=[Optional(), Length(max=200)])
    description = TextAreaField('Description & Historical Significance', validators=[DataRequired()])
    cover_image_url = StringField('Cover Image URL', validators=[Optional(), Length(max=500)])
    featured = BooleanField('Featured on Homepage')
    submit = SubmitField('Save Destination')


class AdminCultureForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    slug = StringField('Slug', validators=[Optional(), Length(max=150)])
    subtitle = StringField('Subtitle / Tagline', validators=[Optional(), Length(max=300)])
    entry_type = SelectField('Type', choices=[('festival', 'Festival / Mela'), ('art', 'Traditional Art & Craft')], default='festival')
    category = SelectField('Category', choices=[
        ('Religious', 'Religious'),
        ('Cultural', 'Cultural'),
        ('Harvest', 'Harvest'),
        ('Fair', 'Traditional Fair / Mela')
    ], default='Religious')
    district = SelectField('District', choices=[
        ('Nainital', 'Nainital'),
        ('Almora', 'Almora'),
        ('Bageshwar', 'Bageshwar'),
        ('Pithoragarh', 'Pithoragarh'),
        ('Champawat', 'Champawat'),
        ('Chamoli', 'Chamoli'),
        ('Uttarkashi', 'Uttarkashi'),
        ('Dehradun', 'Dehradun & Rishikesh'),
        ('Haridwar', 'Haridwar'),
        ('Rudraprayag', 'Rudraprayag & Chopta'),
        ('Tehri Garhwal', 'Tehri Garhwal')
    ], validators=[DataRequired()])
    venue = StringField('Venue / Sacred Shrine', validators=[Optional(), Length(max=200)])
    deity_or_ritual = StringField('Deity or Ritual', validators=[Optional(), Length(max=200)])
    when_celebrated = StringField('When Celebrated', validators=[Optional(), Length(max=200)])
    month_name = SelectField('Month Celebrated', choices=[
        ('', 'Select Month'),
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    ], default='')
    attendance = StringField('Estimated Attendance', validators=[Optional(), Length(max=150)])
    story_text = TextAreaField('Tradition & Folklore Story', validators=[DataRequired()])
    travel_tips = TextAreaField('Visitor Etiquette & Access Advice', validators=[Optional()])
    cover_image_url = StringField('Cover Image URL', validators=[Optional(), Length(max=500)])
    is_happening_soon = BooleanField('Happening Soon')
    unesco = BooleanField('UNESCO Recognized')
    gi_tag = BooleanField('GI Tag Protected')
    submit = SubmitField('Save Culture Entry')


class AdminFoodForm(FlaskForm):
    name = StringField('Dish Name', validators=[DataRequired(), Length(max=200)])
    region = SelectField('Region', choices=[('kumaon', 'Kumaon'), ('garhwal', 'Garhwal')], validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('main', 'Main Course Curry & Dal'),
        ('sweet', 'Traditional Sweet / Mithai'),
        ('snack', 'Snack & Chutney'),
        ('beverage', 'Himalayan Beverage')
    ], default='main')
    description = TextAreaField('Culinary Description & Story', validators=[DataRequired()])
    ingredients = TextAreaField('Key Local Ingredients', validators=[Optional()])
    where_to_try = StringField('Where to Savor', validators=[Optional(), Length(max=300)])
    image_url = StringField('Photo URL', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Food Item')


class SiteContentForm(FlaskForm):
    key = StringField('Setting Key', validators=[DataRequired(), Length(max=100)])
    value = TextAreaField('Content / Copy String', validators=[DataRequired()])
    description = StringField('Internal Purpose Description', validators=[Optional(), Length(max=255)])
    submit = SubmitField('Update Copy')
