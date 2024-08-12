
base_template = '''
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}View Labs{% endblock %}</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <style>
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        .footer {
            margin-top: auto;
            background-color: #f8f9fa;
            padding: 10px 0;
        }
        .scroll-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            display: none;
        }
        .modal-dialog {
            max-width: 500px;
        }
    
        .modal-content {
            border-radius: 10px;
            box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.2);
        }
    
        .modal-header {
            background-color: #343a40; /* Updated color to match the navbar */
            color: #ffffff;
            border-bottom: none;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        }
    
        .modal-title {
            font-weight: bold;
        }
    
        .modal-body {
            padding: 20px;
        }
    
        .modal-footer {
            border-top: none;
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        }
    
        .close {
            color: #ffffff;
            opacity: 1;
        }
    </style>
</head>
<body>
<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <a class="navbar-brand" href="#">View Labs</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav mr-auto">
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('index') }}"><i class="fas fa-home"></i> Home</a>
            </li>
            {% if current_user.is_authenticated %}
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('student_dashboard') }}"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#" data-toggle="modal" data-target="#announcementModal">
                    <i class="fas fa-bullhorn"></i> Announcements
                </a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('logout') }}"><i class="fas fa-sign-out-alt"></i> Logout</a>
            </li>
            <!-- Profile Icon -->
            <li class="nav-item">
                <a class="nav-link" href="#profileModal" data-toggle="modal">
                    <i class="fas fa-user"></i> {{ current_user.username }}
                </a>
            </li>
            {% else %}
            <li class="nav-item">
                <a class="nav-link" href="{{ url_for('login') }}"><i class="fas fa-sign-in-alt"></i> Login</a>
            </li>
            {% endif %}
        </ul>
        <!-- Search Bar for Logged In Students -->
        {% if current_user.is_authenticated and current_user.role == 'student' %}
        <form class="form-inline ml-auto" action="{{ url_for('student_dashboard') }}" method="GET">
            <input class="form-control mr-sm-2" type="search" placeholder="Search for labs..." aria-label="Search" name="q">
            <button class="btn btn-outline-light my-2 my-sm-0" type="submit">Search</button>
        </form>
        {% endif %}
    </div>
</nav>
<div class="container mt-4">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
</div>
<div class="modal fade" id="profileModal" tabindex="-1" role="dialog" aria-labelledby="profileModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="profileModalLabel">Profile</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <h5>Name: {{ current_user.username }}</h5>
                <p>Email: {{ current_user.email }}</p>
                <h5>Role: {{ current_user.role }}</h5>
                <!-- Update Profile Button -->
                <button class="btn btn-primary" data-toggle="modal" data-target="#updateProfileModal">Update Profile</button>
            </div>
        </div>
    </div>
</div>
<div class="modal fade" id="announcementModal" tabindex="-1" role="dialog" aria-labelledby="announcementModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="announcementModalLabel">Announcements</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                {% for announcement in announcements %}
                <p>{{ announcement }}</p>
                {% endfor %}
                {% if not announcements %}
                <p>No announcements</p>
                {% endif %}
            </div>
        </div>
    </div>
</div>
<footer class="footer text-center">
    <div class="container">
        <span class="text-muted">&copy; 2024 My Flask App. All rights reserved.</span>
    </div>
</footer>
<button class="btn btn-primary scroll-to-top" onclick="scrollToTop()"><i class="fas fa-arrow-up"></i></button>
<script>
    // Scroll to Top Functionality
    function scrollToTop() {
        window.scrollTo({top: 0, behavior: 'smooth'});
    }

    // Show/Hide Scroll to Top Button
    window.addEventListener('scroll', function() {
        const scrollToTopButton = document.querySelector('.scroll-to-top');
        if (window.pageYOffset > 100) {
            scrollToTopButton.style.display = 'block';
        } else {
            scrollToTopButton.style.display = 'none';
        }
    });

    // Highlight Active Navbar Link
    $(document).ready(function() {
        $('a.nav-link').each(function() {
            if (this.href === window.location.href) {
                $(this).addClass('active');
            }
        });
    });
</script>
</body>
</html>



'''

index_template = '''
{% extends "base.html" %}

{% block title %}Welcome to View Labs{% endblock %}

{% block content %}
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <a class="navbar-brand" href="#">View Labs</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ml-auto">
            <li class="nav-item active">
                <a class="nav-link" href="#">Home</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#features">Features</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#testimonials">Testimonials</a>
            </li>
            <li class="nav-item">
                <a class="nav-link" href="#contact">Contact</a>
            </li>
        </ul>
    </div>
</nav>

<section class="vh-100 d-flex align-items-center justify-content-center" style="background-image: url('https://source.unsplash.com/1600x900/?technology,office'); background-size: cover; background-position: center;">
    <div class="jumbotron text-center bg-light shadow p-5">
        <!-- Logo -->
        <div class="mb-4">
            <img src="{{ url_for('static', filename='logo.png') }}" alt="University Logo" style="max-width: 200px; animation: bounce 2s infinite;">
        </div>
        
        <h1 class="display-4">Welcome to View Labs!</h1>
        <p class="lead">This is a simple web application built with Flask.</p>
        <hr class="my-4">
        <p>It allows users to book computers in labs and manage their bookings efficiently.</p>
        {% if form %}
            <div class="mt-4">
                <a class="btn btn-primary btn-lg mr-2" href="/register" role="button">Register</a>
                <a class="btn btn-success btn-lg" href="/login" role="button">Login</a>
            </div>
        {% else %}
            <!-- Handle the case where form is not available -->
            <p class="lead mt-4">
                Please <a href="/login" class="text-primary">login</a> or <a href="/register" class="text-primary">register</a> to access the application.
            </p>
        {% endif %}
    </div>
</section>

<section id="features" class="container my-5">
    <div class="row">
        <div class="col-md-4">
            <h3>Book Computers</h3>
            <p>Easily book available computers in any lab with just a few clicks. Ensure you always have access to the resources you need.</p>
        </div>
        <div class="col-md-4">
            <h3>View Available Labs</h3>
            <p>Check the availability of different labs in real-time. Know exactly where and when you can work without any hassle.</p>
        </div>
        <div class="col-md-4">
            <h3>Access Applications</h3>
            <p>Access a range of pre-installed applications on lab computers, tailored to your academic and professional needs.</p>
        </div>
    </div>
</section>

<section id="testimonials" class="bg-light py-5">
    <div class="container">
        <h2 class="text-center">What Our Users Say</h2>
        <div class="row mt-4">
            <div class="col-md-6">
                <blockquote class="blockquote">
                    <p class="mb-0">This application has greatly improved our lab booking process!</p>
                    <footer class="blockquote-footer">User A, <cite title="Source Title">Company A</cite></footer>
                </blockquote>
            </div>
            <div class="col-md-6">
                <blockquote class="blockquote">
                    <p class="mb-0">An essential tool for managing our computer lab resources efficiently.</p>
                    <footer class="blockquote-footer">User B, <cite title="Source Title">Company B</cite></footer>
                </blockquote>
            </div>
        </div>
    </div>
</section>

<footer id="contact" class="bg-dark text-white py-4">
    <div class="container text-center">
        <p>&copy; 2024 View Labs. All rights reserved.</p>
        <p>Contact us at <a href="mailto:info@viewlabs.com" class="text-light">info@viewlabs.com</a></p>
        <p>
            <a href="#" class="text-light mr-3">Privacy Policy</a>
            <a href="#" class="text-light">Terms of Service</a>
        </p>
    </div>
</footer>

<style>
    body {
        font-family: 'Arial', sans-serif;
    }
    .navbar {
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .navbar-brand {
        font-family: 'Montserrat', sans-serif;
        font-weight: bold;
        color: #333 !important;
    }
    .jumbotron {
        background-color: rgba(255, 255, 255, 0.85);
        border-radius: 15px;
        padding: 40px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s;
    }
    .jumbotron:hover {
        transform: scale(1.05);
    }
    .jumbotron h1 {
        font-weight: 700;
        color: #333;
        font-family: 'Montserrat', sans-serif;
    }
    .jumbotron p {
        font-size: 1.2em;
        color: #555;
    }
    .btn-lg {
        padding: 12px 30px;
        border-radius: 50px;
        font-size: 1.2em;
        transition: background-color 0.3s ease, transform 0.3s ease;
    }
    .btn-lg:hover {
        transform: translateY(-3px);
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    .btn-success {
        background-color: #28a745;
        border: none;
    }
    .btn-success:hover {
        background-color: #218838;
    }
    #features h3, #testimonials h2 {
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 20px;
    }
    footer {
        background-color: #333;
        color: #fff;
        padding: 20px 0;
    }
    footer a {
        color: #f6d365;
    }
</style>
{% endblock %}

'''

login_template = '''
{% extends "base.html" %}

{% block title %}Login - University Lab Booking{% endblock %}

{% block content %}
<section class="vh-100 d-flex align-items-center justify-content-center">
  <div class="login-container">
    <!-- Logo -->
    <div class="text-center mb-4">
      <img src="{{ url_for('static', filename='logo.png') }}" alt="University Logo" style="max-width: 200px;">
    </div>

    <h2>Login</h2>
    <form method="post">
      {{ form.hidden_tag() }}
      <!-- Username input -->
      <div class="form-group">
        {{ form.username(class="form-control", placeholder="Username", required=True) }}
      </div>

      <!-- Password input -->
      <div class="form-group">
        {{ form.password(class="form-control", placeholder="Password", required=True) }}
      </div>

      <!-- Remember me checkbox -->
      <div class="form-check mb-3">
        {{ form.remember_me(class="form-check-input", id="rememberMe") }}
        <label class="form-check-label" for="rememberMe">Remember me</label>
      </div>

      <!-- Submit button -->
      <button type="submit" class="btn btn-primary btn-block login-button">Login</button>
    </form>

    <!-- Register link -->
    <p class="register-link mt-3">Don't have an account? <a href="{{ url_for('register') }}">Sign Up</a></p>
  </div>

  <style>
    body {
      background-color: #f8f9fa;
      font-family: Arial, sans-serif;
    }

    .login-container {
      max-width: 500px;
      width: 100%;
      padding: 30px;
      background-color: #fff;
      border-radius: 10px;
      box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.1);
    }

    .login-container h2 {
      text-align: center;
      margin-bottom: 30px;
    }

    .form-control {
      border-radius: 20px;
    }

    .login-button {
      border-radius: 20px;
    }

    .register-link {
      text-align: center;
    }
  </style>
</section>
{% endblock %}


'''

########################################################################################################################
# Admins
admin_panel_template = '''
{% extends "base.html" %}

{% block title %}Admin Panel{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Logo -->
    <div class="text-center mb-4">
        <img src="https://scontent-jnb2-1.xx.fbcdn.net/v/t39.30808-6/395187173_806217761504774_3521576512401740386_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=5f2048&_nc_ohc=6hWXcWYEMvwQ7kNvgEHdBij&_nc_ht=scontent-jnb2-1.xx&oh=00_AYDjyU8BNNOXG50hCpa0XkzfFHJ_1kX-J82xg4f6pQIA1A&oe=667B2D01" alt="University Logo" class="img-fluid" style="max-width: 200px; border-radius: 50%;">
    </div>

    <div class="row justify-content-center">
        <div class="col-md-10">
            <h2 class="text-center mb-4">Admin Panel</h2>

            {% if current_user.is_authenticated and current_user.role == 'admin' %}
            <div class="text-center mb-4">
                <a href="{{ url_for('add_lecturer') }}" class="btn btn-success mx-2">Add Lecturer</a>
                <a href="{{ url_for('add_admin') }}" class="btn btn-success mx-2">Add Admin</a>
                <a href="{{ url_for('add_lab') }}" class="btn btn-success mx-2">Add Laboratory</a>
                <a href="{{ url_for('admin_bookings') }}" class="btn btn-info mx-2">View All Bookings</a>
                <a href="{{ url_for('view_users') }}" class="btn btn-info mx-2">View All Users</a>
                <a href="{{ url_for('view_complaints') }}" class="btn btn-info mx-2">View Complaints</a>
            </div>

            <div class="row">
                {% if labs %}
                    {% for lab in labs %}
                        <div class="col-md-6 mb-4">
                            <div class="card shadow-sm">
                                <a href="{{ url_for('admin_computers', lab_id=lab.id) }}">
                                    <img src="https://pluspng.com/img-png/computer-lab-png-computer-lab-992.png" class="card-img-top" alt="{{ lab.name }}">
                                </a>
                                <div class="card-body">
                                    <h5 class="card-title font-weight-bold">{{ lab.name }}</h5>
                                    <p class="card-text">{{ lab.location }}</p>
                                    <div class="d-flex justify-content-between">
                                        <a href="{{ url_for('admin_applications', lab_id=lab.id) }}" class="btn btn-primary btn-sm">View Applications</a>
                                        <a href="{{ url_for('open_lab', lab_id=lab.id) }}" class="btn btn-primary btn-sm">Open Lab</a>
                                        <a href="{{ url_for('close_lab', lab_id=lab.id) }}" class="btn btn-secondary btn-sm">Close Lab</a>
                                        <form method="post" action="{{ url_for('remove_lab', lab_id=lab.id) }}" style="display: inline;">
                                            <button type="submit" class="btn btn-danger btn-sm">Remove Lab</button>
                                        </form>
                                    </div>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                {% else %}
                    <div class="col-md-12">
                        <div class="alert alert-warning text-center" role="alert">
                            No labs found. Please add labs first.
                        </div>
                    </div>
                {% endif %}
            </div>

            {% else %}
            <div class="alert alert-danger text-center" role="alert">
                Access denied. You need to be logged in as an admin to access this page.
            </div>
            {% endif %}
        </div>
    </div>
</div>

<div class="modal fade" id="announcementModal" tabindex="-1" role="dialog" aria-labelledby="announcementModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
        <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="announcementModalLabel">Send Announcement</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            <div class="modal-body">
                <form method="post" action="{{ url_for('add_announcement') }}">
                    <div class="form-group">
                        <label for="announcement_title">Title:</label>
                        <input type="text" class="form-control" id="announcement_title" name="title" required>
                    </div>
                    <div class="form-group">
                        <label for="announcement_content">Content:</label>
                        <textarea class="form-control" id="announcement_content" name="content" rows="3" required></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Send</button>
                </form>
            </div>
        </div>
    </div>
</div>

<style>
    /* General Styles */
    body {
        background-color: #f8f9fa;
    }
    .container {
        max-width: 1200px;
    }

    /* Card Styles */
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border-radius: 15px;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
    }
    .card img {
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
    }
    .card-body {
        text-align: center;
    }

    /* Button Styles */
    .btn {
        border-radius: 50px;
        margin-bottom: 10px;
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
    }
    .btn-secondary {
        background-color: #6c757d;
        border: none;
    }
    .btn-danger {
        background-color: #dc3545;
        border: none;
    }
    .btn-info {
        background-color: #17a2b8;
        border: none;
    }
    .btn-success {
        background-color: #28a745;
        border: none;
    }

    /* Announcement Modal Styles */
    .modal-content {
        border-radius: 15px;
    }
    .modal-header {
        background-color: #007bff;
        color: white;
        border-top-left-radius: 15px;
        border-top-right-radius: 15px;
    }
    .modal-body .btn-primary {
        background-color: #007bff;
        border: none;
        border-radius: 15px;
    }
</style>
{% endblock %}



'''

view_complaints_template = '''
{% extends "base.html" %}

{% block title %}View Complaints{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-10">
            <h1 class="my-4">Complaints</h1>
            <div class="alert alert-info text-center">
                Total Complaints: {{ count }}
            </div>
            <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-3">Back to dashboard</a>
            <div class="card mb-4">
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Subject</th>
                                <th>Content</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for complaint, user in complaints %}
                            <tr>
                                <td>{{ user.username }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ complaint.subject }}</td>
                                <td>{{ complaint.content }}</td>
                                <td>{{ complaint.date.strftime('%Y-%m-%d %H:%M:%S') }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}



'''

filter_users_template = '''
{% extends "base.html" %}

{% block title %}Filter Users{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-10">
            <h1 class="my-4">Filter Users by Role</h1>
            <a href="{{ url_for('view_users') }}" class="btn btn-secondary mb-3">Back</a>

            <div class="alert alert-info text-center">
                Total Users: {{ user_count }}
            </div>
            <form method="POST" action="{{ url_for('filter_users') }}" class="mb-4">
                {{ form.hidden_tag() }}
                <div class="input-group mb-3">
                    {{ form.role(class="form-select", id="roleSelect") }}
                    <button type="submit" class="btn btn-primary">Filter</button>
                </div>
            </form>

            <div class="card mb-4">
                <div class="card-body">
                    <table class="table table-striped">
                        <thead>
                            <tr>
                                <th>Username</th>
                                <th>Email</th>
                                <th>Role</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for user in users %}
                            <tr>
                                <td>{{ user.username }}</td>
                                <td>{{ user.email }}</td>
                                <td>{{ user.role }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

'''

######################################################################################################################
# Bookings
admin_bookings_view = '''
{% extends "base.html" %}

{% block title %}Admin Bookings{% endblock %}

{% block content %}
<div class="container mt-4">
    <!-- Logo -->
    <div class="text-center mb-4">
        <img src="path_to_your_logo_image.jpg" alt="University Logo" style="max-width: 200px;">
    </div>

    <h1 class="my-4">All Bookings</h1>
    
        <div class="alert alert-info text-center">
                Total Bookings: {{ count }}
            </div>
    
    <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-3">Back to dashboard</a>
    {% if bookings %}
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Student Username</th>
                    <th>PC Number</th>
                    <th>Lab Name</th>
                    <th>Start Time</th>
                    <th>End Time</th>
                </tr>
            </thead>
            <tbody>
                {% for booking in bookings %}
                <tr>
                    <td>{{ booking.user.username }}</td>
                    <td>{{ booking.computer.number }}</td>
                    <td>{{ booking.computer.lab.name }}</td>
                    <td>{{ booking.start_time }}</td>
                    <td>{{ booking.end_time }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No bookings found.</p>
    {% endif %}
</div>
</div>
{% endblock %}

<style>
    .container {
        margin-top: 2rem;
    }
    .table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 10px;
    }
    .table th, .table td {
        padding: 8px;
        border-bottom: 1px solid #dee2e6;
    }
    .table th {
        background-color: #007bff;
        color: #fff;
        font-weight: bold;
        text-align: left;
    }
    .table tbody tr:nth-of-type(odd) {
        background-color: rgba(0, 0, 0, 0.05);
    }
    .table tbody tr:hover {
        background-color: rgba(0, 0, 0, 0.075);
    }
</style>

'''

############################################################################################################################
add_lecturer_template = '''
{% extends "base.html" %}
{% block title %}Add Lecturer{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-body">
                <div class="text-center mb-4">
                    <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" style="max-width: 200px;">
                </div>
                <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-4">Back to Admin Dashboard</a>
                <h2 class="card-title text-center mb-4">Add Lecturer</h2>
                <form method="post" enctype="multipart/form-data">
                    {{ form.csrf_token }}
                    <div class="form-group">
                        <label for="username">Username:</label>
                        {{ form.username(class="form-control", id="username", autofocus=true) }}
                        {% if form.username.errors %}
                            <ul class="errors">
                                {% for error in form.username.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        {{ form.email(class="form-control", id="email") }}
                        {% if form.email.errors %}
                            <ul class="errors">
                                {% for error in form.email.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        {{ form.password(class="form-control", id="password") }}
                        {% if form.password.errors %}
                            <ul class="errors">
                                {% for error in form.password.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="confirm_password">Confirm Password:</label>
                        {{ form.confirm_password(class="form-control", id="confirm_password") }}
                        {% if form.confirm_password.errors %}
                            <ul class="errors">
                                {% for error in form.confirm_password.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="role">Role:</label>
                        {{ form.role(class="form-control", id="role") }}
                        {% if form.role.errors %}
                            <ul class="errors">
                                {% for error in form.role.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="profile_picture">Profile Picture:</label>
                        {{ form.profile_picture(class="form-control-file", id="profile_picture") }}
                        {% if form.profile_picture.errors %}
                            <ul class="errors">
                                {% for error in form.profile_picture.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Register</button>
                </form>
            </div>
        </div>
    </div>
</div>

<style>
    .card {
        border-radius: 10px;
    }
    .card-body {
        padding: 30px;
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
    }
    .form-group {
        margin-bottom: 20px;
    }
    .form-control {
        border-radius: 5px;
    }
    .form-control-file {
        overflow: hidden;
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
        border-radius: 5px;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    .errors {
        color: red;
        margin-top: 5px;
        list-style-type: none;
    }
</style>
{% endblock %}




'''

add_admin_template = '''
{% extends "base.html" %}
{% block title %}Add Admin{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-body">
                <div class="text-center mb-4">
                    <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" style="max-width: 200px;">
                </div>
                <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-4">Back to Admin Dashboard</a>
                <h2 class="card-title text-center mb-4">Add Admin</h2>
                <form method="post" enctype="multipart/form-data">
                    {{ form.csrf_token }}
                    <div class="form-group">
                        <label for="username">Username:</label>
                        {{ form.username(class="form-control", id="username", autofocus=true) }}
                        {% if form.username.errors %}
                            <ul class="errors">
                                {% for error in form.username.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        {{ form.email(class="form-control", id="email") }}
                        {% if form.email.errors %}
                            <ul class="errors">
                                {% for error in form.email.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        {{ form.password(class="form-control", id="password") }}
                        {% if form.password.errors %}
                            <ul class="errors">
                                {% for error in form.password.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="confirm_password">Confirm Password:</label>
                        {{ form.confirm_password(class="form-control", id="confirm_password") }}
                        {% if form.confirm_password.errors %}
                            <ul class="errors">
                                {% for error in form.confirm_password.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="role">Role:</label>
                        {{ form.role(class="form-control", id="role") }}
                        {% if form.role.errors %}
                            <ul class="errors">
                                {% for error in form.role.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="profile_picture">Profile Picture:</label>
                        {{ form.profile_picture(class="form-control-file", id="profile_picture") }}
                        {% if form.profile_picture.errors %}
                            <ul class="errors">
                                {% for error in form.profile_picture.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Register</button>
                </form>
            </div>
        </div>
    </div>
</div>

<style>
    .card {
        border-radius: 10px;
    }
    .card-body {
        padding: 30px;
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
    }
    .form-group {
        margin-bottom: 20px;
    }
    .form-control {
        border-radius: 5px;
    }
    .form-control-file {
        overflow: hidden;
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
        border-radius: 5px;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    .errors {
        color: red;
        margin-top: 5px;
        list-style-type: none;
    }
</style>
{% endblock %}




'''

view_users_template = '''
{% extends "base.html" %}

{% block title %}View Users{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Users</h1>
    <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-3">Back to Admin Panel</a>
        <div>
            <a href="{{ url_for('filter_users') }}" class="btn btn-primary mb-3">Filter Users</a>
        </div>
        
            <div class="alert alert-info text-center">
                Total Users: {{ user_count }}
            </div>
    
    {% if users %}
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Role</th>
                </tr>
            </thead>
            <tbody>
                {% for user in users %}
                <tr>
                    <td>{{ user.username }}</td>
                    <td>{{ user.email }}</td>
                    <td>
                        {{ user.role }}
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No users were found</p>
    {% endif %}
    
</div>
{% endblock %}


'''

#################################################################################################################################
# Laboratory
add_lab_template = '''
{% extends "base.html" %}
{% block title %}Add Lab{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-8">
        <h2 class="text-center mb-4">Add Lab</h2>
        <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-3">Back to dashboard</a>
        <form method="post">
            {{ form.hidden_tag() }}
            <div class="form-group">
                {{ form.name.label(class="form-control-label") }}
                {{ form.name(class="form-control") }}
                {% for error in form.name.errors %}
                    <span class="text-danger">{{ error }}</span>
                {% endfor %}
            </div>
            <div class="form-group">
                {{ form.location.label(class="form-control-label") }}
                {{ form.location(class="form-control") }}
                {% for error in form.location.errors %}
                    <span class="text-danger">{{ error }}</span>
                {% endfor %}
            </div>
            <button type="submit" class="btn btn-primary">Add Lab</button>
        </form>
    </div>
</div>
{% endblock %}

'''

remove_lab_template = '''
{% extends "base.html" %}
{% block title %}Remove Lab{% endblock %}
{% block content %}
<div class="container">
    <h2 class="text-center my-4">Remove Lab</h2>
    <p>Are you sure you want to remove this lab?</p>
    <form action="{{ url_for('remove_lab', lab_id=lab.id) }}" method="post">
        <button type="submit" class="btn btn-danger">Confirm Removal</button>
    </form>
</div>
{% endblock %}

'''
#################################################################################################################################
# Applications
add_application_admin = '''
{% extends "base.html" %}

{% block title %}Add Application{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Add Application</h1>
    
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.name.label(class="form-control-label") }}
            {{ form.name(class="form-control") }}
            {% for error in form.name.errors %}
                <small class="form-text text-danger">{{ error }}</small>
            {% endfor %}
        </div>
        <div class="form-group">
            {{ form.version.label(class="form-control-label") }}
            {{ form.version(class="form-control") }}
            {% for error in form.version.errors %}
                <small class="form-text text-danger">{{ error }}</small>
            {% endfor %}
        </div>
        <button type="submit" class="btn btn-primary">Add Application</button>
    </form>
</div>
{% endblock %}



'''

view_applications_template = '''
{% extends "base.html" %}

{% block title %}View Applications - {{ lab.name }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">{{ lab.name }} - Applications</h1>
    <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-3">Back to Admin Panel</a>
    {% if applications %}
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Version</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for application in applications %}
                <tr>
                    <td>{{ application.name }}</td>
                    <td>{{ application.version }}</td>
                    <td>
                        <a href="{{ url_for('edit_application', application_id=application.id) }}" class="btn btn-primary btn-sm">Edit</a>
                        <form method="post" action="{{ url_for('delete_application', application_id=application.id) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No Applications found in this lab.</p>
    {% endif %}
    <a href="{{ url_for('add_application', lab_id=lab.id) }}" class="btn btn-primary mt-3">Add Application</a>
</div>
{% endblock %}


'''

edit_application_template = '''
{% extends "base.html" %}

{% block title %}Edit Application{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Edit Application</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.name.label(class="form-control-label") }}
            {{ form.name(class="form-control") }}
            {% for error in form.name.errors %}
                <small class="form-text text-danger">{{ error }}</small>
            {% endfor %}
        </div>
        <div class="form-group">
            {{ form.version.label(class="form-control-label") }}
            {{ form.version(class="form-control") }}
            {% for error in form.version.errors %}
                <small class="form-text text-danger">{{ error }}</small>
            {% endfor %}
        </div>
        <button type="submit" class="btn btn-primary">Update Application</button>
    </form>
</div>
{% endblock %}


'''

##########################################################################################################################
# Computers
add_computer_template = '''
{% extends "base.html" %}

{% block title %}Add Computer{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Add Computer</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.number.label(class="form-control-label") }}
            {{ form.number(class="form-control") }}
            {% for error in form.number.errors %}
                <small class="form-text text-danger">{{ error }}</small>
            {% endfor %}
        </div>
        <button type="submit" class="btn btn-primary">Add Computer</button>
    </form>
</div>
{% endblock %}


'''

view_computers_template = '''
{% extends "base.html" %}

{% block title %}View Computers - {{ lab.name }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">{{ lab.name }} - Computers</h1>
    <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mb-3">Back to Admin Panel</a>
    {% if computers %}
        <table class="table table-striped">
            <thead>
                <tr>
                    
                    <th>Number</th>
                    <th>Booked</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                {% for computer in computers %}
                <tr>
                    
                    <td>{{ computer.number }}</td>
                    <td>{{ computer.booked }}</td>
                    <td>
                        <a href="{{ url_for('edit_computer', computer_id=computer.id) }}" class="btn btn-primary btn-sm">Edit</a>
                        <form method="post" action="{{ url_for('remove_computer', computer_id=computer.id) }}" style="display: inline;">
                            <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                        </form>
                    </td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>No computers found in this lab.</p>
    {% endif %}
    <a href="{{ url_for('add_computer', lab_id=lab.id) }}" class="btn btn-primary mt-3">Add Computer</a>
</div>
{% endblock %}





'''

edit_computer_template = '''
{% extends "base.html" %}

{% block title %}Edit Computer{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Edit Computer</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.number.label(class="form-control-label") }}
            {{ form.number(class="form-control") }}
            {% for error in form.number.errors %}
                <small class="form-text text-danger">{{ error }}</small>
            {% endfor %}
        </div>
        <button type="submit" class="btn btn-primary">Update Computer</button>
    </form>
</div>
{% endblock %}


'''


remove_computer_template = '''
{% extends "base.html" %}

{% block title %}Remove Computer{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1 class="my-4">Remove Computer</h1>
    <p>Are you sure you want to remove computer ID {{ computer.id }}?</p>
    <form method="POST">
        {{ form.hidden_tag() }}
        <button type="submit" class="btn btn-danger">Confirm Removal</button>
        <a href="{{ url_for('admin_computers', lab_id=computer.lab_id) }}" class="btn btn-secondary">Cancel</a>
    </form>
</div>
{% endblock %}


'''


########################################################################################################################
# Students
register_template = '''
{% extends "base.html" %}
{% block title %}Register{% endblock %}
{% block content %}
<div class="row justify-content-center mt-4">
    <div class="col-md-6">
        <div class="card shadow">
            <div class="card-body">
                <div class="text-center mb-4">
                    <img src="{{ url_for('static', filename='logo.png') }}" alt="Logo" style="max-width: 200px;">
                </div>
                <h2 class="card-title text-center mb-4">Register</h2>
                <form method="post" enctype="multipart/form-data">
                    {{ form.csrf_token }}
                    <div class="form-group">
                        <label for="username">Username:</label>
                        {{ form.username(class="form-control", id="username", autofocus=true) }}
                        {% if form.username.errors %}
                            <ul class="errors">
                                {% for error in form.username.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="email">Email:</label>
                        {{ form.email(class="form-control", id="email") }}
                        {% if form.email.errors %}
                            <ul class="errors">
                                {% for error in form.email.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="password">Password:</label>
                        {{ form.password(class="form-control", id="password") }}
                        {% if form.password.errors %}
                            <ul class="errors">
                                {% for error in form.password.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="confirm_password">Confirm Password:</label>
                        {{ form.confirm_password(class="form-control", id="confirm_password") }}
                        {% if form.confirm_password.errors %}
                            <ul class="errors">
                                {% for error in form.confirm_password.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="role">Role:</label>
                        {{ form.role(class="form-control", id="role") }}
                        {% if form.role.errors %}
                            <ul class="errors">
                                {% for error in form.role.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <div class="form-group">
                        <label for="profile_picture">Profile Picture:</label>
                        {{ form.profile_picture(class="form-control-file", id="profile_picture") }}
                        {% if form.profile_picture.errors %}
                            <ul class="errors">
                                {% for error in form.profile_picture.errors %}
                                    <li>{{ error }}</li>
                                {% endfor %}
                            </ul>
                        {% endif %}
                    </div>
                    <button type="submit" class="btn btn-primary btn-block">Register</button>
                </form>
            </div>
        </div>
    </div>
</div>

<style>
    .card {
        border-radius: 10px;
    }
    .card-body {
        padding: 30px;
    }
    .card-title {
        font-size: 24px;
        font-weight: bold;
    }
    .form-group {
        margin-bottom: 20px;
    }
    .form-control {
        border-radius: 5px;
    }
    .form-control-file {
        overflow: hidden;
    }
    .btn-primary {
        background-color: #007bff;
        border: none;
        border-radius: 5px;
    }
    .btn-primary:hover {
        background-color: #0056b3;
    }
    .errors {
        color: red;
        margin-top: 5px;
        list-style-type: none;
    }
</style>
{% endblock %}








'''

student_dashboard_template = '''
{% extends "base.html" %}
{% block title %}Student Dashboard{% endblock %}
{% block content %}
<div class="container">
    <!-- Logo -->
    <div class="text-center mb-4">
        <img src="https://scontent-jnb2-1.xx.fbcdn.net/v/t39.30808-6/395187173_806217761504774_3521576512401740386_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=5f2048&_nc_ohc=6hWXcWYEMvwQ7kNvgEHdBij&_nc_ht=scontent-jnb2-1.xx&oh=00_AYDjyU8BNNOXG50hCpa0XkzfFHJ_1kX-J82xg4f6pQIA1A&oe=667B2D01" alt="University Logo" style="max-width: 200px;">
    </div>

    <h1 class="text-center my-4">Welcome to Student Dashboard</h1>

    <div class="row justify-content-center">
        <div class="col-md-6">
            <form method="post" action="{{ url_for('filter_labs') }}" class="card p-2">
                <div class="input-group">
                    <input type="text" class="form-control" id="application_name" name="application_name" placeholder="Search by application name">
                    <div class="input-group-append">
                        <button type="submit" class="btn btn-primary">Search</button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <div class="row justify-content-center mt-4">
        {% if labs %}
            {% for lab in labs %}
                <div class="col-md-4 mb-4">
                    <div class="card shadow position-relative {% if lab.isBooked %} unavailable {% endif %}">
                        <img src="https://pluspng.com/img-png/computer-lab-png-computer-lab-992.png" class="card-img-top" alt="Computer Lab Image">
                        {% if lab.isBooked %}
                            <div class="unavailable-overlay">
                                <span class="unavailable-text">Unavailable</span>
                            </div>
                        {% endif %}
                        <div class="card-body text-center">
                            <h5 class="card-title">{{ lab.name }}</h5>
                            <a href="{{ url_for('view_computers_student', lab_id=lab.id) }}" class="btn btn-primary btn-block {% if lab.isBooked %} disabled {% endif %}">View Computers</a>
                            <a href="{{ url_for('view_lab_applications', lab_id=lab.id) }}" class="btn btn-primary btn-block {% if lab.isBooked %} disabled {% endif %}">View Applications</a>
                        </div>
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <div class="col-12">
                <div class="alert alert-warning text-center" role="alert">
                    No labs found
                </div>
            </div>
        {% endif %}
    </div>
</div>

<style>
    .container {
        margin-top: 2rem;
    }
    .card {
        border-radius: 10px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .card-img-top {
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        width: 100%;
        height: auto;
    }
    .card-title {
        font-weight: bold;
        color: #343a40;
    }
    .btn-primary {
        background-color: #343a40;
        border: none;
        border-radius: 20px;
    }
    .btn-primary:hover {
        background-color: #23272b;
    }
    .btn-secondary {
        background-color: #6c757d;
        border: none;
        border-radius: 20px;
    }
    .btn-secondary:hover {
        background-color: #5a6268;
    }
    .alert {
        margin-top: 2rem;
    }
    .unavailable .card-img-top {
        filter: grayscale(100%) brightness(50%);
    }
    .unavailable .card-body {
        pointer-events: none; /* Make the card-body unclickable */
    }
    .unavailable-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
    }
    .unavailable-text {
        color: #fff;
        font-size: 1.5rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    .disabled {
        pointer-events: none;
        opacity: 0.6;
    }
</style>
{% endblock %}
'''

student_search_template = '''
{% extends "base.html" %}
{% block title %}Search Results{% endblock %}
{% block content %}
<div class="container">
    <!-- Logo -->
    <div class="text-center mb-4">
        <img src="https://scontent-jnb2-1.xx.fbcdn.net/v/t39.30808-6/395187173_806217761504774_3521576512401740386_n.jpg?_nc_cat=100&ccb=1-7&_nc_sid=5f2048&_nc_ohc=6hWXcWYEMvwQ7kNvgEHdBij&_nc_ht=scontent-jnb2-1.xx&oh=00_AYDjyU8BNNOXG50hCpa0XkzfFHJ_1kX-J82xg4f6pQIA1A&oe=667B2D01" alt="University Logo" style="max-width: 200px;">
    </div>

    <h1 class="text-center my-4">Search Results</h1>
    <div class="row justify-content-center mb-4">
        <div class="col-md-6">
            <form method="post" action="{{ url_for('filter_labs') }}" class="form-inline">
                <div class="input-group w-100">
                    <input type="text" class="form-control" id="application_name" name="application_name" placeholder="Search by application name">
                    <div class="input-group-append">
                        <button type="submit" class="btn btn-primary">Search</button>
                    </div>
                </div>
            </form>
        </div>
    </div>

    <div class="row justify-content-center">
        {% if labs %}
            {% for lab in labs %}
                <div class="col-md-4 mb-4">
                    <div class="card shadow position-relative {% if lab.isBooked %} unavailable {% endif %}">
                        <img src="https://pluspng.com/img-png/computer-lab-png-computer-lab-992.png" class="card-img-top" alt="Computer Lab Image">
                        {% if lab.isBooked %}
                            <div class="unavailable-overlay">
                                <span class="unavailable-text">Unavailable</span>
                            </div>
                        {% endif %}
                        <div class="card-body text-center">
                            <h5 class="card-title">{{ lab.name }}</h5>
                            <a href="{{ url_for('view_computers_student', lab_id=lab.id) }}" class="btn btn-primary btn-block {% if lab.isBooked %} disabled {% endif %}">View Computers</a>
                            <a href="{{ url_for('view_lab_applications', lab_id=lab.id) }}" class="btn btn-primary btn-block {% if lab.isBooked %} disabled {% endif %}">View Applications</a>
                        </div>
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <div class="col-12">
                <div class="alert alert-warning text-center" role="alert">
                    No labs found
                </div>
            </div>
        {% endif %}
    </div>
</div>

<style>
    .container {
        margin-top: 2rem;
    }
    .card {
        border-radius: 10px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .card-img-top {
        border-top-left-radius: 10px;
        border-top-right-radius: 10px;
        width: 100%;
        height: auto;
    }
    .card-title {
        font-weight: bold;
        color: #343a40;
    }
    .btn-primary {
        background-color: #343a40;
        border: none;
        border-radius: 20px;
    }
    .btn-primary:hover {
        background-color: #23272b;
    }
    .btn-secondary {
        background-color: #6c757d;
        border: none;
        border-radius: 20px;
    }
    .btn-secondary:hover {
        background-color: #5a6268;
    }
    .alert {
        margin-top: 2rem;
    }
    .unavailable .card-img-top {
        filter: grayscale(100%) brightness(50%);
    }
    .unavailable .card-body {
        pointer-events: none; /* Make the card-body unclickable */
    }
    .unavailable-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        border-radius: 10px;
    }
    .unavailable-text {
        color: #fff;
        font-size: 1.5rem;
        font-weight: bold;
        text-transform: uppercase;
    }
    .disabled {
        pointer-events: none;
        opacity: 0.6;
    }
</style>
{% endblock %}
'''

view_computers_student_template = '''
{% extends "base.html" %}

{% block title %}View Computers{% endblock %}

{% block content %}
<div class="container">
    <h1 class="text-center my-4">Computers in {{ lab.name }}</h1>
    <p class="text-center"><strong>Location:</strong> {{ lab.location }}</p>
    <a href="{{ url_for('student_dashboard') }}" class="btn btn-secondary mb-4">Back to Student Dashboard</a>
    

    {% if computers %}
        <div class="row justify-content-center">
            {% for computer in computers %}
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm border-0">
                        <img src="https://t3.ftcdn.net/jpg/01/14/34/28/360_F_114342835_4xUSqvc7Sy5uKWxDc4tnYYXYbrh6ShLN.jpg" class="card-img-top" alt="Computer Image">
                        <div class="card-body text-center">
                            <h5 class="card-title">PC-{{ computer.number }}</h5>
                            <p class="card-text"><strong>Status:</strong> {% if computer.booked %} Booked {% else %} Available {% endif %}</p>
                            {% if not computer.booked %}
                            <form action="{{ url_for('book_computer', computer_id=computer.id) }}" method="post">
                                <button type="submit" class="btn btn-primary">Book</button>
                            </form>
                            {% else %}
                                <button class="btn btn-secondary" disabled>Booked</button>
                            {% endif %}
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-warning text-center" role="alert">
            No computers found in this lab.
        </div>
    {% endif %}
</div>

<style>
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .btn {
        border-radius: 20px;
    }
</style>
{% endblock %}

'''


view_applications = '''
{% extends "base.html" %}

{% block title %}View Applications{% endblock %}

{% block content %}
<div class="container">
    <h1 class="text-center my-4">Applications in {{ lab.name }}</h1>
    <p class="text-center"><strong>Location:</strong> {{ lab.location }}</p>
    <a href="{{ url_for('student_dashboard') }}" class="btn btn-secondary mb-4">Back to Student Dashboard</a>


    {% if applications %}
        <div class="row">
            <ol>
            {% for application in applications %}
            
            <li><strong>{{ application.name }}</strong> (Version: {{ application.version }})</li>
            
            {% endfor %}
            </ol>
        </div>
    {% else %}
        <div class="alert alert-warning text-center" role="alert">
            No applications found in this lab.
        </div>
    {% endif %}
</div>

{% endblock %}

'''

view_applications_student_template = '''
{% extends "base.html" %}

{% block title %}View Applications{% endblock %}

{% block content %}
<div class="container mt-4">
    <h1>Application List</h1>
    <ul>
        {% for application in applications %}
            <li>{{ application.name }} - {{ application.version }} (Lab: {{ application.lab.name }})</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('add_application') }}">Add a New Application</a>
</div>
{% endblock %}



'''


view_announcement_template = '''
<!-- view_announcement_template.html -->
{% extends "base.html" %}
{% block title %}Announcements{% endblock %}
{% block content %}
<div class="container">
    
    <h1 class="text-center my-4">Announcements</h1>
    {% if announcements %}
        {% for announcement in announcements %}
            <div class="card mb-4">
                <div class="card-header">
                    <h5>{{ announcement.title }}</h5>
                    <small>by {{ announcement.lecturer.username }} on {{ announcement.date.strftime('%Y-%m-%d %H:%M:%S') }}</small>
                </div>
                <div class="card-body">
                    <p class="card-text">{{ announcement.content }}</p>
                </div>
            </div>
        {% endfor %}
    {% else %}
        <div class="alert alert-warning text-center" role="alert">
            No announcements found
        </div>
    {% endif %}
</div>
{% endblock %}




'''

student_complaint_template = '''
<!-- templates/student_complaint_template.html -->
{% extends "base.html" %}

{% block title %}Write Complaint{% endblock %}

{% block content %}
<div class="container d-flex justify-content-center align-items-center" style="min-height: 100vh;">
    <div class="row justify-content-center w-100">
        <div class="col-md-6 col-lg-5">
            <div class="card shadow-lg border-0">
                <div class="card-body">
                    <h2 class="card-title text-center">Write Complaint</h2>
                    <form method="POST" action="{{ url_for('add_complaint') }}">
                        {{ form.hidden_tag() }}
                        <div class="form-group">
                            {{ form.subject.label(class="form-label") }}
                            {{ form.subject(class="form-control", placeholder="Enter subject") }}
                        </div>
                        <div class="form-group">
                            {{ form.content.label(class="form-label") }}
                            {{ form.content(class="form-control", placeholder="Enter Content", rows=6) }}
                        </div>
                        <div class="d-grid">
                            <button type="submit" class="btn btn-primary btn-block">Submit</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<style>
    .card {
        border-radius: 10px;
    }

    .card-body {
        padding: 2rem;
    }

    .form-group {
        margin-bottom: 1.5rem;
    }

    .form-label {
        font-weight: bold;
    }

    .form-control {
        border-radius: 5px;
        box-shadow: none;
        border: 1px solid #ced4da;
    }

    .form-control:focus {
        border-color: #80bdff;
        box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
    }

    .btn-primary {
        background-color: #007bff;
        border-color: #007bff;
        padding: 0.75rem;
    }

    .btn-primary:hover {
        background-color: #0056b3;
        border-color: #004085;
    }

    .btn-block {
        width: 100%;
    }
</style>
{% endblock %}


'''

add_complaint_template = '''
<!-- add_complaint_template -->
{% extends "base.html" %}
{% block title %}Write Complaint{% endblock %}
{% block content %}
<div class="container">
    <h1 class="text-center my-4">Write Complaint</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.subject.label(class="form-label") }}
            {{ form.subject(class="form-control") }}
        </div>
        <div class="form-group">
            {{ form.content.label(class="form-label") }}
            {{ form.content(class="form-control") }}
        </div>
        <div class="form-group">
            {{ form.submit(class="btn btn-primary") }}
        </div>
    </form>
</div>
{% endblock %}

'''


##########################################################################################################################
# Lecturer
lecturer_dashboard_template = '''
<!-- templates/lecturer_dashboard_template.html -->
{% extends "base.html" %}

{% block title %}Lecturer Dashboard{% endblock %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-md-8">
            <h1>Lecturer Dashboard</h1>
            <p>Welcome, {{ current_user.username }}! This is the lecturer dashboard page.</p>

            <div class="card mb-4">
                <div class="card-body">
                    <h2>View Labs</h2>
                    <ul class="list-group">
                        {% for lab in labs %}
                        <li class="list-group-item">
                            <a href="{{ url_for('view_computers_lecture', lab_id=lab.id) }}">{{ lab.name }} - {{ lab.location }}</a>
                            <span class="badge {% if lab.isBooked %}badge-danger{% else %}badge-success{% endif %}">
                                {% if lab.isBooked %}
                                    Lab Closed
                                {% else %}
                                    Lab Open
                                {% endif %}
                            </span>
                        </li>
                        {% endfor %}
                    </ul>
                </div>
            </div>

            
        </div>

        <div class="col-md-4">
            <div class="card">
                <div class="card-body">
                    <h2>Add Announcement</h2>
                    <form method="POST" action="{{ url_for('add_announcement') }}">
                        {{ form.hidden_tag() }}
                        <div class="form-group">
                            {{ form.title.label }}
                            {{ form.title(class="form-control", placeholder="Enter Title") }}
                        </div>
                        <div class="form-group">
                            {{ form.content.label }}
                            {{ form.content(class="form-control", placeholder="Enter Content", rows=4) }}
                        </div>
                        <button type="submit" class="btn btn-primary">Submit</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}


'''


view_computers_lecturer_template = '''
{% extends "base.html" %}

{% block title %}View Computers{% endblock %}

{% block content %}
<div class="container">
    <h1 class="text-center my-4">Computers in {{ lab.name }}</h1>
    <p class="text-center"><strong>Location:</strong> {{ lab.location }}</p>
    <a href="{{ url_for('lecturer_dashboard') }}" class="btn btn-secondary mb-4">Back to Lecturer Dashboard</a>


    {% if computers %}
        <div class="row justify-content-center">
            {% for computer in computers %}
                <div class="col-md-4 mb-4">
                    <div class="card shadow-sm border-0">
                        <img src="https://t3.ftcdn.net/jpg/01/14/34/28/360_F_114342835_4xUSqvc7Sy5uKWxDc4tnYYXYbrh6ShLN.jpg" class="card-img-top" alt="Computer Image">
                        <div class="card-body text-center">
                            <h5 class="card-title">PC-{{ computer.number }}</h5>
                            
                            <p class="card-text"><strong>Status:</strong> {% if computer.booked %} Booked {% else %} Available {% endif %}</p>
                            {% if not computer.booked %}
                                <button class="btn btn-secondary" disabled>Avaliable</button>
                            {% else %}
                                <button class="btn btn-secondary" disabled>Booked</button>
                            {% endif %}
                        </div>
                    </div>
                </div>
            {% endfor %}
        </div>
    {% else %}
        <div class="alert alert-warning text-center" role="alert">
            No computers found in this lab.
        </div>
    {% endif %}
</div>

<style>
    .card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .btn {
        border-radius: 20px;
    }
</style>
{% endblock %}


'''


add_announcement_template = '''
<!-- add_announcement_template -->
{% extends "base.html" %}
{% block title %}Add Announcement{% endblock %}
{% block content %}
<div class="container">
    <h1 class="text-center my-4">Add Announcement</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div class="form-group">
            {{ form.title.label(class="form-label") }}
            {{ form.title(class="form-control") }}
        </div>
        <div class="form-group">
            {{ form.content.label(class="form-label") }}
            {{ form.content(class="form-control") }}
        </div>
        <div class="form-group">
            {{ form.submit(class="btn btn-primary") }}
        </div>
    </form>
</div>
{% endblock %}

'''


#######################################################################################################################
# Errors
error_403_template = '''
{% extends "base.html" %}

{% block title %}
    403 Forbidden
{% endblock %}

{% block content %}
    <div class="container">
        <h1>403 - Forbidden</h1>
        <p>Sorry, you are not authorized to access this page.</p>
        <p>Return to <a href="{{ url_for('index') }}">home</a>.</p>
    </div>
{% endblock %}
'''

error_404_template = '''
{% extends "base.html" %}

{% block title %}
    404 Not Found
{% endblock %}

{% block content %}
    <div class="container">
        <h1>404 - Not Found</h1>
        <p>The page you are looking for does not exist.</p>
        <p>Return to <a href="{{ url_for('index') }}">home</a>.</p>
    </div>
{% endblock %}

'''

error_500_template = '''
{% extends "base.html" %}

{% block title %}
    500 Internal Server Error
{% endblock %}

{% block content %}
    <div class="container">
        <h1>500 - Internal Server Error</h1>
        <p>Sorry, something went wrong on the server.</p>
        <p>Please try again later.</p>
        <p>Return to <a href="{{ url_for('index') }}">home</a>.</p>
    </div>
{% endblock %}

'''

error_template = '''
{% extends "base.html" %}

{% block title %}Error{% endblock %}

{% block content %}
    <h2>Error</h2>
    <p>{{ error_message }}</p>
{% endblock %}


'''
