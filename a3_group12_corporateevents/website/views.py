from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .forms import EventForm
from .models import Event
from . import db
from datetime import datetime
from werkzeug.utils import secure_filename
import os


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/createevent', methods=['GET', 'POST'])
def create_event():
    form = EventForm()

    if request.method == 'POST':
        print("📨 Form was submitted.")
        print("Form errors:", form.errors)

    if form.validate_on_submit():
        print("✅ Form validated successfully.")

        file = form.upload.data
        filename = None

        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            try:
                file.save(upload_path)
                print(f"✅ File saved to: {upload_path}")
            except Exception as e:
                print(f"❌ File save failed: {e}")
        else:
            print("⚠️ No file selected or empty filename.")

        # Combine date and time
        checkin_dt = datetime.combine(form.checkin_date.data, form.checkin_time.data)
        checkout_dt = datetime.combine(form.checkout_date.data, form.checkout_time.data)

        new_event = Event(
            event_name=form.event_name.data,
            description=form.description.data,
            event_type=form.event_type.data,
            checkin_date=checkin_dt,
            checkout_date=checkout_dt,
            checkin_time=checkin_dt,
            checkout_time=checkout_dt,
            status=form.status.data,
            # file_name=filename  # Uncomment if storing filename
        )

        db.session.add(new_event)
        db.session.commit()

        print("🎉 Event created and committed to the database.")
        return redirect(url_for('main.view_event'))

    return render_template('createevent.html', form=form)





@main_bp.route('/user')
def user():
    return render_template('user.html')


@main_bp.route('/eventhistory')
def event_history():
    return render_template('eventhistory.html')


@main_bp.route('/viewevent')
def view_event():
    return render_template('viewevent.html')