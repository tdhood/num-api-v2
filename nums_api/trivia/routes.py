from flask import Blueprint, jsonify
from random import choice
from nums_api.limiter import shared_limit

from nums_api.trivia.models import Trivia


trivia = Blueprint("trivia", __name__)

@trivia.get("/<int:number>")
@shared_limit
def get_num_fact(number):
    """ Returns a random trivia fact in JSON about a number passed as a URL
    parameter.

    If fact is found -->
        {fact: {number, fragment, statement, type}}
    If no fact is found -->
        {error: {status, message}} and a status code 404 is sent
    """

    trivia_instances = (
        Trivia
        .query
        .filter(Trivia.number == number)
        .all())

    # if there are no instances then respond with below
    if not trivia_instances:
        error = {
            'status': 404,
            'message': f'A trivia fact for { number } not found',
        }

        return (jsonify(error=error), 404)

    # picks a random instance from the list
    trivia = choice(trivia_instances)
    fact = {
        'number': trivia.number,
        'fragment': trivia.fact_fragment,
        'statement': trivia.fact_statement,
        'type': 'trivia'
    }

    return jsonify(fact=fact)


@trivia.get("/random")
@shared_limit
def get_num_fact_random():
    """ Returns a random trivia fact in JSON

    Ex: {fact: {number, fragment, statement, type}}
    """

    trivia_instances = Trivia.query.all()

    # picks a random instance from the list
    random_trivia = choice(trivia_instances)
    fact = {
        'number': random_trivia.number,
        'fragment': random_trivia.fact_fragment,
        'statement': random_trivia.fact_statement,
        'type': 'trivia'
    }

    return jsonify(fact=fact)
