from flask import Blueprint, jsonify
from random import choice
from nums_api.limiter import shared_limit

from nums_api.maths.models import Math


math = Blueprint("math", __name__)


@math.get("/<int:number>")
@shared_limit
def get_num_fact(number):
    """ Returns a random math fact in JSON about a number passed as a URL
    parameter.

    If fact is found -->
        {fact: {number, fragment, statement, type}}
    If no fact is found -->
        {error: {status, message}} and a status code 404 is sent
    """

    math_instances = (
        Math
        .query
        .filter(Math.number == number)
        .all())

    # if there are no instances then respond with below
    if not math_instances:
        error = {
            'status': 404,
            'message': f'A math fact for { number } not found',
        }

        return (jsonify(error=error), 404)

    # picks a random instance from the list
    math = choice(math_instances)
    fact = {
        'number': math.number,
        'fragment': math.fact_fragment,
        'statement': math.fact_statement,
        'type': 'math'
    }

    return jsonify(fact=fact)


@math.get("/random")
@shared_limit
def get_num_fact_random():
    """ Returns a random math fact in JSON

    Ex: {fact: {number, fragment, statement, type}}
    """

    math_instances = Math.query.all()

    # picks a random instance from the list
    random_math = choice(math_instances)
    fact = {
        'number': random_math.number,
        'fragment': random_math.fact_fragment,
        'statement': random_math.fact_statement,
        'type': 'math'
    }

    return jsonify(fact=fact)
