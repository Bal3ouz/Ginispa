from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField,SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
#from Data.models import *





class FeedbackForm(FlaskForm):
    message = StringField('Message', widget=TextArea())
    feedback = SelectField(
        'Choose option',
        choices=[ ('1', 'Feedback'), ('2', 'Report a bug'),('3', 'Other')]
    )
    mail_me = BooleanField('Remember me')
    submit  = SubmitField('Submit')