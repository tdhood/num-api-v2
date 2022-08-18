from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Email, InputRequired

class SubscriptionForm(FlaskForm):
    """Form for subscribing to factual updates"""

    email = StringField(
        "Enter your email address",
        validators=[Email(), InputRequired()]
    )

class CSRFProtectionForm(FlaskForm):
    """Form for adding CSRF protection"""
