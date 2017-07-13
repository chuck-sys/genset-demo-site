from flask_uploads import UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField
from wtforms.validators import DataRequired
from app import app

csvs = UploadSet('csvs', ('csv',))
configure_uploads(app, (csvs,))

class ProcessingForm(FlaskForm):
    testcsv = FileField('test csv', validators=[
        FileRequired(),
        FileAllowed(csvs, 'CSVs only!')
    ])
    trainingcsv = FileField('training csv', validators=[
        FileAllowed(csvs, 'CSVs only!')
    ])
    trainingset = SelectField('Training set', [DataRequired()], choices=[
        ('ecoli', 'E. coli'),
        ('spi1', 'S. dysenteriae'),
        ('spi2', 'S. typhimurium'),
        ('hrp1', 'P. syringae'),
        ('hrp2', 'X. campestris'),
        ('chl', 'C. trachematis'),
        ('custom', 'Custom...')
    ])
