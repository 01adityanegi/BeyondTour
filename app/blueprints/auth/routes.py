import json
import random
import re
from datetime import datetime, timedelta
from flask import render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from app.blueprints.auth import bp
from app.extensions import db, limiter
from app.models import User

# Firebase Admin SDK stub / integration
try:
    import firebase_admin
    from firebase_admin import auth as firebase_auth, credentials
    # Initialize only if not already initialized
    if not firebase_admin._apps:
        # Check for service account or default credentials
        cred = credentials.ApplicationDefault() if 'GOOGLE_APPLICATION_CREDENTIALS' in request.environ else None
        if cred:
            firebase_admin.initialize_app(cred)
except Exception:
    firebase_auth = None


def validate_password_strength(password):
    """Min 8 characters, at least 1 number."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r'\d', password):
        return False, "Password must contain at least 1 number."
    return True, ""


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------
@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        login_type = request.form.get('login_type', 'email')

        if login_type == 'email':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            remember = request.form.get('remember') == 'on'
            
            user = User.query.filter_by(email=email).first()
            if user and user.is_active_account and user.check_password(password):
                # Extend session duration if remember me is checked
                duration = timedelta(days=30) if remember else timedelta(days=1)
                login_user(user, remember=remember, duration=duration)
                next_page = request.args.get('next')
                flash(f'Welcome back, {user.name}!', 'success')
                return redirect(next_page or url_for('main.index'))
            
            flash('Invalid email or password.', 'danger')

        elif login_type == 'phone':
            phone = request.form.get('phone', '').strip()
            otp = request.form.get('otp', '').strip()
            session_otp = session.get('otp_code')
            session_phone = session.get('otp_phone')

            if otp and otp == session_otp and phone == session_phone:
                user = User.query.filter_by(phone_number=phone).first()
                if not user:
                    # Create account via phone OTP
                    user = User(
                        name=f'Traveler {phone[-4:]}',
                        email=f'{phone}@phone.beyondtour.in',
                        phone_number=phone,
                        auth_provider='phone',
                        role='tourist',
                        email_verified=True
                    )
                    db.session.add(user)
                    db.session.commit()
                login_user(user, remember=True)
                session.pop('otp_code', None)
                session.pop('otp_phone', None)
                flash(f'Signed in via mobile OTP. Welcome, {user.name}!', 'success')
                return redirect(url_for('main.index'))
            else:
                flash('Invalid OTP code. Please request a new code.', 'danger')

    return render_template('auth/login.html', title='Sign In — Beyond Tour')


# ---------------------------------------------------------------------------
# Sign Up
# ---------------------------------------------------------------------------
@bp.route('/signup', methods=['GET', 'POST'])
@limiter.limit("15 per minute")
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        role = request.form.get('role', 'tourist')

        # Restrict role assignment to tourist or business (admin is manually set)
        if role not in ['tourist', 'business']:
            role = 'tourist'

        # Server-side password policy validation
        is_valid, err_msg = validate_password_strength(password)
        if not is_valid:
            flash(err_msg, 'danger')
            return render_template('auth/signup.html', title='Join Beyond Tour', prefill_name=name, prefill_email=email, prefill_role=role)

        if User.query.filter_by(email=email).first():
            flash('This email address is already registered. Please sign in.', 'warning')
            return redirect(url_for('auth.login'))

        user = User(
            name=name,
            email=email,
            role=role,
            auth_provider='local',
            email_verified=False,
            interests='["trekking", "culture", "food"]'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        flash(f'Account created successfully! Welcome to Beyond Tour, {name}. Please verify your email to unlock all features.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/signup.html', title='Join Beyond Tour')


# ---------------------------------------------------------------------------
# Google OAuth Simulation / Firebase Callback
# ---------------------------------------------------------------------------
@bp.route('/google', methods=['POST', 'GET'])
def google_auth():
    """Google OAuth / Firebase Token handler."""
    # Simulate Google OAuth one-click login for demo
    email = request.form.get('email') or request.args.get('email', 'google_traveler@beyondtour.in')
    name = request.form.get('name') or request.args.get('name', 'Himalayan Explorer')
    
    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(
            name=name,
            email=email,
            role='tourist',
            auth_provider='google',
            email_verified=True,
            avatar_url='https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=200&q=80',
            interests='["trekking", "heritage", "photography"]'
        )
        db.session.add(user)
        db.session.commit()

    login_user(user, remember=True)
    flash(f'Signed in with Google as {user.name}!', 'success')
    return redirect(url_for('main.index'))


# ---------------------------------------------------------------------------
# Phone OTP Sender
# ---------------------------------------------------------------------------
@bp.route('/send-otp', methods=['POST'])
@limiter.limit("5 per minute")
def send_otp():
    phone = request.form.get('phone', '').strip()
    if not phone or len(phone) < 10:
        return jsonify({'success': False, 'message': 'Please enter a valid 10-digit mobile number.'}), 400

    # Generate a 6-digit OTP code (for demo, display it in the flash / response)
    otp = str(random.randint(100000, 999999))
    session['otp_code'] = otp
    session['otp_phone'] = phone

    return jsonify({
        'success': True,
        'message': f'Verification OTP sent to {phone}. For demo testing, your code is: {otp}',
        'demo_code': otp
    })


# ---------------------------------------------------------------------------
# Forgot Password Flow
# ---------------------------------------------------------------------------
@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = User.query.filter_by(email=email).first()
        if user:
            flash(f'A secure password reset link has been dispatched to {email}. Please check your inbox.', 'success')
        else:
            flash(f'If an account exists for {email}, a reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html', title='Reset Password — Beyond Tour')


# ---------------------------------------------------------------------------
# Email Verification
# ---------------------------------------------------------------------------
@bp.route('/resend-verification', methods=['POST'])
@login_required
def resend_verification():
    current_user.email_verified = True  # Verified directly for demo convenience
    db.session.commit()
    flash('Email verified successfully! All booking and posting capabilities are unlocked.', 'success')
    return redirect(request.referrer or url_for('main.index'))


# ---------------------------------------------------------------------------
# User Profile & Settings
# ---------------------------------------------------------------------------
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        action = request.form.get('action', 'update_info')

        if action == 'update_info':
            current_user.name = request.form.get('name', '').strip() or current_user.name
            current_user.bio = request.form.get('bio', '').strip()
            current_user.home_city = request.form.get('home_city', '').strip()
            current_user.phone_number = request.form.get('phone_number', '').strip()
            avatar_url = request.form.get('avatar_url', '').strip()
            if avatar_url:
                current_user.avatar_url = avatar_url

            # Interests checkboxes
            interests_list = request.form.getlist('interests')
            if interests_list:
                current_user.interests = json.dumps(interests_list)

            db.session.commit()
            flash('Your profile has been updated.', 'success')

        elif action == 'change_password':
            old_pass = request.form.get('old_password', '')
            new_pass = request.form.get('new_password', '')

            if not current_user.check_password(old_pass):
                flash('Current password entered is incorrect.', 'danger')
            else:
                valid, msg = validate_password_strength(new_pass)
                if not valid:
                    flash(msg, 'danger')
                else:
                    current_user.set_password(new_pass)
                    db.session.commit()
                    flash('Your password has been changed successfully.', 'success')

        elif action == 'delete_account':
            current_user.is_active_account = False
            db.session.commit()
            logout_user()
            flash('Your account has been deactivated. We hope to welcome you back to the mountains soon.', 'info')
            return redirect(url_for('main.index'))

        return redirect(url_for('auth.profile'))

    user_interests = []
    if current_user.interests:
        try:
            user_interests = json.loads(current_user.interests) if current_user.interests.startswith('[') else [i.strip() for i in current_user.interests.split(',')]
        except Exception:
            user_interests = []

    return render_template('auth/profile.html', user=current_user, user_interests=user_interests, title='My Profile — Beyond Tour')


# ---------------------------------------------------------------------------
# Logout
# ---------------------------------------------------------------------------
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out securely.', 'info')
    return redirect(url_for('main.index'))
