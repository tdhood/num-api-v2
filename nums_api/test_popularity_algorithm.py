from unittest import TestCase

from nums_api import app

from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST

import nums_api.popularity_algorithm as pa
from nums_api.trivia.models import Trivia, Trivia_Like
from nums_api.maths.models import Math, Math_Like

from datetime import date, datetime

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
        mf1 = Math(
            number=1,
            fact_fragment="the number for this test fact fragment",
            fact_statement="1 is the number for this test fact statement.",
            was_submitted=False,
            timestamp=datetime(2020, 1, 1),
        )

        db.session.add_all([tf1, mf1])
        db.session.commit() 
        cls.tf1 = tf1
        cls.mf1 = mf1

        tl1 = Trivia_Like(trivia_fact_id=cls.tf1.id, timestamp=datetime(2020, 2, 1))
        tl2 = Trivia_Like(trivia_fact_id=cls.tf1.id, timestamp=datetime(2020, 2, 2))
        tl3 = Trivia_Like(trivia_fact_id=cls.tf1.id, timestamp=datetime(2020, 2, 3))
        ml1 = Math_Like(math_fact_id=cls.mf1.id, timestamp=datetime(2020, 2, 1))
        ml2 = Math_Like(math_fact_id=cls.mf1.id, timestamp=datetime(2020, 2, 2))
    
        db.session.add_all([tl1, tl2, tl3, ml1, ml2])
        db.session.commit()

        cls.tl1 = tl1
        cls.tl2 = tl2
        cls.tl3 = tl3
        cls.ml1 = ml1
        cls.ml2 = ml2
        

        cls.client = app.test_client()


    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    @classmethod
    def tearDownClass(cls):
        """Tear down after all tests have ran."""
        Trivia_Like.query.delete()
        Math_Like.query.delete()
        Trivia.query.delete()
        Math.query.delete()
        

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_fetch_points(self):
        """Test fetch_points, expected to return a list of lists representing
        fact's data"""
        self.assertEqual(
            pa.fetch_points(),
            [[self.tf1.id, 3, "trivia"], [self.mf1.id, 2, "math"]],
        )

    def test_fetch_time_of_submission(self):
        """tests fetch_time_of_submission, expected to add a time-submission
        signature to the fact's data in the list of lists """
        self.assertEqual(
            pa.fetch_time_of_submission([[self.tf1.id, 2, "trivia"]]),
            [
                [
                    self.tf1.id,
                    2,
                    datetime(2020, 1, 1, 0, 0),
                    "trivia",
                ]
            ],
        )

    # FIXME: This function returns the change in days based on datetime.utcnow. 
    # Unfortunately, this is changing the expected result as well. Not sure how
    # fix this for correct testing.
    
    # def test_delta_time(self):
    #     """test test_delta_time, expected to calculates the time deference and
    #     adds that to the fact's data in the list of lists  """
    #     import pdb
    #     pdb.set_trace()
    #     self.assertEqual(
    #         pa.delta_time([[self.tf1.id, 2, self.tf1.timestamp, "trivia"]]),
    #         [[1, 2, 960, "trivia"]],
    #     )

    def test_generate_score(self):
        """test generate_score, expected to add a score to the fact's data"""
        self.assertEqual(
            pa.generate_score([[self.tf1.id, 2, 960, "trivia"]]),
            [[self.tf1.id, 0.0020797366042673926, "trivia"]],
        )

    def test_sort_scores(self):
        """returns a sorted list of lists based off of the score of each fact in
        the list of list"""
        self.assertEqual(
            pa.sort_scores([[1,1,'trivia'],[3,5,'trivia'], [2,3,'trivia']]),
            [[3,5,'trivia'], [2,3,'trivia'], [1,1,'trivia']]
        )
