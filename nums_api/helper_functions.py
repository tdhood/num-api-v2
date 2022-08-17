from datetime import datetime
from sqlalchemy import func
from nums_api.trivia.models import Trivia, Trivia_Like


CURRENT_TIME = datetime.utcnow()
G = 1.00002

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
    print("arry ids total likes ",trivia_points)
    return trivia_points


points = fetch_points()

def fetch_time_of_submission(points):

    trivia_fact_ids = []

    for items in points:
        trivia_fact_ids.append(items[0])

    print('trivia fact ids', trivia_fact_ids)

    trivia_ids_and_points_and_times = []
    for item in points:
        trivia_fact_submission_time = (
            Trivia.query.get(item[0])
        )
        trivia_ids_and_points_and_times.append(
            [item[0],item[1],trivia_fact_submission_time.timestamp])

    return trivia_ids_and_points_and_times

start_times = fetch_time_of_submission(points)

def delta_time(start_times):


    ids_and_points_delta_time =[]
    for item in start_times:
        delta = CURRENT_TIME - item[2]
        ids_and_points_delta_time.append([item[0],item[1],delta.days])
    print("delta times : ",ids_and_points_delta_time)
    return(ids_and_points_delta_time)

ids_and_points_delta_time = delta_time(start_times)


def generate_score(ids_and_points_delta_time):

    score_results_with_ids = []
    for item in ids_and_points_delta_time:
        # print(item[0])
        # print(item[1])
        # print(item[2])
        score = int(item[1]) / (int(item[2]) ** G)
        score_results_with_ids.append([item[0],score])

    print("score with ids : ",score_results_with_ids)

generate_score(ids_and_points_delta_time)
























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
