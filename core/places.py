from sqlalchemy.exc import DataError
from googleplaces import GooglePlaces
from yelpapi import YelpAPI
from flask import jsonify
from models import Place
from core.auth import token_required


API_KEY = "AIzaSyBM7aOj21cM0LyY07I0EDBSpTNwFrYxlfU"
our_place = "ChIJY1l7DbQJwYkRsKxg8RAl7FU"
clientid = "jSrFJLrPGi5-n3JuO-ySFA"
clientsecret = "WS5tdjDSzoiXSgm8q9UyogiuYbYSUzjHsDlhluP4rvsp9pohCmuFDIodNCM1gW05"

# Yelp API object
yelp = YelpAPI(clientid, clientsecret)

# Google Places API Object
google_places = GooglePlaces(API_KEY)

def search_places(json_data):
    """
    Search places from the google places API
    :param json_data: search term, or keyword, location, zip or city/state
    :return: list of results in JSON
    """
    search_term = json_data['keyword']
    location = json_data['location']

    query_json = []

    query = google_places.text_search(query=search_term, location=location)

    for result in query.places:
        result.get_details()
        # TODO make this code more better :)
        formatted_int_phone = result.international_phone_number.replace("-", "",)
        formatted_int_phone = formatted_int_phone.replace(" ", "")
        yelp_query = yelp.phone_search_query(phone=formatted_int_phone)
        if yelp_query['businesses']:
            yelp_rating = yelp_query['businesses'][0]['rating']
        else:
            yelp_rating = None
        if yelp_rating != None and result.rating != None:
            avg_rating = (float(yelp_rating) + float(result.rating)) / 2
        else:
            avg_rating = None
        our_data = Place.query.filter(Place.gid == result.place_id).first()
        if our_data:
            print(our_data.id)
            place_id = our_data.id
        else:
            print(our_data)
            place_id = result.place_id
        result_dict = {}
        result_dict['name'] = result.name
        result_dict['address'] = result.formatted_address
        result_dict['google_rating'] = result.rating
        result_dict['id'] = place_id
        result_dict['yelp_rating'] = yelp_rating
        result_dict['avg_rating'] = avg_rating
        query_json.append(result_dict)
    return jsonify({'query' : query_json})


def single_place(json_data):
    """
    Get info for a single place on the Google API & our database
    :param json_data: a single id, either a google places id or our database id
    :return: info for single place in JSON (reivews, comments, etc)
    """

    # Get the ID
    place_id = json_data['id']

    # Try for Integer ID first, if it fails, the ID is String Type for Google Places API
    try:
        our_data = Place.query.filter(Place.id == place_id).first()
    except DataError:
        our_data = None

    # If we have the data, give that to user and do not make another Places API call
    if our_data:
        return {'name' : our_data.name, 'id': our_data.id}
        # Do something later

    # If we don't have the data, get it from the places API and show it to the user
    else:
        place = google_places.get_place(place_id=place_id)
        details_dict = {'name': place.name, 'address': place.formatted_address, 'phone': place.local_phone_number,
                        'google_url': place.url, 'website': place.website, 'id': place_id}

    return details_dict


@token_required
def leave_review(current_user, json_data):
    """
    Leave a review for a single place, the reviewer needs to be authed
    :param json_data: review scores, auth token
    :return: Success or Error based on factors
    """
    # TODO add the factors
    print(current_user.id)
    print(json_data)
    return ''

