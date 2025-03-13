from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, SubmitField
from wtforms.validators import InputRequired, Regexp
from flask_wtf.file import FileAllowed, FileRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class UploadForm(FlaskForm):
    file = FileField('Upload Image', validators=[
        FileRequired(message="Please select a file to upload."),
        FileAllowed(['jpg', 'jpeg', 'png'], message="Only JPG and PNG files are allowed.")
    ])
    submit = SubmitField('Upload')