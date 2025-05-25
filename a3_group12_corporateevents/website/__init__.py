from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialise extensions globally
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Set before init_app

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'somesecretkey'

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # File upload config
    upload_folder_path = os.path.join(os.getcwd(), 'website', 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder_path
    os.makedirs(upload_folder_path, exist_ok=True)

    # Initialise extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    Bootstrap5(app)

    # Defer model imports to avoid circular imports
    from .models import User, Booking, Event, Ticket, Review

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    from . import views
    from . import auth
    app.register_blueprint(views.main_bp)
    app.register_blueprint(auth.auth_bp)

    # Create all database tables
    with app.app_context():
        db.create_all()

    return app
