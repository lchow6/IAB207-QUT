
from flask import Flask
from .extensions import db, bcrypt, login_manager
from flask_bootstrap import Bootstrap5

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqllite_database.db'
    app.config['UPLOAD_FOLDER'] = 'website/static/upload'

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    Bootstrap5(app)

    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from . import views, auth
    app.register_blueprint(views.main_bp)
    app.register_blueprint(auth.auth_bp)

    return app
