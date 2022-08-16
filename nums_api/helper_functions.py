from datetime import datetime
from nums_api.trivia.models import Trivia
from nums_api.models_helpers import Like
from nums_api.models_helpers import Liked_Fact
from datetime import date
from nums_api.database import db


def test_function():
        new_liked_fact = Liked_Fact(
                trivia_fact_id=2,
        )

        db.session.add(new_liked_fact)
        db.session.commit()
 
test_function()
# function that queries db for top 10 facts
# time stamp only grabing week at a time . order by grab the sum of the likes

# CURRENT_TIME = datetime.utcnow()
# TIME_WINDOW = CURRENT_TIME.replace(day=CURRENT_TIME.day-7)

# fn (category,fact_id)

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



