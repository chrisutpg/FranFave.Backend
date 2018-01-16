from flask_restplus import Namespace, Resource, fields, Api
from core.profiles import PubProfile


api = Namespace('Profiles', description='Profile actions for a User')
apiObject = Api()


login_model = api.model('Public Profile',
                        {'id': fields.String(required=True, description='Email Address')
                         })

# API to create a new user
@api.route('/pub_profile')
class User(Resource):

    # API endpoint to create a new user, takes in user_model
    @api.expect(login_model)
    def post(self):
        resp = PubProfile(apiObject.payload)
        return resp