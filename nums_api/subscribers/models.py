from nums_api.database import db

class Subscriber(db.Model):
    """ Subscribers to NumbersAPI """

    __tablename__ = "subscribers"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )

    email = db.Column(
        db.String(30),
        nullable=True,
    )
