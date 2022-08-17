from datetime import datetime
from nums_api.trivia.models import  Trivia_Like
from nums_api import app
from nums_api.database import db

CURRENT_TIME = datetime.utcnow()


def test_function():

    fact_A_1 = Trivia_Like(
        trivia_fact_id=2,
        timestamp= datetime(2001,2,2)
    )

    fact_A_2 = Trivia_Like(
        trivia_fact_id=2,
        timestamp= datetime(2001,5,5)
    )

    fact_B_1 = Trivia_Like(
        trivia_fact_id=1,
        timestamp= datetime(2012,12,12)
    )

    db.session.add_all([fact_A_1,fact_A_2,fact_B_1])
    db.session.commit()


def popularity_algorithm():

    # Score = (P-1) / (T+2)^G

    # where,
    # P = points of an item (and -1 is to negate submitters vote)
    # T = time since submission (in hours)
    # G = Gravity, defaults to 1.8 in news.arc


    trivia_likes = (Trivia_Like
            .query
            .group_by(Trivia_Like.trivia_fact_id, Trivia_Like.id)
            .order_by(Trivia_Like.timestamp)
            .all())

    print(trivia_likes)






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





test_function()

popularity_algorithm()