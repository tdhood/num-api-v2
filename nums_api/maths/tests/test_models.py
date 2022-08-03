from unittest import TestCase
from nums_api import app
from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST
from nums_api.maths.models import Maths

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.drop_all()
db.create_all()

class MathModelTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""

        Maths.query.delete()

        self.t1 = Maths(
            number=1,
            fact_fragment="the number for this test fact fragment",
            fact_statement="1 is the number for this test fact statement.",
            pos='DET',
            includes_self=False
        )

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_model(self):
        """Test Math model added to database successfully"""
        self.assertIsInstance(self.t1, Maths)
        self.assertEqual(Maths.query.count(), 0)

        db.session.add(self.t1)
        db.session.commit()

        self.assertEqual(Maths.query.count(), 1)
        self.assertEqual(Maths.query.filter_by(number=1).one().number, 1)
