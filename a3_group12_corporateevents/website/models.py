from . import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.id}: {self.first_name} {self.last_name}, Email: {self.email}>"


class Booking(db.Model):
    __tablename__ = 'bookings'

    id = db.Column(db.Integer, primary_key=True)
    booking_date = db.Column(db.DateTime, default=datetime)
    total_price = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)

    tickets = db.relationship('Ticket', backref='booking', lazy=True)

    def __repr__(self):
        return f"<Booking {self.id}: User {self.user_id}, Event {self.event_id}, Date {self.booking_date}, Total ${self.total_price:.2f}>"


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    checkin_date = db.Column(db.DateTime, nullable=False)
    checkout_date = db.Column(db.DateTime, nullable=False)
    checkin_time = db.Column(db.DateTime, nullable=False)
    checkout_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    bookings = db.relationship('Booking', backref='event', lazy=True)
    tickets = db.relationship('Ticket', backref='event', lazy=True)
    reviews = db.relationship('Review', backref='event', lazy=True)

    def __repr__(self):
        return f"<Event {self.id}: {self.event_name} ({self.event_type}) - Status: {self.status}>"



class Ticket(db.Model):
    __tablename__ = 'tickets'

    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    seat_number = db.Column(db.String(10), nullable=True)
    ticket_type = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Ticket {self.id}: Event {self.event_id}, Booking {self.booking_id}, ${self.price:.2f}, Seat {self.seat_number or 'N/A'}>"


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, default=datetime)

    def __repr__(self):
        return f"<Review {self.id}: User {self.user_id}, Event {self.event_id}, Rating {self.rating}>"
