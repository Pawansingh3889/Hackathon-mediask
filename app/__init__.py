import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from app.config import config

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please sign in to access this page.'
login_manager.login_message_category = 'info'


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Initialize Google OAuth
    from app.auth.routes import init_oauth
    init_oauth(app)

    from app.questions import bp as questions_bp
    app.register_blueprint(questions_bp, url_prefix='/questions')

    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.workplace import bp as workplace_bp
    app.register_blueprint(workplace_bp, url_prefix='/workplace')

    from app.stories import bp as stories_bp
    app.register_blueprint(stories_bp, url_prefix='/stories')

    # Inject notification count into all templates
    @app.context_processor
    def inject_notifications():
        from flask_login import current_user
        if current_user.is_authenticated:
            return {'notif_count': current_user.unread_count}
        return {'notif_count': 0}

    return app
