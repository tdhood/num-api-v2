from flask import Blueprint, jsonify
from random import choice
from nums_api.limiter import shared_limit

from nums_api.years.models import Year

years = Blueprint("years", __name__)


@years.get("/<int:year>")
@shared_limit
def get_num_fact(year):
    """Returns a random year fact in JSON about a year passed as a URL
    parameter.

    If fact is found -->
        {fact: {number, fragment, statement, type}}
    If no fact is found -->
        {error: {status, message}} and a status code 404 is sent
    """

    year_instances = Year.query.filter(Year.number == year).all()

    if not year_instances:
        error = {
            "status": 404,
            "message": f"A year fact for { year } not found",
        }

        return (jsonify(error=error), 404)

    # picks a random instance from the list
    year = choice(year_instances)
    fact = {
        'number': year.number,
        'fragment': year.fact_fragment,
        'statement': year.fact_statement,
        'type': 'year'
    }

    return jsonify(fact=fact)


@years.get("/random")
@shared_limit
def get_num_fact_random():
    """ Returns a random year fact in JSON

    Ex: {fact: {number, fragment, statement, type}}
    """

    year_instances = Year.query.all()

    # picks a random instance from the list
    random_year = choice(year_instances)
    fact = {
        'number': random_year.number,
        'fragment': random_year.fact_fragment,
        'statement': random_year.fact_statement,
        'type': 'year'
    }

    return jsonify(fact=fact)
