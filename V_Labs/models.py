from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from wtforms import FileField, PasswordField, SelectField, StringField, SubmitField, ValidationError
from app import bcrypt
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    bookings = db.relationship('Booking', backref='user', lazy=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    announcements = db.relationship('Announcement', back_populates='lecturer')
    profile_picture = db.Column(db.String(255))

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, role={self.role})"

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(
            password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')

        # Additional custom validation based on your requirements
        if len(username.data) >= 10:
            raise ValidationError('Username must be less than 10 characters.')
        if ' ' in username.data:
            raise ValidationError('Username cannot contain spaces.')
        digits_count = sum(c.isdigit() for c in username.data)
        if digits_count < 1:
            raise ValidationError('Username must contain at least one digits.')


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    version = db.Column(db.String(20), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)

    def __repr__(self):
        return f'<Application {self.name}>'


class Lab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    computers = db.relationship('Computer', backref='lab', lazy=True)
    applications = db.relationship('Application', backref='lab', lazy=True)
    lab_bookings = db.relationship('Lab_booking', backref='lab', lazy=True)
    isBooked = db.Column(db.Boolean, default=False)


class Lab_booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)

    def __repr__(self):
        return f"Lab_booking(user_id={self.user_id}, username={self.user.username}, lab_id={self.lab_id})"


class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lab_id = db.Column(db.Integer, db.ForeignKey('lab.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    booked = db.Column(db.Boolean, default=False)
    bookings = db.relationship('Booking', backref='computer', lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    computer_id = db.Column(db.Integer, db.ForeignKey(
        'computer.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Booking(user_id={self.user_id}, username={self.user.username}, computer_id={self.computer_id}, start_time={self.start_time}, end_time={self.end_time})"


class Announcement(db.Model):
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     default=datetime.now(timezone.utc))

    role = db.Column(db.String(20), nullable=False)

    lecturer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    lecturer = relationship(
        'User', back_populates='announcements')  # Renamed backref

    def __repr__(self):
        return f"Announcement('{self.title}', '{self.date}')"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'date': self.date.isoformat(),
            'role': self.role,
            'lecturer': self.lecturer.username  # Assuming User model has 'username' attribute
        }


class Complaints(db.Model):
    __tablename__ = 'complaints'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, nullable=False,
                     default=lambda: datetime.now(timezone.utc))

    student_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Complaint('{self.subject}', '{self.date}')"
