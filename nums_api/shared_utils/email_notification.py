from flask_mail import Mail, Message
from nums_api.subscribers.models import Subscriber

# Creates instance of Mail
mail = Mail()

def send_emails_to_subscribers():
    """ Send new fact notification to subscribers via email. 
        - makes a connection to the Mail server
        - sends emails to each subscriber from the table
    """
    
    subscribers = Subscriber.query.all()
    emails = [subscriber.email for subscriber in subscribers]

    # if there are no subscribers the function will exit here.
    if not emails:
        return None

    # establishes a connection to mail SMTP gmail server.
    # connection is closed automatically once all messages have been sent.
    with mail.connect() as conn:
        for email in emails:
            message = "Hey there's a new fact"
            subject = "Greetings from NumbersAPI"
            msg = Message(
                recipients=[email],
                body=message,
                subject=subject
            )

            conn.send(msg)
