from flask_restplus import Api
from .auth import api as auth
from .places import api as places
from .profiles import api as profiles
from config import authorizations


api = Api(
    title='My Title',
    version='1.0',
    description='A description',
    authorizations=authorizations,
    # All API metadatas
)

api.add_namespace(auth, path='/auth')
api.add_namespace(places, path='/places')
api.add_namespace(profiles, path='/profiles')
