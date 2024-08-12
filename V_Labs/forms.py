from flask_wtf import FlaskForm
from wtforms import BooleanField, FileField, IntegerField, RadioField, SelectField, StringField, PasswordField, SubmitField, TextAreaField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp

from models import User
from models import Lab


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=80,
               message="Username must be between 4 and 80 characters long"),
        Regexp(
            r'^[A-Z][a-zA-Z0-9]*$',
            message="Username must start with an uppercase letter"
        )
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
                       ('student', 'Student')], validators=[DataRequired()])
    profile_picture = FileField('Profile Picture')

    submit = SubmitField('Register')


class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    role = SelectField('Role', choices=[('all', 'All'), ('lecturer', 'Lecturer'), (
        'admin', 'Admin')], default='all', validators=[DataRequired()])
    submit = SubmitField('Send Announcement')


class ComplaintForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send Complaint')


class LabForm(FlaskForm):
    name = StringField('Lab Name', validators=[
        DataRequired(), Length(min=2, max=50)])
    location = StringField('Location', validators=[
        DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Submit')


class AddLabForm(FlaskForm):
    name = StringField('Lab Name', validators=[
        DataRequired(), Length(min=2, max=50)])
    location = StringField('Location', validators=[
        DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Submit')


class AddComputerForm(FlaskForm):
    number = IntegerField('Number', validators=[DataRequired()])
    submit = SubmitField('Add Computer')


class SearchForm(FlaskForm):
    application = StringField('Application', validators=[DataRequired()])
    submit = SubmitField('Search')


class ComputerForm(FlaskForm):
    number = IntegerField('Computer Number', validators=[DataRequired()])
    applications = StringField('Applications', validators=[
        DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Submit')


class AddLecturerForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=80,
               message="Username must be between 4 and 80 characters long"),
        Regexp(
            r'^[A-Z][a-zA-Z0-9]*$',
            message="Username must start with an uppercase letter, contain no spaces, and have at least one digits"
        )
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
                       ('lecturer', 'Lecturer')], validators=[DataRequired()])
    profile_picture = FileField('Profile Picture')

    submit = SubmitField('Register')


class AddAdminForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=80,
               message="Username must be between 4 and 80 characters long"),
        Regexp(
            r'^[A-Z][a-zA-Z0-9]*$',
            message="Username must start with an uppercase letter, contain no spaces, and have at least one digit"
        )
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[
                       ('admin', 'Admin')], validators=[DataRequired()])
    profile_picture = FileField('Profile Picture')

    submit = SubmitField('Register')


class ApplicationForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(max=50)])
    version = StringField('Version', validators=[
                          DataRequired(), Length(max=20)])
    submit = SubmitField('Add Application')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    profile_picture = FileField('Profile Picture')
    submit = SubmitField('Save changes')


class RoleFilterForm(FlaskForm):
    role = SelectField(
        'Select Role',
        choices=[('student', 'Student'), ('lecturer',
                                          'Lecturer'), ('admin', 'Admin')],
        default='student'
    )
    submit = SubmitField('Filter')
