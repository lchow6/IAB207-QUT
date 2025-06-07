from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash, bcrypt
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import bcrypt 
from .extensions import db
# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .forms import LoginForm, RegisterForm  # if you also have a RegisterForm
from .models import User
from . import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None

    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data

        # Find user by email instead of first_name
        user = db.session.scalar(db.select(User).where(User.user_name == user_name))

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            login_user(user)
            nextp = request.args.get('next')
            if not nextp or not nextp.startswith('/'):
                return redirect(url_for('main.index'))
            return redirect(nextp)
        else:
            flash(error)

    return render_template('user.html', login_form=login_form, heading='Login')





@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        print("Form validated")
        print("Username:", form.user_name.data)

        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            contact=form.contact.data,
            address=form.address.data,
            user_name=form.user_name.data,
            password=generate_password_hash(form.password.data).decode('utf-8')  
        )

        db.session.add(user)
        db.session.commit()
        print("User saved to DB")

        flash('Account created successfully!')
        return redirect(url_for('main.index'))
    
    print("Form errors:", form.errors)
    return render_template('register.html', form=form)


