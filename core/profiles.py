from models import db, Reviews, User, Place


def PubProfile(json_data):
    """
    This function takes a reviewer ID and gets the info for the person who wrote it.
    :param json_data: a reviewer ID
    :return: The data for the current reviewer
    """

    # Empty dict to return back in JSON
    profile = {}

    # Get the review ID
    reviewer_id = json_data['id']

    # Get the name for the profile
    get_name = User.query.filter(User.id == reviewer_id).first()

    # Set the name
    profile['name'] = get_name.first_name + " " + get_name.last_name[0]

    # Get all the reviews by this reviewer
    reviews = Reviews.query.filter(Reviews.reviewer_id == reviewer_id).all()

    # Empty list for return
    all_reviews = []

    total_reviews = 0
    # Send back the review data
    for review in reviews:
        total_reviews += 1
        temp_dict = {}
        temp_dict['reviewer_id'] = review.reviewer_id
        temp_dict['review_id'] = review.id
        temp_dict['cat1_score'] = review.cat_1
        temp_dict['cat2_score'] = review.cat_2
        temp_dict['cat3_score'] = review.cat_3
        temp_dict['cat4_score'] = review.cat_4
        temp_dict['cat5_score'] = review.cat_5
        temp_dict['comments'] = review.comments

        # Get the visited date & review date and send them back
        throw_visited = review.visited_date
        throw_reviewed = review.review_date

        # Turn them into strings
        temp_dict['visited_date'] = str(throw_visited)[0:10]
        temp_dict['review_date'] = str(throw_reviewed)[0:10]

        # Round the avg score something readable
        throw_avg = float(review.review_avg)
        avg_score = round(throw_avg * 2) / 2
        temp_dict['avg_score'] = str(avg_score)

        # Get the info for PLACE in this review
        place = Place.query.filter(Place.id == review.place_id).first()

        # Set the name of the place
        temp_dict['place_name'] = place.name

        # Set the place address
        temp_dict['address'] = place.address + " " + place.address_city + " " + place.address_state + " " + place.address_zip + " " + place.address_country

        all_reviews.append(temp_dict)

    profile['reviews'] = all_reviews
    profile['total_reviews'] = str(total_reviews)
    return profile, 200

