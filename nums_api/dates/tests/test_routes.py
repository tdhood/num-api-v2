from unittest import TestCase

# Importing limiter so we can disable it in the setUp
from nums_api.limiter import limiter

from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.dates.models import Date

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class DateRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Date.query.delete()

        self.d1 = Date(
            day_of_year=1,
            year=2000,
            fact_fragment="the date for this test fragment",
            fact_statement="January 1st in 2000 is the date fact statement.",
            was_submitted=False)

        self.d2 = Date(
            day_of_year=2,
            year=2000,
            fact_fragment="the date for this test fragment",
            fact_statement="January 2nd in 2000 is the date fact statement.",
            was_submitted=False)

        db.session.add_all([self.d1, self.d2])
        db.session.commit()

        limiter.enabled = False

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_date_fact(self):
        """Test for date fact for the number 1"""
        with self.client as c:
            resp = c.get("api/date/1/1")
            data = resp.get_json()

            self.assertEqual(
                data,
                {"fact": {
                    "number": 1,
                    "year": 2000,
                    "fragment": "the date for this test fragment",
                    "statement": "January 1st in 2000 is the date fact statement.",
                    "type": "date"
                }})
            self.assertEqual(resp.status_code, 200)

    def test_get_date_fact_random(self):
        """Test for date fact for random route"""
        with self.client as c:
            d1_fact_data = {"fact": {
                'number': 1,
                'year': 2000,
                'fragment': "the date for this test fragment",
                'statement': "January 1st in 2000 is the date fact statement.",
                'type': 'date'
            }
            }

            d2_fact_data = {"fact": {
                'number': 2,
                'year': 2000,
                'fragment': "the date for this test fragment",
                'statement': "January 2nd in 2000 is the date fact statement.",
                'type': 'date'
            }
            }

            resp = c.get("api/date/random")
            data = resp.get_json()

            self.assertIn(data, [d1_fact_data, d2_fact_data])
            self.assertEqual(resp.status_code, 200)

    def test_error_for_number_with_no_fact(self):
        """Test error for number with no fact"""
        with self.client as c:
            resp = c.get("api/date/3/3")
            data = resp.get_json()

            self.assertEqual(
                data,
                {"error": {
                    "message": "A date fact for 3/3 not found",
                    "status": 404
                }})
            self.assertEqual(resp.status_code, 404)

    def test_error_for_invalid_date(self):
        """Test date fact with an invalid month/day"""
        with self.client as c:
            resp = c.get("api/date/13/1")
            data = resp.get_json()

            self.assertEqual(
                data,
                {"error": {
                    "message": "13/1 is not valid date. Please give valid" +
                    " date in URL.",
                    "status": 400
                }})
            self.assertEqual(resp.status_code, 400)

            resp2 = c.get("api/date/1/100")
            data2 = resp2.get_json()

            self.assertEqual(
                data2,
                {"error": {
                    "message": "1/100 is not valid date. Please give valid" +
                    " date in URL.",
                    "status": 400
                }})
            self.assertEqual(resp2.status_code, 400)

            resp3 = c.get("api/date/2/31")
            data3 = resp3.get_json()

            self.assertEqual(
                data3,
                {"error": {
                    "message": '2/31 is not valid date. Please give' +
                    ' valid date in URL.',
                    "status": 400
                }})
            self.assertEqual(resp3.status_code, 400)
