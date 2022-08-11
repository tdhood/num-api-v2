from flask import Blueprint, jsonify
from nums_api.limiter import shared_limit
from random import choice
from nums_api.dates.models import Date

dates = Blueprint("dates", __name__)


@dates.get("/<int:month>/<int:day>")
@shared_limit
def get_num_fact(month, day):
    """ Returns a random date fact in JSON about a month/day passed as a URL
    parameter.

    If fact is found -->
        {fact: {number, year, fragment, statement, type}}
    If no fact is found -->
        {error: {status, message}} and a status code 404 is sent
    If month/day is invalid -->
        {error: {status, message}} and a status code 400 is sent
    """

    day_of_year = None

    try:
        day_of_year = Date.date_to_day_of_year(month,day)

    except ValueError:
        error = {
            'status': 400,
            'message': f'{ month }/{ day } is not valid date. Please give' +
            ' valid date in URL.',
        }
        return (jsonify(error=error), 400)

    date_instances = (
        Date
        .query
        .filter(Date.day_of_year == day_of_year)
        .all()
    )

    # if there are no instances then respond with below
    if not date_instances:
        error = {
            'status': 404,
            'message': f'A date fact for { month }/{ day } not found',
        }

        return (jsonify(error=error), 404)

    # picks a random instance from the list
    random_date = choice(date_instances)
    fact = {
        'number': random_date.day_of_year,
        'year': random_date.year,
        'fragment': random_date.fact_fragment,
        'statement': random_date.fact_statement,
        'type': 'date'
    }

    return jsonify(fact=fact)


@dates.get("/random")
@shared_limit
def get_num_fact_random():
    """ Returns a random date fact in JSON

    Ex: {fact: {number, year, fragment, statement, type}}
    """
    
    date_instances = Date.query.all()

    # picks a random instance from the list
    random_date = choice(date_instances)
    fact = {
        'number': random_date.day_of_year,
        'year': random_date.year,
        'fragment': random_date.fact_fragment,
        'statement': random_date.fact_statement,
        'type': 'date'
    }

    return jsonify(fact=fact)
