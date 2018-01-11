from werkzeug.security import generate_password_hash, check_password_hash
from models import User, UserProfile, db
from sqlalchemy.exc import IntegrityError
from flask import request
from config import SECRET_KEY
from functools import wraps
import jwt
import datetime



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']
        print(token)
        if not token:
            return {'Err' : 'Token is missing!'}, 401

        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = User.query.filter_by(id=data['id']).first()
        except:
            print('invalid')
            return {'Err' : 'Token is invalid!'}, 401

        return f(current_user, *args, **kwargs)
    return decorated


def create_user(json_data):
    """
    Create a new User
    :param json_data: data from API endpoint auth/create_user
    :return: 201 if added, 500 for an error
    """

    # Get data needed for new user
    email = json_data['email']
    first_name = json_data['first_name']
    last_name = json_data['last_name']

    password = json_data['password']
    # TODO add password strength checking / front end maybe?

    hashed_pass = generate_password_hash(password)

    # If we make it to here, add the biz under biz_user table
    new_user = User(email=email,
                    first_name=first_name,
                    last_name=last_name,
                    password=hashed_pass)

    # Add new_biz to the session for insert
    db.session.add(new_user)

    try:
        db.session.commit()
    except IntegrityError:
        return {'Err' : 'That email already exists!'}, 500

    # Now we need to create a profile for the new_user in the user_profile table
    user_profile = UserProfile(user_id=new_user.id)
    db.session.add(user_profile)

    # Commit the new data to the db
    db.session.commit()
    return {'Created!' : 'New User Was Created!'}, 201


def login_user(json_data):
    """
    Logs in a user and returns a JWT for them to user for the rest of the session
    :param json_data: data from endpoint auth/login_user
    :return: 200 status & JWT if logged in, otherwise 401 and try again
    """

    # Get user data
    email = json_data['email']
    password = json_data['password']

    # check to see if the email is in the db
    user = User.query.filter_by(email=email).first()

    # If we cannot find the user, fail
    if user is None:
        return {'Err' : 'Cannot find an account with that email!'}, 401

    # If user is in DB check the password
    check_pass = check_password_hash(user.password, password)

    # If the password check is incorrect, fail
    if check_pass is False:
        return {'Err' : 'That password is incorrect'}, 401

    # If we are here, credentials are correct, lets get JWT
    token = jwt.encode({'id' : user.id,
                        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                       SECRET_KEY)
    return {'token' : token.decode('UTF-8')}


@token_required
def is_user(current_user):
    print(current_user.id)
    return current_user
