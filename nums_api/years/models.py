from nums_api.database import db
from datetime import datetime

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
