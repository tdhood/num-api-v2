from datetime import datetime
from operator import itemgetter
from sqlalchemy import func
from nums_api.trivia.models import Trivia, Trivia_Like
from nums_api.maths.models import Math, Math_Like
from nums_api.years.models import Year, Year_Like
from nums_api.dates.models import Date, Date_Like


CURRENT_TIME = datetime.utcnow()
G = 1.00002


# Popularity algorithm:
# Score = (P) / (T+2)^G

# where,
# P = points of an item
# T = time since submission (in days)
# G = Gravity, defaults to 1.00002 in news.arc


def fetch_points():
    """Function queries each category_likes database.
    Totals all the likes for each fact_id as points.
    Returns an array of array (id, total points, category)
      // [(3,1,'trivia'),...]
    """

    id_points_category = []

    trivia_points = (
        Trivia_Like.query.with_entities(
            Trivia_Like.trivia_fact_id, func.count(Trivia_Like.trivia_fact_id)
        )
        .group_by(Trivia_Like.trivia_fact_id)
        .all()
    )
    for tuple in trivia_points:
        id_points_category.append([*tuple, "trivia"])

    math_points = (
        Math_Like.query.with_entities(
            Math_Like.math_fact_id, func.count(Math_Like.math_fact_id)
        )
        .group_by(Math_Like.math_fact_id)
        .all()
    )
    for tuple in math_points:
        id_points_category.append([*tuple, "math"])

    years_points = (
        Year_Like.query.with_entities(
            Year_Like.year_fact_id, func.count(Year_Like.year_fact_id)
        )
        .group_by(Year_Like.year_fact_id)
        .all()
    )
    for tuple in years_points:
        print(tuple)
        id_points_category.append([*tuple, "year"])

    date_points = (
        Date_Like.query.with_entities(
            Date_Like.date_fact_id, func.count(Date_Like.date_fact_id)
        )
        .group_by(Date_Like.date_fact_id)
        .all()
    )
    for tuple in date_points:
        print(tuple)
        id_points_category.append([*tuple, "date"])

    print("id_points_category ", id_points_category)
    return id_points_category


id_points_category = fetch_points()


def fetch_time_of_submission(id_points_category):
    """Takes an array of arrays like [[fact_id, points, category],...]

    Returns an array of arrays like
        [[fact_id, points, initial fact timestamp, category]]

    """

    ids_points_starttimes_category = []

    for item in id_points_category:
        if item[2] == "trivia":
            fact_submission_time = Trivia.query.get(item[0])
            ids_points_starttimes_category.append(
                [item[0], item[1], fact_submission_time.timestamp, item[2]]
            )

        if item[2] == "math":
            fact_submission_time = Math.query.get(item[0])
            ids_points_starttimes_category.append(
                [item[0], item[1], fact_submission_time.timestamp, item[2]]
            )

        if item[2] == "year":
            fact_submission_time = Year.query.get(item[0])
            ids_points_starttimes_category.append(
                [item[0], item[1], fact_submission_time.timestamp, item[2]]
            )

        if item[2] == "date":
            fact_submission_time = Date.query.get(item[0])
            ids_points_starttimes_category.append(
                [item[0], item[1], fact_submission_time.timestamp, item[2]]
            )

    print("ids_points_starttimes_category", ids_points_starttimes_category)
    return ids_points_starttimes_category


ids_points_starttimes_category = fetch_time_of_submission(id_points_category)


def delta_time(ids_points_starttimes_category):
    """Takes an array of [[fact_id, points, initial fact timestamp, category], ...]
    Calculates the time difference from initial fact timestamp to Current_Time

    Returns [[fact_id, points, delta_time, category], ...]
    """

    ids_points_deltatime_category = []

    for item in ids_points_starttimes_category:
        delta = CURRENT_TIME - item[2]
        ids_points_deltatime_category.append(
            [item[0], item[1], delta.days, item[3]])
    print("delta times : ", ids_points_deltatime_category)
    return ids_points_deltatime_category


ids_points_deltatime_category = delta_time(ids_points_starttimes_category)


def generate_score(ids_points_deltatime_category):
    """Takes an array like [[fact_id, points, delta_time, category], ...]
        Calculates the Score using Popularity algorithm

        Returns array like [[fact_id, score, category], ...]
    """

    id_score_category = []
    for item in ids_points_deltatime_category:
        score = int(item[1]) / (int(item[2]) ** G)
        id_score_category.append([item[0],score, item[3]])

    print("score with ids : ",id_score_category)
    return id_score_category

id_score_category = generate_score(ids_points_deltatime_category)

def sort_scores(id_score_category):
    """Takes an array like [[fact_id, score, category], ...]

        Sorts array based on score

    """
    sorted_id_score_category = (sorted(
        id_score_category, key=itemgetter(1), reverse=True))

    print("sorted_id_score_category", sorted_id_score_category[:10])

    return sorted_id_score_category[:10]

sort_scores(id_score_category)
