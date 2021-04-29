from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class LinkAddressForm(FlaskForm):
    address = StringField('nano_address')
    submit = SubmitField('Explore')