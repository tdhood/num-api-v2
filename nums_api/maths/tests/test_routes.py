from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Math

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()


class MathRouteTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        Math.query.delete()

        self.m1 = Math(
            number=1,
            fact_fragment="the number for this test fact fragment",
            fact_statement="1 is the number for this test fact statement.",
            was_submitted=False)

        self.m2 = Math(
            number=2,
            fact_fragment="the number for this test fact fragment",
            fact_statement="2 is the number for this test fact statement.",
            was_submitted=False)

        db.session.add_all([self.m1, self.m2])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_get_math_fact(self):
        """Test for math fact for the number 1"""
        with self.client as c:
            resp = c.get("api/math/1")
            data = resp.get_json()

            self.assertEqual(
                data,
                {"fact": {
                    "number": 1,
                    "fragment": "the number for this test fact fragment",
                    "statement": "1 is the number for this test fact statement.",
                    "type": "math"
                }})
            self.assertEqual(resp.status_code, 200)

    def test_error_for_number_with_no_fact(self):
        """Test error for number with no fact"""
        with self.client as c:
            resp = c.get("api/math/3")
            data = resp.get_json()

            self.assertEqual(
                data,
                {"error": {
                    "message": "A math fact for 3 not found",
                    "status": 404
                }})
            self.assertEqual(resp.status_code, 404)

    def test_get_math_fact_random(self):
        """Test for math fact for random route"""
        with self.client as c:
            m1_fact_data = c.get("api/math/1").get_json()
            m2_fact_data = c.get("api/math/2").get_json()

            resp = c.get("api/math/random")
            data = resp.get_json()

            self.assertIn(data, [m1_fact_data, m2_fact_data])
            self.assertEqual(resp.status_code, 200)

    def test_get_num_fact(self):
        """Test math fact with an invalid number"""
        with self.client as c:
            resp = c.get("/rando")

            self.assertEqual(resp.status_code, 404)
