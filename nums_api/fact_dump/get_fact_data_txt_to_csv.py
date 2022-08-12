import json
import csv
from csv import reader
import os
import sys

# Natural Language Toolkit Library
# POS tag examples DT:determiner, NNP:proper noun singular, VB:verb, JJ:adjective,
# # NN:noun singular
# NOTE: If you need to run this script, the NLTK libraries: PUNKT and
# AVERAGED_PERCEPTRON_TAGGER will be installed!
import nltk

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")
print('Generating Data File...')

# NOTE: This script currently for use with only the following models:
# - Trivia, Math, Year
# - Date is a TODO

"""Use script to generate file paths when new txt files are added to a category.

These files are opened, the data is is parsed and written to a csv file:
(fact_record_modified.csv)

Run this script from the top level Numbers_API_V2/ directory like:
python3 nums_api/fact_dump/get_facts.py
"""

PATHS_AND_CATEGORIES = []


def file_path_builder():
    """Builds a file path for files added to the fact_dump/category folder
    Appends [filepath, type] to PATHS_AND_CATEGORIES
    """

    categories = ["trivia", "math", "year"]

    for category in categories:
        category_raw_path = os.path.join(sys.path[0], category)
        for filename in os.listdir(category_raw_path):
            PATHS_AND_CATEGORIES.append(
                [f"nums_api/fact_dump/{category}/{filename}", category]
            )


file_path_builder()


def get_words_tags(str):
    """Tag words with its lexical category.
    takes string (fact_fragment) like: "is a prime number"
    returns list like: ['is', 'VB']"""

    text = nltk.word_tokenize(str)
    word_tags = nltk.pos_tag(text)
    return [(word, tag) for word, tag in word_tags]


# creates fact_record.csv from all raw data text files
# creates pos tags for first word in fact_fragment
# currently was_submitted default sets to False, would need to update for
# user submitted data text files
header = ["type", "pos", "number", "fact_fragment", "was_submitted"]

with open("fact_record.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for path, category in PATHS_AND_CATEGORIES:
        with open(path, "r") as fact_file:
            fact_data = json.load(fact_file)

            for number in fact_data:
                for fact_dict in fact_data[number]:
                    words_tags = get_words_tags(fact_dict["text"])

                    fact_record = [
                        category,
                        words_tags[0][1],
                        number,
                        fact_dict['text'],
                        False,
                    ]

                    writer.writerow(fact_record)

# creates fact_record_modified.csv
# cleans up fact_fragments for generating fact_statements
# This file needs to be reviewed and cleaned up manually before running the
# add_facts_to_database.py script
header = ["category", "pos", "number",
          "fact_statement", "fact_fragment", "was_submitted"]

with open("fact_record_modified.csv", "w", encoding="UTF8") as f:
    writer = csv.writer(f)
    writer.writerow(header)

    with open("fact_record.csv", "r", encoding="UTF8") as r:
        csv_reader = reader(r)
        header = next(csv_reader)

        for row in csv_reader:
            category = row[0]
            pos = row[1]
            number = row[2]
            fact_fragment = row[3]
            was_submitted = row[4]
            fact_statement = ''

            if len(fact_fragment) < 200:
                if fact_fragment[-1] not in [".", "!", "?"]:
                    fact_fragment = fact_fragment + '.'

                if pos != 'NNP':
                    fact_fragment = fact_fragment[0].lower() + fact_fragment[1:]

                if category == 'trivia':
                    fact_statement = f"{number} is the number of {fact_fragment}"

                if category == 'math':
                    fact_statement = f"{number} is {fact_fragment}"

                if category == 'year':
                    year_number = ""
                    if number.startswith("-"):
                        year_number = number[1:] + " BC"
                    else:
                        year_number = number
                    fact_statement = f"{year_number} is the year that {fact_fragment}"

                modified_fact_record = [
                    category,
                    pos,
                    number,
                    fact_statement,
                    fact_fragment,
                    was_submitted,
                ]

                writer.writerow(modified_fact_record)
