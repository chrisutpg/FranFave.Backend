from flask_restplus import Namespace, Resource, fields, Api
from core.auth import create_user, login_user, is_user


api = Namespace('Auth', description='Create & Authenticate a User')
apiObject = Api()

user_model = api.model('User',
                       {'email': fields.String(required=True, description='Email Address'),
                        'first_name': fields.String(required=True, description='First Name'),
                        'last_name': fields.String(required=True, description='Last Name'),
                        'password': fields.String(required=True, description='A Password'),
                        })

login_model = api.model('Login User',
                        {'email': fields.String(required=True, description='Email Address'),
                         'password': fields.String(required=True, description='A Password'),
                         })

# API to create a new user
@api.route('/create_user')
class User(Resource):

    # API endpoint to create a new user, takes in user_model
    @api.expect(user_model)
    def post(self):
        print(apiObject.payload)
        resp = create_user(apiObject.payload)
        return resp


# API to log in a user
@api.route('/login_user')
class UserLogin(Resource):

    # API endpoint to login a user
    @api.expect(login_model)
    def post(self):
        print('test')
        print(apiObject.payload)
        resp = login_user(apiObject.payload)
        return resp


# API to check if the current visitor is a user
@api.route('/is_user')
class IsUser(Resource):

    # Returns user information, otherwise nothing
    @api.marshal_with(user_model)
    def post(self):
        resp = is_user()
        return resp