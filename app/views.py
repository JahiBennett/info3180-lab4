import os
from app import app, db, login_manager
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory
from flask_login import login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash  
from app.models import UserProfile  
from app.forms import LoginForm, UploadForm


###
# Routing for your application.
###

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    form = UploadForm()  # Instantiate the form

    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        flash('File uploaded successfully!', 'success')
        return redirect(url_for('upload'))  

    return render_template('upload.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserProfile.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Successfully logged in!", "success")
            return redirect(url_for("upload"))
        else:
            flash("Invalid username or password.", "danger")
    return render_template("login.html", form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return db.session.execute(db.select(UserProfile).filter_by(id=id)).scalar()

def get_uploaded_images():
    """Retrieve the list of uploaded image filenames."""
    if not os.path.exists(UPLOAD_FOLDER):
        return []
    return [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

@app.route("/uploads/<filename>")
def get_image(filename):
    """Serve images from the uploads folder."""
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/files")
@login_required
def files():
    """Display uploaded images in an HTML template."""
    images = get_uploaded_images()
    return render_template("files.html", images=images)

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
