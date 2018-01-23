from flask import Flask
from flask_mail import Mail
from flask_cors import CORS
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from api import api
from models import *


# Define the WSGI application object
app = Flask(__name__)


# CORS support for AngularJS Development
CORS(app, origins=['*'])


# Init api
api.init_app(app)


# Configurations
app.config.from_object('config')


# Start the Mails
mail = Mail(app)


# Define the database object
db.init_app(app)


# Get migrate going for database
migrate = Migrate(app, db)


# Add CLI for migrate
manager = Manager(app)
manager.add_command('db', MigrateCommand)


# Add some Blueprints
from views.test import test1 as test
from views.test import search as test2
app.register_blueprint(test)
app.register_blueprint(test2)