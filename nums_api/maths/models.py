from nums_api.database import db
<<<<<<< HEAD
from datetime import datetime
=======
from sqlalchemy import event
from ..shared_utils.email_notification import send_emails_to_subscribers
>>>>>>> main

class Math(db.Model):
    """General math facts about numbers"""

    __tablename__ = "math"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    number = db.Column(
        db.Integer,
        nullable=False
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(200),
        nullable=False
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(250),
        nullable=False
    )

    was_submitted = db.Column(
        db.Boolean,
        nullable=False
    )

<<<<<<< HEAD
    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )


class Math_Like(db.Model):

    __tablename__='math_likes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    math_fact_id = db.Column(
        db.Integer,
        db.ForeignKey('math.id'),
        default=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
=======
# Event listener decorator
# Calls function when there is an insertion to the the Math table
@event.listens_for(Math, "after_insert")
def listening_for_new_fact(mapper, connection, target):
    """ Calls email sending function
        - Takes:
        mapper, connection and target as required parameters by the decorator
    """
    send_emails_to_subscribers()
>>>>>>> main
