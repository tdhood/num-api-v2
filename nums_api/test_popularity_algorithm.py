from unittest import TestCase

from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST

import nums_api.popularity_algorithm as pa
from nums_api.trivia.models import Trivia, Trivia_Like
from nums_api.maths.models import Math, Math_Like

# from nums_api.years.models import Year, Year_Like
# from nums_api.dates.models import Date, Date_Like
from datetime import datetime

# import pdb
# pdb.set_trace()
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()


class PopularityAlgorithmTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up data for popularity algorithm testing here"""

        tf1 = Trivia(
            number=1,
            fact_fragment="the number for this test fact fragment",
            fact_statement="1 is the number for this test fact statement.",
            was_submitted=False,
            timestamp=datetime(2020, 1, 1),
        )
        tf2 = Trivia(
            number=2,
            fact_fragment="the number for this test fact fragment",
            fact_statement="2 is the number for this test fact statement.",
            was_submitted=False,
            timestamp=datetime(2020, 2, 2),
        )
        mf1 = Math(
            number=1,
            fact_fragment="the number for this test fact fragment",
            fact_statement="1 is the number for this test fact statement.",
            was_submitted=False,
            timestamp=datetime(2020, 1, 1),
        )
        mf2 = Math(
            number=2,
            fact_fragment="the number for this test fact fragment",
            fact_statement="2 is the number for this test fact statement.",
            was_submitted=False,
            timestamp=datetime(2020, 2, 2),
        )
        tl1 = Trivia_Like(trivia_fact_id=1, timestamp=datetime(2020, 2, 1))
        tl2 = Trivia_Like(trivia_fact_id=1, timestamp=datetime(2020, 2, 2))
        tl3 = Trivia_Like(trivia_fact_id=1, timestamp=datetime(2020, 2, 3))
        tl4 = Trivia_Like(trivia_fact_id=2, timestamp=datetime(2020, 2, 4))
        ml1 = Math_Like(math_fact_id=1, timestamp=datetime(2020, 2, 1))
        ml2 = Math_Like(math_fact_id=1, timestamp=datetime(2020, 2, 2))
        ml3 = Math_Like(math_fact_id=2, timestamp=datetime(2020, 2, 3))

        db.session.add_all([tf1, tf2, mf1, mf2, tl1, tl2, tl3, tl4, ml1, ml2, ml3])
        db.session.commit()

        cls.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_fetch_points(self):
        """Test fetch_points, expected to return a list of lists representing
        fact's data"""
        self.assertEquals(
            pa.fetch_points(),
            [[2, 1, "trivia"], [1, 3, "trivia"], [2, 1, "math"], [1, 2, "math"]],
        )

    def test_fetch_time_of_submission(self):
        """tests fetch_time_of_submission, expected to add a time-submission
        signature to the fact's data in the list of lists """
        self.assertEquals(
            pa.fetch_time_of_submission([[1, 2, "trivia"]]),
            [
                [
                    1,
                    2,
                    datetime(2020, 1, 1, 0, 0),
                    "trivia",
                ]
            ],
        )

    def test_delta_time(self):
        """test test_delta_time, expected to calculates the time deference and
        adds that to the fact's data in the list of lists  """
        self.assertEquals(
            pa.delta_time([[1, 2, datetime(2020, 1, 1, 0, 0), "trivia"]]),
            [[1, 2, 960, "trivia"]],
        )

    def test_generate_score(self):
        """test generate_score, expected to add a score to the fact's data"""
        self.assertEquals(
            pa.generate_score([[1, 2, 960, "trivia"]]),
            [[1, 0.0020797366042673926, "trivia"]],
        )

    def test_sort_scores(self):
        """returns a sorted list of lists based off of the score of each fact in
        the list of list"""
        self.assertEquals(
            pa.sort_scores([[1,1,'trivia'],[1,5,'trivia'], [1,3,'trivia']]),
            [[1,5,'trivia'], [1,3,'trivia'], [1,1,'trivia']]
        )
