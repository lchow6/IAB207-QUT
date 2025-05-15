# import flask - from 'package' import 'Class'
from flask import Flask 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# initialise SQLAlchemy instance globally
db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application
def create_app():
    app = Flask(__name__)  # this is the name of the module/package that is calling this app

    # Debug and secret key
    app.debug = True
    app.secret_key = 'somesecretkey'

    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # File upload config 
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'website', 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    # Initialise extensions
    db.init_app(app)
    Bootstrap5(app)

    # Initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Import models inside function to avoid circular imports
    from .models import User, Booking, Event, Ticket, Review

    # Define user loader callback
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))

    # Register blueprints
    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    # ✅ Create all database tables
    with app.app_context():
        db.create_all()

    return app
