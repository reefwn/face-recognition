from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired

extensions = ['jpg', 'jpeg', 'png']
ext_error = 'Images only!'


class CompareForm(FlaskForm):
    image1 = FileField('Upload First Image', validators=[
                       DataRequired(), FileAllowed(extensions, ext_error)])
    image2 = FileField('Upload Second Image', validators=[
                       DataRequired(), FileAllowed(extensions, ext_error)])
    submit = SubmitField('Compare')
