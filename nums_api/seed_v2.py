from sqlite3 import Timestamp
from nums_api import app
from nums_api.database import db
from nums_api.trivia.models import Trivia,Trivia_Like
from nums_api.maths.models import Math,Math_Like
from nums_api.years.models import Year,Year_Like
from nums_api.dates.models import Date,Date_Like
from datetime import datetime



db.drop_all(app=app)
db.create_all(app=app)

trivia_fact = Trivia(
    number=2,
    fact_fragment='hello',
    fact_statement='hello_world',
    was_submitted=True,
    timestamp=datetime(2002,2,2)
)

db.session.add(trivia_fact)
db.session.commit()

trivia_fact = Trivia(
    number=3,
    fact_fragment='mello',
    fact_statement='mello_world',
    was_submitted=True,
    timestamp=datetime(2004,2,2)
)

db.session.add(trivia_fact)
db.session.commit()

trivia_fact = Trivia(
    number=4,
    fact_fragment='testing',
    fact_statement='tesssst',
    was_submitted=True,
    timestamp=datetime(2006,2,2)
)

db.session.add(trivia_fact)
db.session.commit()

year_fact = Year(
    number=3,
    fact_fragment='new',
    fact_statement='new_year',
    was_submitted=True,
    timestamp=datetime(2002,2,2)
)

db.session.add(year_fact)
db.session.commit()

year_fact = Year(
    number=1,
    fact_fragment='dew',
    fact_statement='dew_year',
    was_submitted=True,
    timestamp=datetime(2002,4,2)
)

db.session.add(year_fact)
db.session.commit()

math_fact = Math(
    number=1,
    fact_fragment='math',
    fact_statement='math_fact',
    was_submitted=True,
    timestamp=datetime(2005,2,2)
)

db.session.add(math_fact)
db.session.commit()

math_fact = Math(
    number=3,
    fact_fragment='math',
    fact_statement='More math_fact',
    was_submitted=True,
    timestamp=datetime(2012,2,2)
)

db.session.add(math_fact)
db.session.commit()

date_fact = Date(
    day_of_year=3,
    year=1990,
    fact_fragment='today',
    fact_statement='today nothing happened',
    was_submitted=True,
    timestamp=datetime(2018,2,2)
)

db.session.add(date_fact)
db.session.commit()

date_fact = Date(
    day_of_year=4,
    year=1991,
    fact_fragment='today',
    fact_statement='today nothing happened again',
    was_submitted=True,
    timestamp=datetime(2022,2,2)
)
db.session.add(date_fact)
db.session.commit()


fact_A_1 = Trivia_Like(trivia_fact_id=2, timestamp=datetime(2001, 2, 2))

fact_A_2 = Trivia_Like(trivia_fact_id=2, timestamp=datetime(2001, 5, 5))

fact_B_1 = Trivia_Like(trivia_fact_id=1, timestamp=datetime(2012, 12, 12))

fact_B_2 = Trivia_Like(trivia_fact_id=3, timestamp=datetime(2012, 1, 12))

db.session.add_all([fact_A_1, fact_A_2, fact_B_1, fact_B_2])
db.session.commit()