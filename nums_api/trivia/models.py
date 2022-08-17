from email.policy import default
from nums_api.database import db
from datetime import datetime


class Trivia(db.Model):
    """General trivia facts about numbers."""

    __tablename__ = "trivia"

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

class Trivia_Like(db.Model):

    __tablename__='trivia_likes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    trivia_fact_id = db.Column(
        db.Integer,
        db.ForeignKey('trivia.id'),
        default=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
    )

    # is this fact id in table
    # check if is_trending is on
    # add 1 to counter points
    # grouping by the total times a fact is in the datebase, and use that in
    # the algorithm as 'P'

    # and our time is going to follow : (time now - timestamp ) = T

    # after 7 days using some type of logic, we set 'on' in is_trending to 'off'


    # score is generated each time we use the popularity algorithm, but not
    # stored in the db. they are going to be stored in an an array inside the
    # function, which we will use for ranking.


    # to turn the trending to off :
    # we are checking the last record if the fact is still
    # trending,* we are going to find the

    # *if a fact doesn't get a like in 7 days, first instance
    # where it's on set it to off.