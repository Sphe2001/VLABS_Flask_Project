
from datetime import datetime, timedelta, timezone

from functools import wraps
from app import bcrypt
from flask import jsonify, render_template, redirect, render_template_string, request, url_for, flash, Flask
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from app import admin_required, app, db
from models import Booking, User, Lab, Computer, Announcement, Complaints, Application, Lab_booking
from forms import (LoginForm, RegisterForm, AnnouncementForm, AddLabForm, AddComputerForm, ComplaintForm,
                   ApplicationForm, AddLecturerForm, AddAdminForm, RoleFilterForm)
from templates import (index_template, lecturer_dashboard_template, view_computers_lecturer_template,
                       login_template, student_dashboard_template, admin_panel_template, register_template,
                       view_computers_student_template, add_lab_template,
                       add_computer_template, view_computers_template, remove_computer_template, error_template,
                       error_404_template, error_403_template, error_500_template, admin_bookings_view,
                       edit_computer_template, add_lecturer_template, add_announcement_template,
                       view_announcement_template, add_complaint_template, student_complaint_template,
                       view_applications_student_template, add_application_admin, view_applications, view_applications_template,
                       edit_application_template, add_admin_template, view_users_template, view_complaints_template,
                       filter_users_template, student_search_template)
from sqlalchemy.orm import joinedload
from werkzeug.utils import secure_filename
import os
import re


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(
    __file__)), 'static', 'profile_pictures')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    form = LoginForm()
    return render_template_string(index_template, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember_me.data

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password_hash, password):
            login_user(user, remember=remember)
            flash('Login successful!', 'success')

            if user.role == 'student':
                return redirect(url_for('student_dashboard'))
            elif user.role == 'lecturer':
                return redirect(url_for('lecturer_dashboard'))
            elif user.role == 'admin':
                return redirect(url_for('admin_panel'))
            else:
                flash(f'Unknown role "{user.role}" for user {
                      user.username}', 'danger')

        else:
            flash('Login unsuccessful. Please check your credentials.', 'danger')
    return render_template_string(login_template, form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/labs/<int:lab_id>/computers', methods=['GET'])
@login_required
def view_computers(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    computers = Computer.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_computers_student_template, lab=lab, computers=computers)


@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    username = request.form.get('username')
    email = request.form.get('email')
    profile_picture = request.files.get('profile_picture')

    # Check if the new username or email already exists in the database
    if User.query.filter_by(username=username).first() and username != current_user.username:
        if current_user.role == 'student':
            flash('Username already taken. Please choose a different one.', 'danger')

            return redirect(url_for('student_dashboard'))
        elif current_user.role == 'lecturer':
            flash('Username already taken. Please choose a different one.', 'danger')
            return redirect(url_for('lecturer_dashboard'))
        else:
            flash('Username already taken. Please choose a different one.', 'danger')
            return redirect(url_for('admin_panel'))

    if User.query.filter_by(email=email).first() and email != current_user.email:
        if current_user.role == 'student':
            flash('Email already in use. Please choose a different one.', 'danger')

            return redirect(url_for('student_dashboard'))
        elif current_user.role == 'lecturer':
            flash('Email already in use. Please choose a different one.', 'danger')
            return redirect(url_for('lecturer_dashboard'))
        else:
            flash('Email already in use. Please choose a different one.', 'danger')
            return redirect(url_for('admin_panel'))

    # Update user's profile
    current_user.username = username
    current_user.email = email

    # Handle profile picture update
    if profile_picture:
        filename = secure_filename(profile_picture.filename)
        profile_picture.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename))
        current_user.profile_picture = filename

    db.session.commit()

    if current_user.role == 'student':
        flash('Profile picture updated successfully', 'success')

        return redirect(url_for('student_dashboard'))
    elif current_user.role == 'lecturer':
        flash('Profile picture updated successfully', 'success')
        return redirect(url_for('lecturer_dashboard'))
    else:
        flash('Profile picture updated successfully', 'success')
        return redirect(url_for('admin_panel'))


@app.route('/upload_profile_picture', methods=['POST'])
@login_required
def upload_profile_picture():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        current_user.profile_picture = filename
        db.session.commit()
        if current_user.role == 'student':
            flash('Profile picture updated successfully', 'success')

            return redirect(url_for('student_dashboard'))
        elif current_user.role == 'lecturer':
            flash('Profile picture updated successfully', 'success')
            return redirect(url_for('lecturer_dashboard'))
        else:
            flash('Profile picture updated successfully', 'success')
            return redirect(url_for('admin_panel'))

    flash('Invalid file type. Allowed types: png, jpg, jpeg, gif', 'danger')
    return redirect(request.url)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # Get the user by ID
    user = User.query.get_or_404(user_id)

    # Check if the user has bookings and delete them
    if user.bookings:
        for booking in user.bookings:
            db.session.delete(booking)

    # Check if the user has complaints and delete them
    complaints = Complaints.query.filter_by(student_id=user.id).all()
    if complaints:
        for complaint in complaints:
            db.session.delete(complaint)

    # Check if the user has announcements and delete them
    if user.announcements:
        for announcement in user.announcements:
            db.session.delete(announcement)

    # Delete the user
    db.session.delete(user)
    db.session.commit()

    flash(f'User {
          user.username} and all associated records have been deleted.', 'success')
    return redirect(url_for('index'))

#################################################################################################################################
# Lecturers


@app.route('/lecturer_dashboard')
@login_required
def lecturer_dashboard():
    labs = Lab.query.all()
    bookings = Booking.query.all()
    form = AnnouncementForm()
    return render_template_string(lecturer_dashboard_template, labs=labs, bookings=bookings, form=form)


@app.route('/view_computers_lecture/<int:lab_id>', methods=['GET', 'POST'])
@login_required
def view_computers_lecture(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    computers = Computer.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_computers_lecturer_template, lab=lab, computers=computers)


@app.route('/book_lab/<int:lab_id>', methods=['GET', 'POST'])
@login_required
def book_lab(lab_id):
    lab = Lab.query.get_or_404(lab_id)

    # Check if the Lab is already booked
    if lab.isBooked:
        flash('Laboratory is already booked', 'danger')
        return redirect(url_for('lecturer_dashboard'))

    # Check if the user already has an active booking for this Lab
    existing_booking = Lab_booking.query.filter_by(
        user_id=current_user.id, lab_id=lab_id).first()
    if existing_booking:
        flash('You already have an active booking for this Lab', 'danger')
        return redirect(url_for('lecturer_dashboard'))

    # Create a new Booking object
    booking = Lab_booking(user_id=current_user.id, lab_id=lab_id)

    # Try to add the booking and update Lab status
    try:
        db.session.add(booking)
        lab.isBooked = True
        db.session.commit()
        flash('Laboratory booked successfully', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Failed to book Lab {lab_id}: {str(e)}')
        flash('Failed to book the Lab. Please try again.', 'danger')

    return redirect(url_for('lecturer_dashboard'))


###############################################################################################################################
# Students
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        profile_picture = form.profile_picture.data

        if not username[0].isupper():
            flash('Username must start with an uppercase letter.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('username already exists. Please use a different username.', 'danger')
            return redirect(url_for('register'))

        # Create a new user
        new_user = User(username=username, email=email,
                        role=role)
        new_user.set_password(password)

        # Add profile picture if provided
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            new_user.profile_picture = filename

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template_string(register_template, form=form)


@app.route('/student_dashboard')
@login_required
def student_dashboard():
    search_query = request.args.get('q')
    if search_query:
        labs = Lab.query.filter(Lab.name.ilike(f'%{search_query}%')).all()
    else:
        labs = Lab.query.all()
    return render_template_string(student_dashboard_template, labs=labs)


@app.route('/filter_labs', methods=['GET', 'POST'])
def filter_labs():
    if request.method == 'POST':
        application_name = request.form.get('application_name')

        # Query labs based on the application name
        if application_name:
            labs = Lab.query.filter(Lab.applications.any(
                Application.name.ilike(f'%{application_name}%'))).all()
        else:
            labs = Lab.query.all()

        return render_template_string(student_search_template, labs=labs)

    # Handle GET request (show form to input application name)
    return render_template_string(student_search_template)


@app.route('/view_computers/<int:lab_id>', methods=['GET'])
@login_required
def view_computers_student(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    search = request.args.get('search', '')
    if search:
        computers = Computer.query.filter(
            Computer.lab_id == lab_id,
            Computer.applications.ilike(f'%{search}%')
        ).all()
    else:
        computers = Computer.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_computers_student_template, lab=lab, computers=computers)


@app.route('/book_computer/<int:computer_id>', methods=['POST'])
@login_required
def book_computer(computer_id):
    computer = Computer.query.get_or_404(computer_id)

    # Check if the computer is already booked
    if computer.booked:
        flash('Computer is already booked', 'danger')
        return redirect(url_for('view_computers_student', lab_id=computer.lab_id))

    # Check if the user already has an active booking for this computer
    existing_booking = Booking.query.filter_by(
        user_id=current_user.id, computer_id=computer_id, end_time=None).first()
    if existing_booking:
        flash('You already have an active booking for this computer', 'danger')
        return redirect(url_for('view_computers_student', lab_id=computer.lab_id))

    # Calculate start_time and end_time for the new booking
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=3)  # Adjust duration as needed

    # Create a new Booking object
    booking = Booking(user_id=current_user.id, computer_id=computer_id,
                      start_time=start_time, end_time=end_time)

    # Try to add the booking and update computer status
    try:
        db.session.add(booking)
        computer.booked = True
        db.session.commit()
        flash('Computer booked successfully', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Failed to book computer {computer_id}: {str(e)}')
        flash('Failed to book the computer. Please try again.', 'danger')

    return redirect(url_for('view_computers_student', lab_id=computer.lab_id))


####################################################################################################################################
# Admin
@app.route('/admin_panel')
@login_required
@admin_required
def admin_panel():
    labs = Lab.query.all()
    computers = Computer.query.all()
    return render_template_string(admin_panel_template, labs=labs, computers=computers)


@app.route('/add_lecturer', methods=['GET', 'POST'])
@login_required
@admin_required
def add_lecturer():
    form = AddLecturerForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        profile_picture = form.profile_picture.data

        if not username[0].isupper():
            flash('Username must start with an uppercase letter.', 'danger')
            return redirect(url_for('add_lecturer'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('add_lecturer'))

        if User.query.filter_by(username=username).first():
            flash('username already exists. Please use a different username.', 'danger')
            return redirect(url_for('add_lecturer'))

        # Create a new user
        new_user = User(username=username, email=email,
                        role=role)
        new_user.set_password(password)

        # Add profile picture if provided
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            new_user.profile_picture = filename

        db.session.add(new_user)
        db.session.commit()

        flash('Lecturer successful added', 'success')
        return redirect(url_for('admin_panel'))
    return render_template_string(add_lecturer_template, form=form)


@app.route('/add_admin', methods=['GET', 'POST'])
@login_required
@admin_required
def add_admin():
    form = AddAdminForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data
        profile_picture = form.profile_picture.data

        if not username[0].isupper():
            flash('Username must start with an uppercase letter.', 'danger')
            return redirect(url_for('add_admin'))

        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please use a different email.', 'danger')
            return redirect(url_for('add_admin'))

        if User.query.filter_by(username=username).first():
            flash('username already exists. Please use a different username.', 'danger')
            return redirect(url_for('add_admin'))

        # Create a new user
        new_user = User(username=username, email=email,
                        role=role)
        new_user.set_password(password)

        # Add profile picture if provided
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename))
            new_user.profile_picture = filename

        db.session.add(new_user)
        db.session.commit()

        flash('Admin successful added', 'success')
        return redirect(url_for('admin_panel'))
    return render_template_string(add_admin_template, form=form)


@app.route('/admin/bookings')
@login_required
def admin_bookings():
    if current_user.role != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('index'))
    bookings = (db.session.query(Booking)
                .join(Computer)
                .join(Lab)
                .options(joinedload(Booking.computer).joinedload(Computer.lab))
                .all())
    count = len(bookings)
    return render_template_string(admin_bookings_view, bookings=bookings, count=count)


@app.route('/view_users', methods=['GET'])
def view_users():

    users = User.query.all()
    user_count = len(users)

    return render_template_string(view_users_template, users=users, user_count=user_count)


@app.route('/filter_users', methods=['GET', 'POST'])
@login_required
@admin_required
def filter_users():
    form = RoleFilterForm()

    if form.validate_on_submit():
        selected_role = form.role.data
        users = User.query.filter_by(role=selected_role).all()
        user_count = len(users)
    else:
        users = User.query.all()
        user_count = len(users)

    return render_template_string(filter_users_template, users=users, user_count=user_count, form=form)

################################################################################################################################
# Laboratory


@app.route('/add_lab', methods=['GET', 'POST'])
@login_required
@admin_required
def add_lab():
    form = AddLabForm()
    if form.validate_on_submit():
        lab = Lab(name=form.name.data, location=form.location.data)
        db.session.add(lab)
        db.session.commit()
        flash('Lab added successfully', 'success')
        return redirect(url_for('admin_panel'))
    return render_template_string(add_lab_template, form=form)


@app.route('/remove_lab/<int:lab_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def remove_lab(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    if request.method == 'POST':
        db.session.delete(lab)
        db.session.commit()
        flash('Lab removed successfully', 'success')
        return redirect(url_for('admin_panel'))
    return render_template('remove_lab.html', lab=lab)


@app.route('/open_lab/<int:lab_id>', methods=['GET', 'POST'])
def open_lab(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    if lab.isBooked:
        lab.isBooked = False
        db.session.commit()
        flash('Lab Opened', 'success')
        return redirect(url_for('admin_panel'))
    else:
        flash('Lab is already open.', 'info')
    return redirect(url_for('admin_panel'))


@app.route('/close_lab/<int:lab_id>', methods=['GET', 'POST'])
def close_lab(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    if not lab.isBooked:
        lab.isBooked = True
        db.session.commit()
        flash('Lab Closed', 'success')
        return redirect(url_for('admin_panel'))
    else:
        flash('Lab is already Closed.', 'info')
    return redirect(url_for('admin_panel'))

#########################################################################################################################
# Computers


@app.route('/admin_computers/<int:lab_id>')
@login_required
def admin_computers(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    computers = Computer.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_computers_template, lab=lab, computers=computers)


@app.route('/add_computer/<int:lab_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_computer(lab_id):
    form = AddComputerForm()
    lab = Lab.query.get_or_404(lab_id)

    if form.validate_on_submit():
        computer = Computer(
            number=form.number.data,
            lab_id=lab_id,
        )
        db.session.add(computer)
        db.session.commit()
        flash('Computer added successfully', 'success')
        return redirect(url_for('admin_computers', lab_id=lab_id))
    return render_template_string(add_computer_template, form=form, lab=lab)


@app.route('/remove_computer/<int:computer_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def remove_computer(computer_id):
    computer = Computer.query.get_or_404(computer_id)

    if request.method == 'POST':
        try:
            # Delete all bookings associated with the computer
            bookings = Booking.query.filter_by(computer_id=computer_id).all()
            for booking in bookings:
                db.session.delete(booking)

            # Now delete the computer
            db.session.delete(computer)
            db.session.commit()
            flash('Computer and associated bookings removed successfully', 'success')
            return redirect(url_for('admin_computers', lab_id=computer.lab_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Error deleting computer: {str(e)}', 'danger')
    return render_template_string(remove_computer_template, computer=computer)


@app.route('/edit_computer/<int:computer_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_computer(computer_id):
    computer = Computer.query.get_or_404(computer_id)
    form = AddComputerForm(obj=computer)

    if form.validate_on_submit():
        computer.number = form.number.data
        db.session.commit()
        flash('Computer updated successfully', 'success')
        return redirect(url_for('admin_computers', lab_id=computer.lab_id))
    return render_template_string(edit_computer_template, form=form, computer=computer)


@app.route('/make_computers_available', methods=['POST'])
@login_required
@admin_required
def make_computers_available():
    try:
        Computer.query.update({Computer.booked: False})
        db.session.commit()
        return jsonify({'message': 'All computers are now available.'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

#####################################################################################################################
# Applications


@app.route('/admin_applications/<int:lab_id>')
@login_required
def admin_applications(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    applications = Application.query.filter_by(lab_id=lab_id).all()
    return render_template_string(view_applications_template, lab=lab, applications=applications)


@app.route('/add_application/<int:lab_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_application(lab_id):
    form = ApplicationForm()
    lab = Lab.query.get_or_404(lab_id)
    if form.validate_on_submit():
        version = form.version.data

        # Regular expression to check if the version contains only digits and dots
        if not re.match(r'^[0-9.]+$', version):
            flash('Version must contain only numbers and dots.', 'danger')
            return render_template_string(add_application_admin, form=form, lab=lab)

    if form.validate_on_submit():
        application = Application(
            name=form.name.data,
            version=version,
            lab_id=lab_id
        )
        db.session.add(application)
        db.session.commit()
        flash('Application added successfully!', 'success')
        return redirect(url_for('admin_applications', lab_id=lab_id))
    return render_template_string(add_application_admin, form=form, lab=lab)


@app.route('/applications/<int:lab_id>', methods=['GET'])
@login_required
def view_lab_applications(lab_id):
    lab = Lab.query.get_or_404(lab_id)
    applications = Application.query.filter_by(lab_id=lab_id).all()

    return render_template_string(view_applications, lab=lab, applications=applications)


@app.route('/edit_application/<int:application_id>', methods=['GET', 'POST'])
@login_required
def edit_application(application_id):
    application = Application.query.get_or_404(application_id)
    form = ApplicationForm(obj=application)

    if form.validate_on_submit():
        application.name = form.name.data
        application.version = form.version.data
        db.session.commit()
        flash('Application updated successfully!', 'success')
        return redirect(url_for('admin_applications', lab_id=application.lab_id))

    return render_template_string(edit_application_template, form=form, application=application)


@app.route('/delete_application/<int:application_id>', methods=['POST'])
@login_required
def delete_application(application_id):
    application = Application.query.get_or_404(application_id)
    lab_id = application.lab_id
    db.session.delete(application)
    db.session.commit()
    flash('Application deleted successfully!', 'success')
    return redirect(url_for('admin_applications', lab_id=lab_id))


################################################################################################################################
# Complaints
@app.route('/add_complaint', methods=['GET', 'POST'])
@login_required
def add_complaint():
    if current_user.role not in ['student', 'lecturer']:
        flash('Access denied. You are not authorized to add complaints.', 'danger')
        return redirect(url_for('index'))

    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaints(
            subject=form.subject.data,
            content=form.content.data,
            student_id=current_user.id
        )
        db.session.add(complaint)
        db.session.commit()
        flash('Complaint Sent, We will contact you soon', 'success')

        return redirect(url_for('student_dashboard'))

    return render_template_string(add_complaint_template, form=form)


@app.route('/write_complaint')
@login_required
def write_complaint():
    form = ComplaintForm()
    return render_template_string(student_complaint_template, form=form)


@app.route('/view_complaints')
@login_required
@admin_required
def view_complaints():

    complaints = (db.session.query(Complaints, User)
                  .join(User, Complaints.student_id == User.id)
                  .all())
    count = len(complaints)
    return render_template_string(view_complaints_template, complaints=complaints, count=count)


###################################################################################################################
# Announcements
@app.route('/add_announcement', methods=['GET', 'POST'])
@login_required
def add_announcement():
    if current_user.role not in ['lecturer', 'admin']:
        flash('Access denied. You are not authorized to add announcements.', 'danger')
        return redirect(url_for('index'))

    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            lecturer_id=current_user.id,
            role=current_user.role
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement added successfully', 'success')

        if current_user.role == 'admin':
            return redirect(url_for('admin_panel'))
        else:
            return redirect(url_for('lecturer_dashboard'))

    return render_template_string(add_announcement_template, form=form)


@app.route('/view_announcements')
@login_required
def view_announcements():

    print("Current user role:", current_user.role)

    if current_user.role == 'student':
        announcements = Announcement.query.filter(
            (Announcement.role == 'student') | (
                Announcement.lecturer_id != None)
        ).all()
    elif current_user.role == 'lecturer':
        announcements = Announcement.query.filter(
            Announcement.lecturer_id == current_user.id
        ).all()
    else:
        announcements = []

    print("Fetched Announcements:", announcements)
    for ann in announcements:
        print(f"Title: {ann.title}, Role: {
              ann.role}, Lecturer: {ann.lecturer.username}")

    if request.headers.get('content-type') == 'application/json':
        return jsonify([announcement.serialize() for announcement in announcements])
    return render_template_string(view_announcement_template, announcements=announcements)


@app.route('/api/announcements', methods=['GET'])
@login_required
def get_announcements():
    if current_user.role == 'student':
        announcements = Announcement.query.filter(
            (Announcement.role == 'student') | (
                Announcement.lecturer_id != None)
        ).all()
    elif current_user.role == 'lecturer':
        announcements = Announcement.query.filter(
            Announcement.lecturer_id == current_user.id
        ).all()
    else:
        announcements = []

    return jsonify([announcement.serialize() for announcement in announcements])


#######################################################################################################################
# Tables
@app.route('/create_tables')
def create_tables():
    db.create_all()
    return "Tables created successfully."


########################################################################################################################
# Errors
@app.errorhandler(404)
def not_found_error(error):
    return render_template_string(error_404_template), 404


@app.errorhandler(403)
def forbidden_error(error):
    return render_template_string(error_403_template), 403


@app.errorhandler(500)
def internal_error(error):
    return render_template_string(error_500_template), 500
