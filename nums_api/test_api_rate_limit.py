from unittest import TestCase

# Setting TEST environmental variable so that rate limit is set to 1/hour.
# This way, we don't have to make as many API calls to test the limiter.
import os
os.environ["TEST"]='testing'

# Importing limiter so we can enable it in the setUp
from nums_api.limiter import limiter

from nums_api import app

from nums_api.database import db
from nums_api.config import DATABASE_URL_TEST

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL_TEST
app.config["TESTING"] = True
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.drop_all()
db.create_all()

class ApiRateLimitTestCase(TestCase):
    def setUp(self):
        """Set up test data here"""
        self.client = app.test_client()

        limiter.enabled = True
        limiter.reset()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_setup(self):
        """Test to make sure tests are set up correctly"""
        test_setup_correct = True
        self.assertEqual(test_setup_correct, True)

    def test_api_rate_limit(self):
        """Test to make sure that a route gets blocked if requested too
            many times"""
        resp = self.client.get('/api/year/1')

        self.assertEqual(404, resp.status_code)

        resp = self.client.get('/api/year/1')

        self.assertEqual(429, resp.status_code)

        resp2 = self.client.get('/api/math/1')

        self.assertEqual(429, resp2.status_code)

    def test_root_route_not_blocked(self):
        """Test to make sure that the root route is exempt from rate limit."""
        resp = self.client.get('/')

        self.assertEqual(200, resp.status_code)

        resp = self.client.get('/')

        self.assertEqual(200, resp.status_code)
