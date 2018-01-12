from googleplaces import GooglePlaces
from yelpapi import YelpAPI
from pprint import pprint


# Google API Key for places
API_KEY = "AIzaSyBM7aOj21cM0LyY07I0EDBSpTNwFrYxlfU"

# Google Place ID for development testing
our_place = "ChIJY1l7DbQJwYkRsKxg8RAl7FU"

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
print(place.details['address_components'][7]['long_name'])
print(place.details['address_components'][6]['short_name'])
print(place.details['international_phone_number'])
print(place.details['name'])

if our_place == place.place_id:
    print('Yes')