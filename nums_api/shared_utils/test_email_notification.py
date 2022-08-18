import os
from unittest import TestCase
from nums_api.shared_utils.email_notification import send_emails_to_subscribers
from nums_api.subscribers.models import Subscriber
from nums_api.trivia.models import Trivia
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from flask_mail import Mail

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Configures and initializes Mail instance
mail = Mail()

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_DEFAULT_SENDER'] = "superman@superman.com"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail.init_app(app)

db.drop_all()
db.create_all()


class EmailTestCase(TestCase):
    def setUp(self):
        """ Set up test data here """

        Subscriber.query.delete()

        # Creates a test subscriber to send emails.
        test_subscriber = Subscriber(
            email = "batman@batman.com"
        )

        db.session.add(test_subscriber)
        db.session.commit()

    def tearDown(self):
        """ Clean up any fouled transcation. """
        db.session.rollback()

    def test_empty_outbox(self):
        """ Test to make sure empty outbox. """
        with app.app_context():
            with mail.record_messages() as outbox:

                self.assertEqual(len(outbox), 0)

    def test_sending_email(self):
        """ Test to make sure an email is sent to subscribers. """
        with app.app_context():
            with mail.record_messages() as outbox:
                send_emails_to_subscribers()

                self.assertEqual(len(outbox), 1)

    def test_not_sending_email_when_no_subscribers(self):
        """ Test to make sure no emails are sent when no subscribers
            exist.
        """
        Subscriber.query.delete()
        db.session.commit()

        with app.app_context():
            with mail.record_messages() as outbox:
                send_emails_to_subscribers()
                self.assertEqual(len(outbox), 0)

    def test_sending_email_through_event_listener(self):
        """ Integration test to makes sure email is sent when a new fact is
            added to a fact table.
        """
        with app.app_context():
            with mail.record_messages() as outbox:

                trivia_test = Trivia(
                    number=1,
                    fact_fragment="is the loneliest number.",
                    fact_statement="1 is the loneliest number.",
                    was_submitted=True,
                )

                db.session.add(trivia_test)
                db.session.commit()

                self.assertEqual(len(outbox), 1)
