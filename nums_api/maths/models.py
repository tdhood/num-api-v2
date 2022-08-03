from nums_api.database import db

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

    pos = db.Column(
        db.String(20), 
        nullable=False
    )

    self = db.Column(
        db.Boolean,
        nullable=False
    )
