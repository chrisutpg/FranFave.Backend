from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64),  nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    registered_on = db.Column(db.DateTime, default=datetime.now(), nullable=False)


class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    phone1 = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(128), nullable=True)
    address_city = db.Column(db.String(128), nullable=True)
    address_state = db.Column(db.String(128), nullable=True)
    address_zip = db.Column(db.String(128), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)


class Place(db.Model):
    __tablename__ = 'place'
    id = db.Column(db.Integer, primary_key=True)
    gid = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    phone1 = db.Column(db.String(10), nullable=True)
    address = db.Column(db.String(128), nullable=False)
    address_city = db.Column(db.String(128), nullable=False)
    address_state = db.Column(db.String(2), nullable=False)
    address_zip = db.Column(db.String(5), nullable=False)
    address_country = db.Column(db.String(64), nullable=False)


class Reviews(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    review_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    visited_date = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    cat_1 = db.Column(db.Integer, nullable=False)
    cat_2 = db.Column(db.Integer, nullable=False)
    cat_3 = db.Column(db.Integer, nullable=False)
    cat_4 = db.Column(db.Integer, nullable=False)
    cat_5 = db.Column(db.Integer, nullable=False)
    review_avg = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String(), nullable=True)
