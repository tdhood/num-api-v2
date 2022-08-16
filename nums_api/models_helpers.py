from nums_api.database import db
from datetime import datetime


class Like(db.Model):
    """Likes information"""

    __tablename__ = "likes"

    id = db.Column(
        db.Integer,
        autoincrement=True,
        primary_key=True,
    )

    fact_id = db.Column(
        db.Integer,
        nullable=False,
        primary_key=True
    )

    # get from URL
    fact_category = db.Column(
        db.String(50),
        nullable=False,
        primary_key=True,
    )

    timestamp = db.Column(
        db.DateTime,
        default=db.func.now(),
        nullable=False,
    )