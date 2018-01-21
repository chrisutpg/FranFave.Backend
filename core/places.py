from sqlalchemy.exc import DataError
from urllib.error import HTTPError
from googleplaces import GooglePlaces
from yelpapi import YelpAPI
from flask import jsonify
from datetime import datetime
from models import db, Place, Reviews, User
from core.auth import token_required
from core.utils import add_place, whos_data


API_KEY = "AIzaSyBM7aOj21cM0LyY07I0EDBSpTNwFrYxlfU"
clientid = "jSrFJLrPGi5-n3JuO-ySFA"
clientsecret = "WS5tdjDSzoiXSgm8q9UyogiuYbYSUzjHsDlhluP4rvsp9pohCmuFDIodNCM1gW05"

# Yelp API object
yelp = YelpAPI(clientid, clientsecret)

google = GooglePlaces(API_KEY)

def search_places(json_data):
    """
    Search places from the google places API
    :param json_data: search term, or keyword, location, zip or city/state
    :return: list of results in JSON
    """
    print(json_data)
    # Get the keyword to search for, and the location, possibly longitude/latitude
    # TODO add some kind of check to make sure it is a franchise/chain?
    search_term = json_data['keyword']
    location = json_data['location']
    long = json_data['long']
    lat = json_data['lat']

    # Set the return list to empty before we start adding to it
    search_return = []

    if long is None and lat is None:
        # Call the Places API to search for our places
        try:
            search = google.nearby_search(keyword=search_term, location=location, rankby='distance')
        except HTTPError:
            return {'Err': "Uh Oh.. It looks like something went wrong. Check the search terms or try again in a bit!"}
    else:
        # Call the Places API to search for our places
        try:
            search = google.nearby_search(keyword=search_term, lat_lng={"lat": lat, "lng": long}, rankby='distance')
        except HTTPError:
            return {'Err': "Uh Oh.. It looks like something went wrong. Check the search terms or try again in a bit!"}

    # If we provide correct stuff, but get nothing back
    if search is None:
        return {'Err': "Uh Oh.. It looks like we couldn't find what you searched for! Check the spelling and location!"}

    # Loop through the return and do stuff
    for place in search.places:

        # Get details for each place
        place.get_details()

        # Empty dict to spend to our search_return
        details = {}

        # Set some initial values for the search_return, these wouldn't change even if in our database
        details['name'] = place.name
        details['address'] = place.formatted_address
        details['phone'] = place.international_phone_number

        # Get the Reference ID and cross it with our database, if we have info on it we need to return are stuff also
        google_ref_id = place.place_id

        # Cross check our places database to see if we have info on it
        in_db = Place.query.filter(Place.gid == google_ref_id).first()

        # If we have the info in our database, get it and find the reviews
        if in_db:

            # We want the details['id'] to be OUR database ID if its our info, so we don't call Google API again
            place_id = in_db.id
            details['id'] = place_id

            # Now we need to get the Reviews information
            get_reviews = Reviews.query.filter(Reviews.place_id == place_id).all()

            # If no reviews, skip this.. In theory this should never happen. You can't add a place without reviewing
            if get_reviews:

                total_reviews = 0
                review_scores = 0
                # During the search_places return we only show the overall rating, not EVERY review
                for review in get_reviews:
                    total_reviews += 1
                    review_scores += float(review.review_avg)

                # Get the avg of all scores
                review_avg_not_rounded = review_scores / total_reviews
                review_avg = round(review_avg_not_rounded * 2) / 2

                # Set the returns for the reviews, need to watch out for decimals, JSON doesn't like them!
                details['review_avg'] = str(review_avg)
                details['total_reviews'] = str(total_reviews)



        else:
            details['id'] = google_ref_id
            details['review_avg'] = None
            details['total_reviews'] = None

        # Append the dict to the search_return list
        search_return.append(details)

    # JSONIFY and return it
    return jsonify({"search_return": search_return})

def single_place(json_data):
    """
    Get info for a single place on the Google API & our database
    :param json_data: a single id, either a google places id or our database id
    :return: info for single place in JSON (reivews, comments, etc)
    """

    # Empty dict to put our return into
    details = {}

    # Get the ID
    place_id = json_data['id']

    # Check to see if we have the place in our database, if not make call to Google Places API for details
    find_it = whos_data(place_id)

    # If we don't have it, get google places data
    if find_it is False:

        # This gets the info
        place = google.get_place(place_id=place_id)

        # Place the info into details dict for return
        details['id'] = place_id
        details['name'] = place.name
        details['phone'] = place.international_phone_number
        details['address'] = place.formatted_address

        # It would not be possible for us to have reviews if the place is not in our DB
        details['review_avg'] = None
        details['total_reviews'] = None

        # This is an empty dict without reviews
        details['reviews'] = {}

        # This is an empty dict without review scores
        details['review_stats'] = {}

    # If we find_it we need to get all of OUR info, avoid google API call, pull all reviews and send it off
    else:

        # find_it is now database object
        details['id'] = find_it.id
        details['name'] = find_it.name
        details['phone'] = find_it.phone

        # Need to put together the address
        formatted_address = find_it.address + ", " + find_it.address_city + ", " + find_it.address_state + ", " + find_it.address_zip + " " + find_it.address_country
        details['address'] = formatted_address

        # Get all reviews for given place
        get_reviews = db.session.query(Reviews).filter(Reviews.place_id == find_it.id).order_by(Reviews.review_date.desc()).all()

        # If no reviews, skip this.. In theory this should never happen. You can't add a place without reviewing
        if get_reviews:

            total_reviews = 0
            review_scores = 0
            cat1_scores = 0
            cat2_scores = 0
            cat3_scores = 0
            cat4_scores = 0
            cat5_scores = 0

            # Set a list for individual reviews, we limit the length to 100 reviews
            each_review = []

            # Calulate overall reviews and avgs
            for review in get_reviews:
                total_reviews += 1
                review_scores += float(review.review_avg)
                cat1_scores += review.cat_1
                cat2_scores += review.cat_2
                cat3_scores += review.cat_3
                cat4_scores += review.cat_4
                cat5_scores += review.cat_5

                # If our total_reviews less 100, continue
                if total_reviews <= 100:
                    get_name = User.query.filter(User.id == review.reviewer_id).first()

                    temp_dict = {}
                    temp_dict['first_name'] = get_name.first_name + " " + get_name.last_name[0]
                    temp_dict['reviewer_id'] = review.reviewer_id
                    temp_dict['review_id'] = review.id
                    temp_dict['cat1_score'] = review.cat_1
                    temp_dict['cat2_score'] = review.cat_2
                    temp_dict['cat3_score'] = review.cat_3
                    temp_dict['cat4_score'] = review.cat_4
                    temp_dict['cat5_score'] = review.cat_5
                    temp_dict['comments'] = review.comments

                    #Get the visited date & review date and send them back
                    throw_visited = review.visited_date
                    throw_reviewed = review.review_date

                    #Turn them into strings
                    temp_dict['visited_date'] = str(throw_visited)[0:10]
                    temp_dict['review_date'] = str(throw_reviewed)[0:10]

                    # Round the avg score something readable
                    throw_avg = float(review.review_avg)
                    avg_score = round(throw_avg * 2) / 2
                    temp_dict['avg_score'] = str(avg_score)

                    each_review.append(temp_dict)

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

            # Set the returns for the reviews, need to watch out for decimals, JSON doesn't like them!
            details['review_avg'] = str(review_avg)
            details['total_reviews'] = str(total_reviews)
            details['review_stats'] = {"cat1_avg": str(cat1_avg),
                                       "cat2_avg": str(cat2_avg),
                                       "cat3_avg": str(cat3_avg),
                                       "cat4_avg": str(cat4_avg),
                                       "cat5_avg": str(cat5_avg)}

            # Add individual review list
            details['reviews'] = each_review

    # Send it back
    return details

@token_required
def leave_review(current_user, json_data):
    """
    Leave a review for a single place, the reviewer needs to be authed
    :param json_data: review scores, auth token
    :return: Success or Error based on factors
    """

    # This can be a Google Place Refernce ID, or our database primary key
    place_id = json_data['id']

    # Try to find the place in our Database, if we can't,
    # call Google Places API to get the details to add to our database
    find_it = whos_data(place_id)

    # If we don't have the data we need to add it, we do that in this code block / if we have it this skips
    if find_it is False:
        newly_added = add_place(place_id)

    # Now lets get the details from the review
    cat1 = json_data['cat1']
    cat2 = json_data['cat2']
    cat3 = json_data['cat3']
    cat4 = json_data['cat4']
    cat5 = json_data['cat5']
    comments = json_data['comments']
    visited_date = json_data['visited']

    # Make sure all of our categories has valid data, if not we need to return an error
    valid_data = [cat1, cat2, cat3, cat4, cat5]

    # 0 is form default, if 0 something is missing
    if 0 in valid_data:
        return {'Err': 'It looks likes the review is missing some required data!'}, 401

    if visited_date:
        # Make a datetime object from the user input
        # data should look like '2018-01-10T05:00:00.000Z'
        # TODO this needs refactor both front and back ends
        # Get rid of excess string
        date = visited_date[0:10]
        date_obj = datetime.strptime(date, '%Y-%m-%d')
    else:
        date_obj = None


    # TODO add something to see if any fields are blank

    # Set the Avg Rating
    review_avg = (int(cat1) + int(cat2) + int(cat3) + int(cat4) + int(cat5)) / 5

    # Get the correct foreign key to use
    if find_it is False:
        fkey_place = newly_added.id
    else:
        fkey_place = find_it.id

    add_new_review = Reviews(place_id=fkey_place,
                             reviewer_id=current_user.id,
                             visited_date=date_obj,
                             cat_1=cat1,
                             cat_2=cat2,
                             cat_3=cat3,
                             cat_4=cat4,
                             cat_5=cat5,
                             review_avg=str(review_avg),  # store as a string, later can take it into float
                             comments=comments)
    # TODO add try/except incase of error
    db.session.add(add_new_review)
    db.session.commit()

    # TODO add the factors

    return {'Success': 'Thanks for reviewing this location!', 'place_id': fkey_place}, 200

def recent_reviews(json_data):
    """
    This function return the x amount of recent reviews
    :param json_data: the amount of reviews to return
    :return: the reviews in date order from most recent to oldest
    """

    # Find out how many we need to retrieve
    how_many = json_data['how_many']

    # Retrieve them from the reviews database
    reviews = db.session.query(Reviews).order_by(Reviews.review_date.desc()).limit(how_many).all()

    # Set empty dict for json returns
    recents = {}

    # Set empty list for appending
    review_list = []

    # Loop through the reviews for the details
    for review in reviews:
        temp_dict = {}
        temp_dict['reviewer_id'] = review.reviewer_id
        temp_dict['review_id'] = review.id
        temp_dict['place_id'] = review.place_id
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

        # Get the name for the profile
        get_name = User.query.filter(User.id == review.reviewer_id).first()

        # Set the name
        temp_dict['reviewer_name'] = get_name.first_name + " " + get_name.last_name[0]

        # Set the name of the place
        temp_dict['place_name'] = place.name

        # Set the place address
        temp_dict['address'] = place.address + ", " + place.address_city + ", " + place.address_state + " " + place.address_zip

        review_list.append(temp_dict)

    recents['reviews'] = review_list

    return recents, 200