from flask import Flask
from flask_cors import CORS
import os
from flask_debugtoolbar import DebugToolbarExtension

from nums_api.config import DATABASE_URL, SECRET_KEY
from nums_api.database import connect_db
from nums_api.trivia.routes import trivia
from nums_api.maths.routes import math
from nums_api.dates.routes import dates
from nums_api.years.routes import years
from nums_api.root.routes import root

from nums_api.limiter import limiter
from nums_api.shared_utils.email_notification import mail

# create app and add configuration
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# links and initializes the limiter for the app
limiter.app = app
limiter.init_app(app)

# Configures how the Mail instance will be sending emails using SMTP gmail.
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = os.environ['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail.init_app(app)

# register blueprints
app.register_blueprint(root)
app.register_blueprint(trivia, url_prefix='/api/trivia')
app.register_blueprint(math, url_prefix='/api/math')
app.register_blueprint(dates, url_prefix='/api/date')
app.register_blueprint(years, url_prefix='/api/year')

# allow CORS and connect app to database
CORS(app)
connect_db(app)
