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
    app = Flask(__name__)

    # Debug and security config
    app.debug = True
    app.secret_key = 'somesecretkey'

    # Database config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ✅ File upload config
    upload_folder_path = os.path.join(os.getcwd(), 'website', 'static', 'uploads')
    app.config['UPLOAD_FOLDER'] = upload_folder_path
    os.makedirs(upload_folder_path, exist_ok=True)

    # Initialise extensions
    db.init_app(app)
    Bootstrap5(app)

    # Login Manager setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Avoid circular import
    from .models import User, Booking, Event, Ticket, Review

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))  # ✅ Use db.session.get for SQLAlchemy 2.x

    # Register blueprints
    from . import views
    app.register_blueprint(views.main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

    # Create all tables
    with app.app_context():
        db.create_all()

    return app