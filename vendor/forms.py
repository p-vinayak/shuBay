from flask_wtf import FlaskForm
from wtforms import *


class VendorApplicationForm(FlaskForm):
    title = StringField('Title', [validators.Length(min=1, max=100), validators.DataRequired()])
    description = TextAreaField('Description', [validators.Length(min=1, max=1024), validators.DataRequired()])
