from datetime import datetime
from nums_api.models_helpers import Like
from datetime import date



# function that queries db for top 10 facts
# time stamp only grabing week at a time . order by grab the sum of the likes

CURRENT_TIME = datetime.utcnow()
TIME_WINDOW = CURRENT_TIME.replace(day=CURRENT_TIME.day-7)

fn (category,fact_id)

like = Like (
        fact_id=fact_id,
        fact_category=category,
        uniqe_id=
)


likes = (Like
            .query
            .filter(Like.timestamp).in_([TIME_WINDOW,CURRENT_TIME])
            .group_by(Like.fact_id & Like.fact_category)
            .order_by(Like.timestamp.desc())
            .limit(10)
            .all())



