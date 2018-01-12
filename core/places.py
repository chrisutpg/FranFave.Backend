from sqlalchemy.exc import DataError
from googleplaces import GooglePlaces
from yelpapi import YelpAPI
from flask import jsonify
from models import db, Place
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
        result_dict['google_rating'] = str(result.rating)
        result_dict['id'] = place_id
        result_dict['yelp_rating'] = str(yelp_rating)
        result_dict['avg_rating'] = str(avg_rating)
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

    # Try to find the place in our Database, if we can't,
    # call Google Places API to get the details to add to our database
    place_id = json_data['id']
    try:
        our_data = Place.query.filter(Place.id == place_id).first()
    except DataError:
        our_data = None

    # If we don't have the data we need to add it, we do that in this code block / if we have it this skips
    if not our_data:
        place_details = google_places.get_place(place_id=place_id)

        # Street Addr from google Places API
        addr = place_details.details['address_components'][0]['long_name'] + " " + \
               place_details.details['address_components'][1]['long_name']

        # City from google Places API
        addr_city = place_details.details['address_components'][2]['short_name']

        # State short name 'XX' from google places API
        addr_state = place_details.details['address_components'][5]['short_name']

        # Zip code from places API
        addr_zip = place_details.details['address_components'][7]['long_name']

        # Country from google places API
        addr_country = place_details.details['address_components'][6]['short_name']

        # International formatted phone number from google places API
        phone_inter = place_details.details['international_phone_number']

        # Franchise name from google places API
        place_name = place_details.details['name']

        add_new_place = Place(gid=place_id,  # The place ID in this case would be a Google Places Reference ID
                              name=place_name,
                              phone1=phone_inter,
                              address=addr,
                              address_city=addr_city,
                              address_state=addr_state,
                              address_zip=addr_zip,
                              address_country=addr_country)
        db.session.add(add_new_place)
        db.session.commit()


    # TODO add the factors
    print(current_user.id)
    print(json_data)
    return ''

