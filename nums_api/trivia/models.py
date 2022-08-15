from nums_api.database import db


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

    category = db.Column(
        db.String(50),
        nullable=False
    )
