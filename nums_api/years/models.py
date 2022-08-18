from nums_api.database import db
from datetime import datetime
from sqlalchemy import event
from ..shared_utils.email_notification import send_emails_to_subscribers

class Year(db.Model):
    """General facts about years."""

    __tablename__ = "years"

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

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

class Year_Like(db.Model):

    __tablename__='year_likes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    year_fact_id = db.Column(
        db.Integer,
        db.ForeignKey('years.id'),
        default=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
# Event listener decorator
# Calls function when there is an insertion to the the Year table
@event.listens_for(Year, "after_insert")
def listening_for_new_fact(mapper, connection, target):
    """ Calls email sending function
        - Takes:
        mapper, connection and target as required parameters by the decorator
    """
    send_emails_to_subscribers()
