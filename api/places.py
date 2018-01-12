from flask_restplus import Namespace, Resource, fields, Api
from core.places import search_places, single_place, leave_review


api = Namespace('Places', description='Get all the places')
apiObject = Api()


search_model = api.model('Search',
                        {'keyword': fields.String(required=True, description='Phrase, or Word'),
                         'location': fields.String(required=True, description='City, State, or Zip'),
                         })

single_model = api.model('Single Place',
                        {'id': fields.String(requried=False, description='FranFave database ID'),
                         'gid': fields.String(required=False, description='Google Places ID')
                         })

review_model = api.model('Leave Review',
    {'id': fields.String(required=True, description='FranFace ID or Google Places ID')})


# End point to search for place
@api.route('/search_places')
class SearchPlaces(Resource):

    @api.expect(search_model)
    def post(self):
        resp = search_places(apiObject.payload)
        return resp


# End point for single place details
@api.route('/single_place')
class SinglePlace(Resource):

    @api.expect(single_model)
    def post(self):
        resp = single_place(apiObject.payload)
        return resp


# End point for single place review
@api.route('/leave_review')
class LeaveReview(Resource):

    @api.expect(review_model)
    def post(self):
        resp = leave_review(apiObject.payload)
        return resp
