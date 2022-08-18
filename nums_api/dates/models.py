from nums_api.database import db
import datetime
from sqlalchemy import event
from ..shared_utils.email_notification import send_emails_to_subscribers



class Date (db.Model):
    """General date facts about numbers"""

    __tablename__ = "dates"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    # 1 - 366 to accommodate for leap years
    day_of_year = db.Column(
        db.Integer,
        nullable=False
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    # fact with no prefix, first word lowercase, no punctuation at the end
    fact_fragment = db.Column(
        db.String(200),
        nullable=False
    )

    # fact with prefix, first word is number, has punctuation at the end
    fact_statement = db.Column(
        db.String(250),
        nullable=False
    )

    was_submitted = db.Column(
        db.Boolean,
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )


    @classmethod
    def date_to_day_of_year(cls, month, day):
        """ A helper function to convert a month and day to the day of year.

            - Takes month and day as integers.
            - Returns day of year as an integer.

            If month or day is out of bounds,
                raises an ValueError with invalid message.

            >>> Date.date_to_day_of_year(2, 28)
            59

            >>> Date.date_to_day_of_year(2, 29)
            60

            >>> Date.date_to_day_of_year(3, 1)
            61

            >>> Date.date_to_day_of_year(12, 31)
            366
        """

        try:
            # Use datetime to convert a given month and day to the day of year.
            # Using 2004 as year, since our model expects day range to always
            # be 1-366 (year itself doesn't matter, just needs to be a leap year).
            # Do not change the year here-- there's no reason to.
            # Resultant day_of_year will be a zero-padded string of integers.
            day_of_year = datetime.datetime(2004, month, day).strftime("%j")

        except ValueError:
            raise ValueError("Invalid month or day")

        # Returns an integer of the string with no leading zeros using lstrip()
        return int(day_of_year.lstrip('0'))

    @classmethod
    def day_to_string(cls, day):
        """ A helper function that converts a day (passed as an integer) to its
                string equivalent using datetime library.

             - Takes day of year as a integer between 1 - 366.
             - Return date as a string like "January 1st"

            >>> Date.day_to_string(1)
            'January 1st'

            >>> Date.day_to_string(59)
            'February 28th'

            >>> Date.day_to_string(3)
            'January 3rd'

            >>> Date.day_to_string(33)
            'February 2nd'
        """

        try:
            # Using datetime function to convert given day of year to month and
            # day. Using 2004 as year, since our model expects day range to
            # always be 1-366 (year itself doesn't matter, just needs to be a
            # leap year). There should not be any reason to change the year.
            # Resultant variable will be a string of the month and day, where
            # the day may include one leading zero, like "January 01"
            date_string = datetime.datetime.strptime("2004" + "-" + str(day),
                "%Y-%j").strftime("%B %d")

        except ValueError:
            raise ValueError("Invalid day of year")

        # removes leading 0 for single digit days
        if date_string[-2] == "0":
            date_string = date_string.replace(date_string[-2], "")

        # adds number suffixes
        if date_string[-1] == "1":
            date_string += "st"
        elif date_string[-1] == "2":
            date_string += "nd"
        elif date_string[-1] == "3":
            date_string += "rd"
        else:
            date_string += "th"

        return date_string
        

class Date_Like(db.Model):

    __tablename__='date_likes'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    date_fact_id = db.Column(
        db.Integer,
        db.ForeignKey('dates.id'),
        default=False,
    )

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
    )

# Event listener decorator
# Calls function when there is an insertion to the the Date table
@event.listens_for(Date, "after_insert")
def listening_for_new_fact(mapper, connection, target):
    """ Calls email sending function
        - Takes:
        mapper, connection and target as required parameters by the decorator
    """
    send_emails_to_subscribers()
