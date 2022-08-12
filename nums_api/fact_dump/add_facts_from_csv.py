from csv import reader
from nums_api.database import db
from nums_api.trivia.models import Trivia
from nums_api.maths.models import Math
from nums_api.years.models import Year


# NOTE: This script currently for use with only the following models:
# - Trivia, Math, Year
# - Date is a TODO

# Set csv file to import facts from here
# File structure should be:
#   category, pos, number, fact_statement, fact_fragment, was_submitted
FILE = "fact_record_modified.csv"
print("Importing Data...")

# reads fact_record_modified.csv
# creates instances of each category model and adds them to database
with open(FILE, "r", encoding="UTF8") as r:
    csv_reader = reader(r)
    header = next(csv_reader)

    for row in csv_reader:
        category = row[0]
        pos = row[1]
        number = row[2]
        fact_statement = row[3]
        fact_fragment = row[4]
        was_submitted = bool(row[5])

        fact_instance = ""

        if category == "trivia":
            fact_instance = Trivia(
                number=number,
                fact_fragment=fact_fragment,
                fact_statement=fact_statement,
                was_submitted=was_submitted,
            )
            db.session.add(fact_instance)

        if category == "math":
            fact_instance = Math(
                number=number,
                fact_fragment=fact_fragment,
                fact_statement=fact_statement,
                was_submitted=was_submitted,
            )
            db.session.add(fact_instance)

        if category == "year":
            fact_instance = Year(
                number=number,
                fact_fragment=fact_fragment,
                fact_statement=fact_statement,
                was_submitted=was_submitted,
            )
            db.session.add(fact_instance)

    db.session.commit()
