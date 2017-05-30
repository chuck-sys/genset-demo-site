from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from app import app

class ProcessingForm(FlaskForm):
    n30_protout = FileField(validators=[FileRequired()])
