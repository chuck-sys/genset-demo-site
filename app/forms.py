from flask_uploads import UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SelectField
from wtforms.validators import DataRequired
from app import app

csvs = UploadSet('csvs', ('csv',))
configure_uploads(app, (csvs,))

class ProcessingForm(FlaskForm):
    '''
    The form for processing file uploads.
    '''
    testcsv = FileField('test csv', validators=[
        FileRequired(),
        FileAllowed(csvs, 'CSVs only!')
    ])
    trainingcsv = FileField('training csv', validators=[
        FileAllowed(csvs, 'CSVs only!')
    ])
    trainingset = SelectField('Training set', [DataRequired()], choices=[
        ('ecoli', 'E. coli (SPI-2)'),
        ('spi1', 'S. dysenteriae (SPI-1)'),
        ('spi2', 'S. typhimurium (SPI-1/SPI-2)'),
        ('hrp1', 'P. syringae (Hrp1)'),
        ('hrp2', 'X. campestris (Hrp2)'),
        ('chl', 'C. trachematis (Chlam)'),
        ('custom', 'Custom...')
    ])
