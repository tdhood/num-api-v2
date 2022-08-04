from nums_api import app
from nums_api.database import db
from nums_api.trivia.models import Trivia
from nums_api.maths.models import Math
from nums_api.years.models import Year

db.drop_all(app=app)
db.create_all(app=app)
