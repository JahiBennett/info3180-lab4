import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash  
from app.models import UserProfile  
from app.forms import LoginForm, UploadForm


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/upload', methods=['POST', 'GET'])
@login_required  # Ensure user is logged in before accessing upload
def upload():
    """Upload route for logged-in users."""
    form = UploadForm()  # Instantiate the UploadForm

    if form.validate_on_submit():  # Validate form submission
        file = form.file.data  # Get uploaded file
        filename = secure_filename(file.filename)  # Sanitize filename
        file.save(os.path.join('uploads', filename))  # Save file to uploads folder

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('home'))  # Update this to display all uploaded files

    return render_template('upload.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route to authenticate users."""
    form = LoginForm()  # Create an instance of LoginForm

    if form.validate_on_submit():  # Ensure form data is valid
        username = form.username.data
        password = form.password.data

        # Query the database for the user
        user = UserProfile.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):  # Verify password
            login_user(user)  # Log the user in
            flash('Login successful!', 'success')
            return redirect(url_for('upload'))  # Redirect to the upload page
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', form=form)

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

###
# The functions below should be applicable to all Flask apps.
###

# Flash errors from the form if validation fails
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
