import os


# Statement for enabling the development environment
DEBUG = True


# Define the app directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Define the database
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:mdhsgolf1@localhost/ultrafran'
DATABASE_CONNECT_OPTIONS = {}


# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True


# Use a secure, unique and absolutely secret key for signing the data.
CSRF_SESSION_KEY = "secret"


# Secret key for signing cookies
SECRET_KEY = "secret"


# Config for API token authorizations
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-KEY'
    }
}