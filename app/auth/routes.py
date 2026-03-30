import os
from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.models import User, Notification

# Global OAuth instance
oauth = OAuth()
_oauth_initialized = False


def init_oauth(app):
    """Initialize OAuth with the Flask app."""
    global _oauth_initialized
    if _oauth_initialized:
        return
    oauth.init_app(app)
    oauth.register(
        name='google',
        client_id=app.config.get('GOOGLE_CLIENT_ID') or os.environ.get('GOOGLE_CLIENT_ID'),
        client_secret=app.config.get('GOOGLE_CLIENT_SECRET') or os.environ.get('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
    )
    _oauth_initialized = True


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            user.add_points('daily_login')
            db.session.commit()
            next_page = request.args.get('next')
            flash('Welcome back!', 'success')
            return redirect(next_page or url_for('main.index'))
        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(
            email=form.email.data.lower()
        ).first()
        if existing:
            flash('An account with this email already exists.', 'danger')
            return render_template('auth/register.html', form=form)

        user = User(
            first_name=form.first_name.data.strip(),
            last_name=form.last_name.data.strip(),
            email=form.email.data.lower().strip()
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        notif = Notification(
            user_id=user.id,
            type='welcome',
            message='Welcome to MediAsk! Start by asking a health question or sharing your experience.',
            link=url_for('questions.ask')
        )
        db.session.add(notif)
        db.session.commit()

        login_user(user)
        flash('Account created! Welcome to MediAsk.', 'success')
        return redirect(url_for('main.index'))

    return render_template('auth/register.html', form=form)


@bp.route('/login/google')
def google_login():
    """Redirect to Google OAuth."""
    redirect_uri = url_for('auth.google_callback', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@bp.route('/login/google/callback')
def google_callback():
    """Handle Google OAuth callback."""
    try:
        token = oauth.google.authorize_access_token()
        user_info = token.get('userinfo')

        if not user_info:
            flash('Could not get your information from Google.', 'danger')
            return redirect(url_for('auth.login'))

        email = user_info.get('email', '').lower()
        given_name = user_info.get('given_name', 'User')
        family_name = user_info.get('family_name', '')
        picture = user_info.get('picture', '')
        google_id = user_info.get('sub', '')

        user = User.query.filter_by(email=email).first()

        if user:
            if not user.oauth_provider:
                user.oauth_provider = 'google'
                user.oauth_id = google_id
            if picture and not user.avatar_url:
                user.avatar_url = picture
            user.add_points('daily_login')
            db.session.commit()
        else:
            user = User(
                first_name=given_name,
                last_name=family_name or given_name,
                email=email,
                oauth_provider='google',
                oauth_id=google_id,
                avatar_url=picture,
            )
            db.session.add(user)
            db.session.commit()

            notif = Notification(
                user_id=user.id,
                type='welcome',
                message='Welcome to MediAsk! Start by asking a health question or sharing your experience.',
                link=url_for('questions.ask')
            )
            db.session.add(notif)
            db.session.commit()

        login_user(user)
        flash(f'Welcome, {user.first_name}!', 'success')
        return redirect(url_for('main.index'))

    except Exception as e:
        print(f'Google OAuth error: {e}')
        flash('Google sign-in failed. Please try again or use email/password.', 'danger')
        return redirect(url_for('auth.login'))


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been signed out.', 'info')
    return redirect(url_for('main.index'))
