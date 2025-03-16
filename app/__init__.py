import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Ensure UPLOAD_FOLDER is set
if not app.config['UPLOAD_FOLDER']:
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')

# Ensure the directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db = SQLAlchemy(app)
# Instantiate Flask-Migrate library here
migrate = Migrate(app, db)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import views
