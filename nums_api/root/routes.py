from flask import Blueprint, render_template, redirect, flash
import markdown
from nums_api.database import db

from ..subscribers.models import Subscriber
from ..subscribers.form import SubscriptionForm

root = Blueprint("root", __name__)

@root.route('/', methods = ['GET', 'POST'])
def home_page():
    """Homepage: renders the landing page for Numbers Api
        - Provides a form for users of the app to subscribe and receive emails
    """

    # Reads in the api_docs.md file and converts it to a string of html.
    with open("nums_api/api_docs.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text, output_format='xhtml')

    # shows a form to input and email and subscribe to email notifications.
    form = SubscriptionForm()

    if form.validate_on_submit():
        subscriber = Subscriber(email=form.email.data)

        db.session.add(subscriber)
        db.session.commit()
        flash("Subscribed!", "success")

        return redirect("/")

    return render_template('index.html', docs=html, form=form)
