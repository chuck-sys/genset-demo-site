from flask_uploads import UploadSet, configure_uploads, ARCHIVES
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField
from wtforms.validators import DataRequired
from app import app

csvs = UploadSet('csvs', ('csv',))
configure_uploads(app, (csvs,))

class ProcessingForm(FlaskForm):
    testzip = FileField('test archive', validators=[
        FileRequired(),
        FileAllowed(csvs, 'CSVs only!')
    ])
    trainingzip = FileField('training archive', validators=[
        FileAllowed(csvs, 'CSVs only!')
    ])
    trainingset = SelectField('Training set', [DataRequired()], choices=[
        ('ysc', 'Y. Pestis'),
        ('spi1', 'S. dysenteriae'),
        ('spi2', 'S. typhimurium'),
        ('hrp1', 'P. syringae'),
        ('hrp2', 'X. campestris'),
        ('chl', 'C. trachematis'),
        ('rhi', 'S. fredii'),
        ('custom', 'Custom...')
    ])
