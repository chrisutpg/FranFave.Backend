from models import db, Reviews, User


def PubProfile(json_data):
    review_id = json_data['id']
    get_review = Reviews.query.filter(Reviews.id == review_id).first()
    get_user = User.query.filter(User.id == get_review.reviewer_id).first()
    return {'first_name' : get_user.first_name}