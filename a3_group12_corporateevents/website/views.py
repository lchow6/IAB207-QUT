from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import login_required, current_user
from .forms import EventForm, LoginForm
from .models import Event, Ticket, Booking  
from . import db
from datetime import datetime
from werkzeug.utils import secure_filename
from collections import defaultdict
import os


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    login_form = LoginForm()
    # Fetch a sample event to pass (for example the most recent)
    events = Event.query.order_by(Event.checkin_date.desc()).limit(4).all()
    return render_template('index.html', login_form=login_form, events=events)


@main_bp.route('/createevent', methods=['GET', 'POST'])
@login_required  # Ensure user is logged in to create an event
def create_event():
    form = EventForm()
    login_form = LoginForm() 

    if request.method == 'POST':
        print("Form was submitted.")
        print("Form errors:", form.errors)

    if form.validate_on_submit():
        file = form.upload.data
        filename = None

        if file and file.filename:
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.root_path, 'static', 'upload', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            try:
                file.save(upload_path)
                print(f"File saved to: {upload_path}")
            except Exception as e:
                filename = None
                print(f"File save failed: {e}")

        # Outside try/except so it always runs
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
            file_name=filename,
            user_id=current_user.id
        )

        db.session.add(new_event)
        db.session.commit()
        return redirect(url_for('main.view_event', event_id=new_event.id))

    return render_template('createevent.html', form=form, login_form=login_form, event=None)

@main_bp.route('/viewevents')
def view_events():
    events = Event.query.all()
    return render_template('viewevents.html', events=events)

@main_bp.route('/viewevent/<int:event_id>', methods=['GET', 'POST'])
@login_required
def view_event(event_id):
    event = Event.query.get_or_404(event_id)
    login_form = LoginForm()

    if request.method == 'POST':
        ticket_type = request.form.get('ticket_type')
        attendee_names = request.form.get('attendee_names', '').strip().split('\n')
        attendee_names = [name.strip() for name in attendee_names if name.strip()]
        quantity = len(attendee_names)

        if quantity == 0:
            flash("Please enter at least one attendee name.", "warning")
            return redirect(url_for('main.view_event', event_id=event.id))

        # Pricing logic
        if ticket_type == 'General Access':
            price = 50
        elif ticket_type == 'Deluxe Access':
            price = 80
        elif ticket_type == 'V.I.P Access':
            price = 120
        else:
            flash("Invalid ticket type selected.", "danger")
            return redirect(url_for('main.view_event', event_id=event.id))

        total_price = price * quantity

        # Create booking
        booking = Booking(
            user_id=current_user.id,
            event_id=event.id,
            total_price=total_price
        )
        db.session.add(booking)
        db.session.commit()

        # Create tickets with attendee names
        for name in attendee_names:
            ticket = Ticket(
                booking_id=booking.id,
                event_id=event.id,
                price=price,
                seat_number=None,
                ticket_type=ticket_type,
                attendee_name=name  
            )
            db.session.add(ticket)

        db.session.commit()
        flash("Tickets booked successfully!", "success")
        return redirect(url_for('main.view_tickets'))

    return render_template('viewevent.html', event=event, login_form=login_form)


@main_bp.route('/user')
def user():
    login_form = LoginForm()
    return render_template('user.html', login_form=login_form, heading='Login')


@main_bp.route('/eventhistory')
def event_history():
    user_events = Event.query.filter_by(user_id=current_user.id).all()
    return render_template('eventhistory.html', events=user_events)



@main_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = db.session.get(Event, event_id)
    if not event or event.user_id != current_user.id:
        return "Unauthorized", 403

    form = EventForm(obj=event)

    if form.validate_on_submit():
        event.event_name = form.event_name.data
        event.description = form.description.data
        event.event_type = form.event_type.data
        event.checkin_date = datetime.combine(form.checkin_date.data, form.checkin_time.data)
        event.checkout_date = datetime.combine(form.checkout_date.data, form.checkout_time.data)
        event.checkin_time = form.checkin_time.data
        event.checkout_time = form.checkout_time.data

        file = form.upload.data
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'static', 'upload', filename)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            file.save(path)
            event.file_name = filename

        db.session.commit()
        return redirect(url_for('main.view_event', event_id=event.id))

    return render_template('createevent.html', form=form, event=event)

@main_bp.route('/cancel_event/<int:event_id>', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = db.session.get(Event, event_id)
    if not event or event.user_id != current_user.id:
        return "Unauthorized", 403
    event.status = "Cancelled"
    db.session.commit()
    return redirect(url_for('main.event_history'))

from collections import defaultdict

@main_bp.route('/tickets')
@login_required
def view_tickets():
    all_tickets = (
        db.session.query(Ticket)
        .join(Booking)
        .filter(Booking.user_id == current_user.id)
        .all()
    )

    grouped = defaultdict(list)
    for ticket in all_tickets:
        key = (ticket.event_id, ticket.ticket_type)
        grouped[key].append(ticket)

    ticket_groups = []
    for (event_id, ticket_type), tickets in grouped.items():
        event = tickets[0].event
        booking_id = tickets[0].booking_id
        ticket_groups.append({
            'event': event,
            'ticket_type': ticket_type,
            'price': tickets[0].price,
            'quantity': len(tickets),
            'booking_id': booking_id,
            'tickets': tickets  
        })

    return render_template('tickets.html', ticket_groups=ticket_groups)

@main_bp.route('/admin/events')
@login_required
def admin_events():
    events = Event.query.all()
    return render_template("admin_events.html", events=events)




