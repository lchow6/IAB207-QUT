from flask import Blueprint, render_template, url_for

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/createevent')
def create_event():
    return render_template('createevent.html')


@main_bp.route('/user')
def user():
    return render_template('user.html')


@main_bp.route('/eventhistory')
def event_history():
    return render_template('eventhistory.html')


@main_bp.route('/viewevent')
def view_event():
    return render_template('viewevent.html')