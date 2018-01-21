from flask_restplus import Namespace, Resource, fields, Api
from core.profiles import PubProfile, add_my_place, private_profile


api = Namespace('Profiles', description='Profile actions for a User')
apiObject = Api()


login_model = api.model('Public Profile',
                        {'id': fields.String(required=True, description='Email Address')
                         })

add_place_model = api.model('Add My Place',
                            {'id': fields.String(required=True, description='A Place ID')})

# API to create a new user
@api.route('/pub_profile')
class User(Resource):

    # API endpoint to create a new user, takes in user_model
    @api.expect(login_model)
    def post(self):
        resp = PubProfile(apiObject.payload)
        return resp

# End Point To Add a Place to 'My Places'
@api.route('/add_my_place')
class AddPlace(Resource):

    # Add a place to my places, also requires a valid token
    @api.expect(add_place_model)
    def post(self):
        resp = add_my_place(apiObject.payload)
        return resp

# End Point to return the users private profile
@api.route('/private_profile')
class PrivateProfile(Resource):

    # Get the private profile for the logged in user, required valid token
    def get(self):
        resp = private_profile()
        return resp