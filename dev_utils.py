from googleplaces import GooglePlaces
from yelpapi import YelpAPI
from pprint import pprint
from flask_mail import Message
from datetime import datetime
from models import db, Place, Reviews
from flask import Flask, current_app
from app import app, mail



def api():
    # Google API Key for places
    API_KEY = "AIzaSyBM7aOj21cM0LyY07I0EDBSpTNwFrYxlfU"

    # Google Place ID for development testing
    our_place = "ChIJU15olDoGwYkR5V4cJDvVpuI"

    # Yelp Keys
    clientid = "jSrFJLrPGi5-n3JuO-ySFA"
    clientsecret = "WS5tdjDSzoiXSgm8q9UyogiuYbYSUzjHsDlhluP4rvsp9pohCmuFDIodNCM1gW05"

    # Yelp Object
    yelp = YelpAPI(clientid, clientsecret)

    # Google Object
    google = GooglePlaces(API_KEY)

    # Only gives name, lat & lng
    place = google.get_place(place_id=our_place)
    pprint(place.details)
    print(place.details['address_components'][0]['long_name'])
    print(place.details['address_components'][1]['long_name'])
    print(place.details['address_components'][2]['short_name'])
    print(place.details['address_components'][5]['short_name'])
    #print(place.details['address_components'][7]['long_name'])
    #print(place.details['address_components'][6]['short_name'])
    print(place.details['international_phone_number'])
    print(place.details['name'])

    if our_place == place.place_id:
        print('Yes')

    addr = place.details['formatted_address'].split(",")
    print(addr)
    print(addr[0], addr[1], addr[2][1:3].strip(), addr[2][4:9], addr[3])
    print(len(addr[2][1:3].strip()))

def app_context():
    with app.app_context():
        query = Place.query.filter_by()
        for x in query:
            print(x.name)

        # Google API Key for places
        API_KEY = "AIzaSyBM7aOj21cM0LyY07I0EDBSpTNwFrYxlfU"

        google = GooglePlaces(API_KEY)

        # Try adding a new place.. ?
        place_id='ChIJn8ORMaIIwYkRDjaLeuBXyN8'
        place_details = google.get_place(place_id=place_id)
        # print(place_details.details)

        # Street Addr from google Places API
        addr = place_details.details['address_components'][0]['long_name'] + " " + \
               place_details.details['address_components'][1]['long_name']
        print(addr)

        # City from google Places API
        addr_city = place_details.details['address_components'][2]['short_name']
        print(addr_city)

        # State short name 'XX' from google places API
        addr_state = place_details.details['address_components'][5]['short_name']
        print(addr_state)

        # Zip code from places API
        addr_zip = place_details.details['address_components'][7]['long_name']
        print(addr_zip)

        # Country from google places API
        addr_country = place_details.details['address_components'][6]['short_name']
        print(addr_country)

        # International formatted phone number from google places API
        phone_inter = place_details.details['international_phone_number']
        print(phone_inter)

        # Franchise name from google places API
        place_name = place_details.details['name']
        print(place_name)

        new_place = Place(gid=place_id,  # The place ID in this case would be a Google Places Reference ID
                          name=place_name,
                          phone1="test",
                          address=addr,
                          address_city=addr_city,
                          address_state=addr_state,
                          address_zip=addr_zip,
                          address_country=addr_country)
        # TODO add try/except block for errors
        print('test1')
        db.session.add(new_place)
        db.session.commit()


def whos_data(place_id):
    """
    This function helps decide weather we have the data or we need to call Places API to get it
    :param id: Can be a Google Places Refernce ID, or our database primary key to a place
    :return: either False if we do not have the data, or return the data if we do.
    """
    try:
        int_check = int(place_id)
    except ValueError:
        int_check = False

    if int_check is False:
        return False
    else:
        our_data = Place.query.filter(Place.id == place_id).first()
        return our_data


with app.app_context():
    msg = Message("Hello",
                  sender="chris@uptopargolf.com",
                  recipients=["chris@uptopargolf.com"])
    msg.body = 'Testing'
    mail.send(msg)