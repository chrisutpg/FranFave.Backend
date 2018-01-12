import os


# Statement for enabling the development environment
DEBUG = True


# Define the app directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# Turn Off SQL Tracking
SQLALCHEMY_TRACK_MODIFICATIONS = False
# Define for GAE Cloud SQL:
CLOUDSQL_USER = 'postgres'
CLOUDSQL_PASSWORD = 'BhCnutpg1!'
CLOUDSQL_DATABASE = 'franfave'
CLOUDSQL_CONNECTION_NAME = 'franfave-191811:us-central1:franfave'

# Define Live Database
SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@/{database}?host=/cloudsql/{connection_name}'\
                            .format(
                            user=CLOUDSQL_USER, password=CLOUDSQL_PASSWORD,
                            database=CLOUDSQL_DATABASE, connection_name=CLOUDSQL_CONNECTION_NAME)

# Define the LOCAL database
# SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:BhCnutpg1!@35.184.89.176/franfave'
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