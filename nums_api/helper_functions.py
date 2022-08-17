from datetime import datetime
from sqlalchemy import func
from nums_api.trivia.models import Trivia, Trivia_Like
from nums_api import app
from nums_api.database import db

CURRENT_TIME = datetime.utcnow()

# db.drop_all(app=app)
# db.create_all(app=app)


def test_function():

    fact_A_1 = Trivia_Like(trivia_fact_id=2, timestamp=datetime(2001, 2, 2))

    fact_A_2 = Trivia_Like(trivia_fact_id=2, timestamp=datetime(2001, 5, 5))

    fact_B_1 = Trivia_Like(trivia_fact_id=1, timestamp=datetime(2012, 12, 12))

    fact_B_2 = Trivia_Like(trivia_fact_id=3, timestamp=datetime(2012, 1, 12))

    db.session.add_all([fact_A_1, fact_A_2, fact_B_1, fact_B_2])
    db.session.commit()


# test_function()

# Score = (P-1) / (T+2)^G

    # where,
    # P = points of an item (and -1 is to negate submitters vote)
    # T = time since submission (in hours)
    # G = Gravity, defaults to 1.8 in news.arc


def fetch_points():


    # returns array of (trivia_fact_id, totals likes) // [(3,1)...]
    trivia_points = (
        Trivia_Like.query.with_entities(
            Trivia_Like.trivia_fact_id, func.count(Trivia_Like.trivia_fact_id))
        .group_by(Trivia_Like.trivia_fact_id)
        .all()
    )
    print(trivia_points)
    return trivia_points


points = fetch_points()

def fetch_time_of_submission(points):

    trivia_fact_ids = []

    for items in points:
        trivia_fact_ids.append(items[0])
    
    print('trivia fact ids', trivia_fact_ids)

    trivia_ids_and_time = []
    for items in trivia_fact_ids:
        trivia_fact_submission_time = (
            Trivia.query.with_entities(
                Trivia.id, Trivia.timestamp
            ).all()
        )
        trivia_ids_and_time.append(trivia_fact_submission_time)
    
    print(trivia_ids_and_time)

fetch_time_of_submission(points)

# function that queries db for top 10 facts
# time stamp only grabing week at a time . order by grab the sum of the likes

# TIME_WINDOW = CURRENT_TIME.replace(day=CURRENT_TIME.day-7)

# like = Like (
#         fact_id=fact_id,
#         fact_category=category,
#         uniqe_id=
# )


# likes = (Like
#             .query
#             .filter(Like.timestamp).in_([TIME_WINDOW,CURRENT_TIME])
#             .group_by(Like.fact_id & Like.fact_category)
#             .order_by(Like.timestamp.desc())
#             .limit(10)
#             .all())
