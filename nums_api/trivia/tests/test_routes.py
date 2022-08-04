from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.trivia.models import Trivia

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()


class TriviaRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Trivia.query.delete()

        self.t1 = Trivia(
            number=1,
            fact_fragment="the number for this test fact fragment",
            fact_statement="1 is the number for this test fact statement.",
            was_submitted=False
        )

        self.t2 = Trivia(
            number=2,
            fact_fragment="the number for this test fact fragment",
            fact_statement="2 is the number for this test fact statement.",
            was_submitted=False
        )

        db.session.add_all([self.t1, self.t2])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_trivia_fact(self):
        """Test for trivia fact for the number 1"""
        with self.client as c:
            resp = c.get("api/trivia/1")
            data = resp.get_json()

            self.assertEqual(
                data,
                {'fact': {
                    'fragment': 'the number for this test fact fragment',
                    'number': 1,
                    'statement': '1 is the number for this test fact statement.',
                    'type': 'trivia',
                }})
            self.assertEqual(resp.status_code, 200)

    def test_error_for_number_with_no_fact(self):
        """Test error for number with no fact"""
        with self.client as c:
            resp = c.get(f"api/trivia/3")
            data = resp.get_json()

            self.assertEqual(
                data,
                {'error': {
                    'status': 404,
                    'message': 'A trivia fact for 3 not found',
                }})
            self.assertEqual(resp.status_code, 404)

    def test_get_trivia_random_fact(self):
        """Test for trivia fact for random route"""
        with self.client as c:
            t1_fact_data = c.get("api/trivia/1").get_json()
            t2_fact_data = c.get("api/trivia/2").get_json()

            resp = c.get("api/trivia/random")
            data = resp.get_json()

            self.assertIn(data, [t1_fact_data, t2_fact_data])
            self.assertEqual(resp.status_code, 200)

    def test_get_trivia_fact_invalid_num(self):
        """Test for trivia fact with an invalid number"""
        with self.client as c:
            resp = c.get("api/trivia/hello")

            self.assertEqual(resp.status_code, 404)
