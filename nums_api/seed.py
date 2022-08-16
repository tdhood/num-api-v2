from nums_api import app
from nums_api.database import db
from nums_api.trivia.models import Trivia
from nums_api.maths.models import Math
from nums_api.years.models import Year
from nums_api.dates.models import Date
from random import randint, choice

# Quantity of dummy data to generate in each table.
NUMBER_OF_ENTRIES = 300

DEFAULT_FACTS = ["is a random number",
                 "is a boring number",
                 "is a generic number",
                 "is a number"]

# Containers to keep track of added number facts
# each element in a set is unique.
TRIVIA_SET = set()
MATH_SET = set()
YEAR_SET = set()
DATE_SET = set()

db.drop_all(app=app)
db.create_all(app=app)

############################## Helper Functions ##############################


def create_trivia_instance(number):
    """ Creates trivia instance to place in the Trivia table
        - Takes a number
        - Ensures that no duplicate fact for a single number is created.
        - Returns a trivia instance or none if number fact already exists
    """

    # creates a random number as an addition to the fact statement to ensure
    # that each fact created is unique
    random_addition = randint(0, 300)

    # trivia fragment from default choices
    trivia_fragment = choice(DEFAULT_FACTS)

    statement = f"{number} {trivia_fragment} {random_addition}"

    if statement not in TRIVIA_SET:

        TRIVIA_SET.add(statement)

        trivia_instance = Trivia(
            number=number,
            fact_fragment=trivia_fragment,
            fact_statement=statement,
            was_submitted=False
        )

        return trivia_instance


def create_math_instance(number):
    """ Creates a math instance to place in the Math table
        - Takes a number
        - Ensures that no duplicate fact for a single number is created.
        - Returns a math instance or none if number fact already exists
    """

    # creates a random number as an addition to the fact statement to ensure
    # that each fact created is unique
    random_addition = randint(0, 300)

    # math fragment from default choices
    math_fragment = choice(DEFAULT_FACTS)

    statement = f"{number} {math_fragment} {random_addition}"

    if statement not in MATH_SET:

        MATH_SET.add(statement)

        math_instance = Math(
            number=number,
            fact_fragment=math_fragment,
            fact_statement=statement,
            was_submitted=False
        )

        return math_instance


def create_year_instance(number):
    """ Creates a year instance to place in the Year table
        - Takes a number
        - Ensures that no duplicate fact for a year is created.
        - Returns a year instance or none if number fact already exists
    """

    # creates a random number as an addition to the fact statement to ensure
    # that each fact created is unique
    random_addition = randint(0, 300)

    # year fragment from default choices
    year_fragment = choice(DEFAULT_FACTS)

    statement = f"{number} {year_fragment} {random_addition}"

    if statement not in YEAR_SET:

        YEAR_SET.add(statement)

        year_instance = Year(
            number=number,
            fact_fragment=year_fragment,
            fact_statement=statement,
            was_submitted=False
        )

        return year_instance


def create_date_instance(number):
    """ Creates a date instance to place in the Date table
        - Takes a number
        - Ensures that no duplicate fact for a date is created.
        - Returns a date instance or none if number fact already exists
    """
    # creates a random number as an addition to the fact statement to ensure
    # that each fact created is unique
    random_addition = randint(0, 300)

    # random year from from 1900-2022
    random_year = randint(1900, 2022)

    statement = f"{Date.day_to_string(number)} is the day in {random_year} test date statement {random_addition}."

    if statement not in DATE_SET:

        DATE_SET.add(statement)

        date_instance = Date(
            day_of_year=number,
            year=random_year,
            fact_fragment=f"is the day in {random_year} test date fragment",
            fact_statement=statement,
            was_submitted=False
        )

        return date_instance


def generate_multiple_facts():
    """ Generates an additional fact for a single number in each table
         - Picks 5 numbers to make duplicate facts for each table
         - Adds an additional fact to each number picked to the database.
         - Guarantees that some numbers have multiple facts.
    """
    # queries five records from each table to generate additional facts
    trivia_instances = Trivia.query.limit(5).all()
    year_instances = Year.query.limit(5).all()
    math_instances = Math.query.limit(5).all()

    for number in [instance.number for instance in trivia_instances]:
        additional_fact = Trivia(
            number=number,
            fact_fragment="ADDITIONAL FACT FOR",
            fact_statement=f"ADDITIONAL FACT FOR {number}",
            was_submitted=False
        )
        db.session.add(additional_fact)

    for number in [instance.number for instance in year_instances]:
        additional_fact = Year(
            number=number,
            fact_fragment="ADDITIONAL FACT FOR",
            fact_statement=f"ADDITIONAL FACT FOR {number}",
            was_submitted=False
        )
        db.session.add(additional_fact)

    for number in [instance.number for instance in math_instances]:
        additional_fact = Math(
            number=number,
            fact_fragment="ADDITIONAL FACT FOR",
            fact_statement=f"ADDITIONAL FACT FOR {number}",
            was_submitted=False
        )
        db.session.add(additional_fact)

    db.session.commit()

############################# Main Function ###################################


def generate_dummy_data():
    """ Main function call to generate bulk dummy data """
    for num in range(0, NUMBER_OF_ENTRIES):

        # Picks a random number to generate a fact
        random_num = randint(0, 9999)

        trivia = create_trivia_instance(random_num)
        math = create_math_instance(random_num)
        year = create_year_instance(random_num)

        # excludes 0 because there is no zeroth day in a year.
        if random_num != 0 and random_num < 367:
            date = create_date_instance(random_num)
            db.session.add(date)

        if math:
            db.session.add(math)

        if trivia:
            db.session.add(trivia)

        if year:
            db.session.add(year)

    db.session.commit()

    # ensures that there are a handful of numbers have more than one fact
    generate_multiple_facts()


generate_dummy_data()
