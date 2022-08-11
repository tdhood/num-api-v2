from unittest import TestCase

# Importing limiter so we can disable it in the setUp
from nums_api.limiter import limiter

from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.years.models import Year

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()


class YearRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Year.query.delete()

        self.y1 = Year(
            number=1,
            fact_fragment="the number for this test fact fragment",
            fact_statement="1 is the number for this test fact statement.",
            was_submitted=False
        )

        self.y2 = Year(
            number=2,
            fact_fragment="the number for this test fact fragment",
            fact_statement="2 is the number for this test fact statement.",
            was_submitted=False
        )

        db.session.add_all([self.y1, self.y2])
        db.session.commit()

        limiter.enabled = False

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_year_fact(self):
        """Test for year fact for the number 1"""
        with self.client as c:
            resp = c.get("api/year/1")
            data = resp.get_json()

            self.assertEqual(
                data,
                {'fact': {
                    'fragment': 'the number for this test fact fragment',
                    'number': 1,
                    'statement': '1 is the number for this test fact statement.',
                    'type': 'year',
                }})
            self.assertEqual(resp.status_code, 200)

    def test_error_for_number_with_no_fact(self):
        """Test error for number with no fact"""
        with self.client as c:
            resp = c.get(f"api/year/3")
            data = resp.get_json()

            self.assertEqual(
                data,
                {'error': {
                    'status': 404,
                    'message': 'A year fact for 3 not found',
                }})
            self.assertEqual(resp.status_code, 404)

    def test_get_year_random_fact(self):
        """Test for year fact for random route"""
        with self.client as c:
            y1_fact_data = c.get("api/year/1").get_json()
            y2_fact_data = c.get("api/year/2").get_json()

            resp = c.get("api/year/random")
            data = resp.get_json()

            self.assertIn(data, [y1_fact_data, y2_fact_data])
            self.assertEqual(resp.status_code, 200)

    def test_get_year_fact_invalid_num(self):
        """Test for year fact with an invalid number"""
        with self.client as c:
            resp = c.get("api/year/hello")

            self.assertEqual(resp.status_code, 404)
