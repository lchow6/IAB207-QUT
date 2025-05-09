# import flask - from 'package' import 'Class'
from flask import Flask 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application
def create_app():
    app = Flask(__name__)  # this is the name of the module/package that is calling this app

    # Should be set to False in a production environment
    app.debug = True
    app.secret_key = 'somesecretkey'

    # Set the app configuration for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sitedata.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialise the database with the app
    db.init_app(app)

    # Bootstrap support
    Bootstrap5(app)

    # Initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Blueprint name.function name
    login_manager.init_app(app)

    # Import models here to avoid circular imports
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

    # Create tables inside app context
    with app.app_context():
        db.create_all()

    return app
