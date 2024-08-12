import os

from flask import app
from app import db, bcrypt
from models import User

# Ensure you are using the correct database URI
database_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'viewLabsDB.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + database_path

# Initialize the app context
with app.app_context():
    db.create_all()

    # Create a student user
    student_password = bcrypt.generate_password_hash('1234').decode('utf-8')
    student = User(username='student', email='student@example.com', password=student_password, role='student')
    db.session.add(student)

    # Create a lecturer user
    lecturer_password = bcrypt.generate_password_hash('1234').decode('utf-8')
    lecturer = User(username='lecturer', email='lecturer@example.com', password=lecturer_password, role='lecturer')
    db.session.add(lecturer)

    # Create an admin user
    admin_password = bcrypt.generate_password_hash('1234').decode('utf-8')
    admin = User(username='admin', email='admin@example.com', password=admin_password, role='admin')
    db.session.add(admin)

    db.session.commit()

print("Users created successfully!")
