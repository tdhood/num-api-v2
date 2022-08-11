from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Create instance of api rate-limiter. Limits each IP address's requests to
# the application limits. These limits are shared across the entire site for
# all endpoints.
limiter = Limiter(
key_func=get_remote_address,
)

def determine_limit():
    """ Checks if there is TEST environmental variable key.
        If so, returns '1/hour'. If not, returns '200/day;50/hour' 
    """
    if os.environ.get("TEST"):
        return '1/hour'
    
    return '200/day;50/day'

# Creating a shared_limit based on if the app is being ran in a testing
# environment or development environment. @shared_limit decorator needs to be
# added to all routes that are to be rate limited.
shared_limit = limiter.shared_limit(determine_limit, scope = "api_limit")


