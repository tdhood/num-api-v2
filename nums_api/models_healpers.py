from nums_api.database import db
from nums_api.years.models import Year
from nums_api.trivia.models import Trivia
from nums_api.dates.models import Date
from nums_api.maths.models import Math


class Like(db.Model):

    __tablename__ = "likes"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    date = db.Column(
        # date input type
        nullable=False
    )


    cate_code = db.relationship('Trivia')
    cate_code = db.relationship('Date')
    cate_code = db.relationship('Math')
    cate_code = db.relationship('Year')
