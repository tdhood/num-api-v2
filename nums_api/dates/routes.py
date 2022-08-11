from flask import Blueprint
from nums_api.limiter import shared_limit

dates = Blueprint("dates", __name__)


@dates.get("/<month>/<day>")
@shared_limit
def get_num_fact(month, day):
    """FIXME
    Stub route for getting fact about date
    """

    return f"Some interesting fact about the date {month}/{day}."


@dates.get("/random")
@shared_limit
def get_num_fact_random():
    """FIXME
    Stub route for getting fact about random date
    """

    return "Some interesting fact about a random date."
