from models import db, Reviews, User, UserProfile, Place, my_places
from .auth import token_required


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

@token_required
def add_my_place(current_user, json_data):
    """
    Add a place to 'My Places' for the user, requires a valid token to get the user ID
    :param json_data: the place_id
    :return: Success or Error
    """

    # Get the place ID from Frontend
    place_id = json_data['id']

    # Get the User ID from the token
    user_id = current_user.id

    # Add the place to my_places table
    statement = my_places.insert().values(place_id=place_id, user_id=user_id)
    db.session.execute(statement)
    db.session.commit()

    return 200


@token_required
def private_profile(current_user):
    """
    Returns the users private profile
    :param current_user: the current_user from the token ID
    :return: the private profile for the user is JSON
    """

    #Empty Dict for JSON return
    profile = {}

    # Get the user info for the current user
    the_user = User.query.filter(User.id == current_user.id).first()
    # Add some of the details to the user to the profile dict
    profile['first_name'] = the_user.first_name
    profile['last_name'] = the_user.last_name
    profile['email'] = the_user.email

    # Find the profile for the current user
    user_profile = UserProfile.query.filter(UserProfile.user_id == current_user.id).first()
    profile['bday'] = user_profile.birthday
    profile['address'] = user_profile.address
    profile['address_city'] = user_profile.address_city
    profile['address_state'] = user_profile.address_state
    profile['address_zip'] = user_profile.address_zip

    # Find the 'My Places' for the current user
    user_places = Place.query.join(my_places).filter(my_places.c.user_id == current_user.id).all()

    # Empty place list
    places = []

    # Loop through their places and set the info
    for place in user_places:
        temp_dict = {}
        temp_dict['place_id'] = place.id
        temp_dict['place_name'] = place.name
        temp_dict['address'] = place.address + ", " + place.address_city + ", " + place.address_state + " " + place.address_zip

        # Start the stats for the reviews
        total_reviews = 0
        review_scores = 0
        cat1_scores = 0
        cat2_scores = 0
        cat3_scores = 0
        cat4_scores = 0
        cat5_scores = 0

        place_reviews = Reviews.query.filter(Reviews.place_id == place.id).all()

        for review in place_reviews:
            total_reviews += 1
            review_scores += float(review.review_avg)
            cat1_scores += review.cat_1
            cat2_scores += review.cat_2
            cat3_scores += review.cat_3
            cat4_scores += review.cat_4
            cat5_scores += review.cat_5

        # Get the avg of all scores
        review_avg_not_rounded = review_scores / total_reviews
        review_avg = round(review_avg_not_rounded * 2) / 2

        cat1_avg_not_rounded = cat1_scores / total_reviews
        cat1_avg = round(cat1_avg_not_rounded * 2) / 2

        cat2_avg_not_rounded = cat2_scores / total_reviews
        cat2_avg = round(cat2_avg_not_rounded * 2) / 2

        cat3_avg_not_rounded = cat3_scores / total_reviews
        cat3_avg = round(cat3_avg_not_rounded * 2) / 2

        cat4_avg_not_rounded = cat4_scores / total_reviews
        cat4_avg = round(cat4_avg_not_rounded * 2) / 2

        cat5_avg_not_rounded = cat5_scores / total_reviews
        cat5_avg = round(cat5_avg_not_rounded * 2) / 2

        temp_dict['avg_score'] = review_avg
        temp_dict['cat1_score'] = cat1_avg
        temp_dict['cat2_score'] = cat2_avg
        temp_dict['cat3_score'] = cat3_avg
        temp_dict['cat4_score'] = cat4_avg
        temp_dict['cat5_score'] = cat5_avg

        places.append(temp_dict)

    # Add the places list to the return
    profile['my_places'] = places

    # This gives up the current users reviews from the pubProfile function
    my_reviews, throw_away = PubProfile({'id': current_user.id})
    profile['my_reviews'] = my_reviews

    return profile, 200