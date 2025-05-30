from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, SelectField
from wtforms.fields import DateField, TimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired
from flask_wtf.file import FileField, FileAllowed   



# Login Form
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

# Register Form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired(), Length(min=2, max=50)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(min=2, max=50)])
    email = StringField("Email Address", validators=[InputRequired(), Email()])
    contact = StringField("Contact Number", validators=[InputRequired(), Length(min=6, max=15)])
    address = StringField("Street Address", validators=[InputRequired()])
    user_name = StringField("User Name", validators=[InputRequired(), Length(min=3, max=20)])
    password = PasswordField("Password", validators=[
        InputRequired(),
        EqualTo('confirm', message="Passwords should match")
    ])
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Register")

# Event Form
class EventForm(FlaskForm):
    event_name = StringField('Event Name', validators=[DataRequired()])
    
    description = TextAreaField('Description', validators=[DataRequired()])
    
    event_type = SelectField('Event Type', choices=[
        ('', 'Choose event type'),
        ('Seminar', 'Seminar'),
        ('Conference', 'Conference'),
        ('Webinar', 'Webinar'),
        ('Networking', 'Networking')
    ], validators=[DataRequired()])

    checkin_date = DateField('Check-in Date', format='%Y-%m-%d', validators=[DataRequired()])
    checkout_date = DateField('Check-out Date', format='%Y-%m-%d', validators=[DataRequired()])
    
    checkin_time = TimeField('Check-in Time', format='%H:%M', validators=[DataRequired()])
    checkout_time = TimeField('Check-out Time', format='%H:%M', validators=[DataRequired()])

    status = SelectField('Status', choices=[
        ('Open', 'Open'),
        ('Inactive', 'Inactive'),
        ('Sold Out', 'Sold Out'),
        ('Cancelled', 'Cancelled')
    ], validators=[DataRequired()])

    upload = FileField('Upload files', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'pdf', 'docx'], 'Only images and documents allowed!')
    ])

    submit = SubmitField('Create Event')

